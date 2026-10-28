import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap, of, map, catchError } from 'rxjs';
import { AppNotification } from '../models/notification.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private baseUrl = `${environment.apiUrl}/notifications`;

  private unreadCountSubject = new BehaviorSubject<number>(0);
  public unreadCount$ = this.unreadCountSubject.asObservable();

  private notificationsSubject = new BehaviorSubject<AppNotification[]>([]);
  public notifications$ = this.notificationsSubject.asObservable();

  constructor(private http: HttpClient) {
    // Purge any legacy client-side cached notifications from localStorage
    try {
      const keysToRemove: string[] = [];
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i);
        if (k && k.startsWith('cropdeal_notifications')) {
          keysToRemove.push(k);
        }
      }
      keysToRemove.forEach(k => localStorage.removeItem(k));
    } catch {}
  }

  public resolveRoleBucket(identifier?: string | null): 'farmer' | 'dealer' | 'delivery' | 'admin' | 'guest' {
    if (!identifier) return 'guest';
    const s = String(identifier).trim().toLowerCase();
    if (s === '1' || s.includes('farmer')) return 'farmer';
    if (s === '2' || s.includes('dealer')) return 'dealer';
    if (s === '3' || s.includes('delivery')) return 'delivery';
    if (s === '4' || s.includes('admin')) return 'admin';
    try {
      const stored = localStorage.getItem('cropdeal_user');
      if (stored) {
        const u = JSON.parse(stored);
        if (String(u.id) === s || String(u.userId) === s || String(u.username).toLowerCase() === s) {
          const r = String(u.role || '').toLowerCase();
          if (r.includes('farmer')) return 'farmer';
          if (r.includes('dealer')) return 'dealer';
          if (r.includes('delivery')) return 'delivery';
          if (r.includes('admin')) return 'admin';
        }
      }
    } catch {}
    return 'guest';
  }

  private getCurrentUserId(): string | null {
    try {
      const stored = localStorage.getItem('cropdeal_user');
      if (stored) {
        const u = JSON.parse(stored);
        return String(u.id || u.userId || '');
      }
    } catch {}
    return null;
  }

  /**
   * Fetches real notifications from the backend Notification Service.
   * If notification-service is stopped / down, this returns [] and resets the notification count to 0.
   * No fallback to fake localStorage data is permitted.
   */
  getUserNotifications(userId: string): Observable<AppNotification[]> {
    if (!userId) {
      this.notificationsSubject.next([]);
      this.unreadCountSubject.next(0);
      return of([]);
    }

    return this.http.get<any[]>(`${this.baseUrl}/user/${userId}`).pipe(
      map(backendList => {
        if (!backendList || !Array.isArray(backendList)) return [];
        return backendList.map(b => ({
          id: String(b.id),
          userId: String(b.recipient || userId),
          title: b.type ? b.type.replace(/_/g, ' ') : 'Notification',
          message: b.message || '',
          type: (b.type || 'SYSTEM') as any,
          isRead: b.status === 'READ' || b.read === true || b.isRead === true,
          createdAt: b.createdAt || new Date().toISOString()
        }));
      }),
      tap(mapped => {
        this.notificationsSubject.next(mapped);
        this.unreadCountSubject.next(mapped.filter(n => !n.isRead).length);
      }),
      catchError(err => {
        console.warn('Backend notification service unreachable. Resetting notification stream:', err);
        // Strict requirement: When notification service is stopped, do NOT show fake/cached notifications!
        this.notificationsSubject.next([]);
        this.unreadCountSubject.next(0);
        return of([]);
      })
    );
  }

  clearStream(): void {
    this.notificationsSubject.next([]);
    this.unreadCountSubject.next(0);
  }

  markAsRead(notificationId: string, userId?: string): Observable<void> {
    const current = this.notificationsSubject.value.map(n =>
      n.id === notificationId ? { ...n, isRead: true } : n
    );
    this.notificationsSubject.next(current);
    this.unreadCountSubject.next(current.filter(n => !n.isRead).length);

    return this.http.put<void>(`${this.baseUrl}/${notificationId}/read`, {}).pipe(
      catchError(() => of(undefined as any))
    );
  }

  deleteNotification(notificationId: string, userId?: string): Observable<boolean> {
    const updated = this.notificationsSubject.value.filter(n => n.id !== notificationId);
    this.notificationsSubject.next(updated);
    this.unreadCountSubject.next(updated.filter(n => !n.isRead).length);

    return this.http.delete<void>(`${this.baseUrl}/${notificationId}`).pipe(
      map(() => true),
      catchError(() => of(true))
    );
  }

  markAllAsRead(userId?: string): void {
    const current = this.notificationsSubject.value.map(n => ({ ...n, isRead: true }));
    this.notificationsSubject.next(current);
    this.unreadCountSubject.next(0);

    const uid = userId || this.getCurrentUserId() || 'me';
    this.http.put(`${this.baseUrl}/user/${uid}/read-all`, {}).pipe(
      catchError(() => of(null))
    ).subscribe();
  }

  clearAllNotifications(userId?: string): void {
    this.notificationsSubject.next([]);
    this.unreadCountSubject.next(0);

    const uid = userId || this.getCurrentUserId() || 'me';
    this.http.delete(`${this.baseUrl}/user/${uid}/clear-all`).pipe(
      catchError(() => of(null))
    ).subscribe();
  }

  /**
   * For backwards compatibility: routes through asynchronous RabbitMQ notification flow
   */
  addClientNotification(notification: AppNotification, userId?: string): void {
    this.sendNotification(
      userId || notification.userId,
      notification.title,
      notification.message,
      notification.type as any
    );
  }

  /**
   * Sends a notification asynchronously through the Notification Service backend & RabbitMQ.
   */
  sendNotification(
    userId: string,
    title: string,
    message: string,
    type: 'ORDER' | 'NEGOTIATION' | 'BID' | 'PRICE_ALERT' | 'WALLET' | 'DELIVERY' | 'SYSTEM',
    targetRole?: 'farmer' | 'dealer' | 'delivery' | 'admin'
  ): void {
    const payload = {
      recipient: userId,
      type: type || 'SYSTEM',
      message: `${title}: ${message}`
    };

    // Dispatch to Backend notification-service so RabbitMQ topic exchange publishes the message
    this.http.post(`${this.baseUrl}`, payload).pipe(
      catchError(err => {
        console.warn('RabbitMQ notification backend dispatch warning:', err);
        return of(null);
      })
    ).subscribe({
      next: () => {
        const currentUserId = this.getCurrentUserId();
        if (currentUserId && (currentUserId === String(userId) || userId === 'ALL')) {
          this.getUserNotifications(currentUserId).subscribe();
        }
      }
    });
  }
}
