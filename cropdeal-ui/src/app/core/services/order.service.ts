import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, catchError, map, of, tap } from 'rxjs';
import { CreateOrderRequest, Order } from '../models/order.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class OrderService {
  private baseUrl = `${environment.apiUrl}/orders`;
  private readonly ORDERS_KEY = 'cropdeal_orders_cache';

  private ordersSubject = new BehaviorSubject<Order[]>(this.loadStoredOrders());
  public orders$ = this.ordersSubject.asObservable();

  constructor(private http: HttpClient) {
    if (typeof window !== 'undefined') {
      window.addEventListener('storage', (e: StorageEvent) => {
        if (e.key === this.ORDERS_KEY) {
          this.refreshOrders();
        }
      });
    }
  }

  refreshOrders(): Order[] {
    const orders = this.loadStoredOrders();
    this.ordersSubject.next(orders);
    return orders;
  }

  private loadStoredOrders(): Order[] {
    try {
      const raw = localStorage.getItem(this.ORDERS_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed)) return parsed;
      }
    } catch {}
    return [];
  }

  private saveOrders(orders: Order[]): void {
    try {
      localStorage.setItem(this.ORDERS_KEY, JSON.stringify(orders));
      this.ordersSubject.next(orders);
    } catch {}
  }

  createOrder(req: CreateOrderRequest): Observable<Order> {
    const orderId = (req as any).id || (req as any).orderId || ('ORD-' + Math.floor(10000 + Math.random() * 90000));
    const newOrder: Order = {
      id: orderId,
      cropId: req.cropId,
      cropName: req.cropName || 'Harvest Crop',
      farmerId: req.farmerId || 'farmer-1',
      farmerName: req.farmerName || 'Sardar Gurpreet Singh',
      dealerId: req.dealerId,
      dealerName: req.dealerName || 'Apex Agro Mills Ltd',
      quantity: req.quantity,
      unit: req.unit || 'Kg',
      pricePerUnit: req.pricePerUnit || Math.round(req.totalPrice / (req.quantity || 1)),
      govMspPrice: req.govMspPrice,
      totalPrice: req.totalPrice,
      taxAmount: req.taxAmount || Math.round(req.totalPrice * 0.05),
      deliveryFee: req.deliveryFee || 0,
      finalAmount: req.finalAmount || req.totalPrice,
      fulfillmentType: req.fulfillmentType || 'DELIVERY_AGENT',
      distanceKm: req.distanceKm,
      paymentMethod: req.paymentMethod || 'Stripe Demo (Card **** 4242)',
      transactionId: req.transactionId || 'STRIPE-TXN-' + Math.floor(100000 + Math.random() * 900000),
      status: 'PAID',
      deliveryAddress: req.deliveryAddress,
      isBidding: req.isBidding ?? false,
      createdAt: new Date().toISOString()
    };

    return this.http.post<Order>(this.baseUrl, req).pipe(
      tap((saved) => {
        const orderToSave = { ...newOrder, ...saved, id: (saved && saved.id) ? saved.id : orderId };
        const current = [orderToSave, ...this.ordersSubject.value];
        this.saveOrders(current);
      }),
      catchError(() => {
        const current = [newOrder, ...this.ordersSubject.value];
        this.saveOrders(current);
        return of(newOrder);
      })
    );
  }

  getOrderById(orderId: string): Observable<Order> {
    return this.http.get<Order>(`${this.baseUrl}/${orderId}`).pipe(
      catchError(() => {
        const found = this.ordersSubject.value.find(o => o.id === orderId);
        return of(found as Order);
      })
    );
  }

  getOrdersByDealer(dealerId: string): Observable<Order[]> {
    return this.http.get<Order[]>(`${this.baseUrl}/dealer/${dealerId}`).pipe(
      catchError(() => {
        return of(this.ordersSubject.value.filter(o => o.dealerId === dealerId));
      })
    );
  }

  getOrdersByFarmer(farmerId: string): Observable<Order[]> {
    return this.http.get<Order[]>(`${this.baseUrl}/farmer/${farmerId}`).pipe(
      catchError(() => {
        return of(this.ordersSubject.value.filter(o => o.farmerId === farmerId));
      })
    );
  }

  getAllOrders(): Observable<Order[]> {
    return this.http.get<Order[]>(this.baseUrl).pipe(
      map(backendList => {
        if (backendList && backendList.length > 0) {
          const ids = new Set(backendList.map(o => o.id));
          const localOnly = this.ordersSubject.value.filter(o => !ids.has(o.id));
          return [...localOnly, ...backendList];
        }
        return this.ordersSubject.value;
      }),
      catchError(() => {
        return of(this.ordersSubject.value);
      })
    );
  }

  updateOrderStatus(orderId: string, status: string): Observable<Order> {
    const list = [...this.ordersSubject.value];
    const cleanId = String(orderId).trim();
    let idx = list.findIndex(o => {
      const oId = String(o.id || '').trim();
      return oId === cleanId ||
             ('ORD-' + oId) === cleanId ||
             oId === ('ORD-' + cleanId) ||
             oId.replace('ORD-', '') === cleanId.replace('ORD-', '');
    });
    if (idx === -1) {
      const cleanLower = cleanId.toLowerCase();
      idx = list.findIndex(o => {
        const cName = (o.cropName || '').trim().toLowerCase();
        return cName && (cleanLower.includes(cName) || cName.includes(cleanLower));
      });
    }
    if (idx !== -1) {
      list[idx].status = status as any;
      this.saveOrders(list);
    }
    return this.http.put<Order>(`${this.baseUrl}/${cleanId}/status`, { status }).pipe(
      catchError(() => of(idx !== -1 ? list[idx] : ({} as Order)))
    );
  }
}
