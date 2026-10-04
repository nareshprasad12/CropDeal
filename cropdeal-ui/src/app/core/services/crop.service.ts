import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, BehaviorSubject } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { Crop, CropAlert, GovernmentPrice } from '../models/crop.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CropService {
  private baseUrl = `${environment.apiUrl}/crops`;
  private priceUrl = `${environment.apiUrl}/prices`;
  private readonly CROPS_KEY = 'cropdeal_crops_cache';
  private cropsSubject = new BehaviorSubject<Crop[]>(this.getLocalCrops());
  public crops$ = this.cropsSubject.asObservable();

  constructor(private http: HttpClient) {
    if (typeof window !== 'undefined') {
      window.addEventListener('storage', (e: StorageEvent) => {
        if (e.key === this.CROPS_KEY) {
          this.cropsSubject.next(this.getLocalCrops());
        }
      });
    }
  }

  refreshCrops(): Crop[] {
    const fresh = this.getLocalCrops();
    this.cropsSubject.next(fresh);
    return fresh;
  }

  public findCropIndex(list: Crop[], idOrName: string): number {
    if (!idOrName) return -1;
    const target = String(idOrName).trim().toLowerCase();
    return list.findIndex(c => {
      const cId = c.id !== undefined && c.id !== null ? String(c.id).trim().toLowerCase() : '';
      const cropId = c.cropId !== undefined && c.cropId !== null ? String(c.cropId).trim().toLowerCase() : '';
      const cName = c.cropName ? c.cropName.trim().toLowerCase() : '';
      return cId === target || cropId === target || cName === target ||
             (cName && target && (cName.includes(target) || target.includes(cName)));
    });
  }

  public getLocalCrops(): Crop[] {
    try {
      const raw = localStorage.getItem(this.CROPS_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed)) {
          return parsed.filter(c => {
            const q = c.quantity !== undefined ? c.quantity : c.availableQuantity;
            return q === undefined || q > 0;
          });
        }
      }
    } catch {}
    return [];
  }

  private saveLocalCrops(crops: Crop[]): void {
    try {
      const activeOnly = (crops || []).filter(c => {
        const q = c.quantity !== undefined ? c.quantity : c.availableQuantity;
        return q === undefined || q > 0;
      });
      localStorage.setItem(this.CROPS_KEY, JSON.stringify(activeOnly));
      this.cropsSubject.next(activeOnly);
    } catch {}
  }

  getAllCrops(): Observable<Crop[]> {
    return this.http.get<Crop[]>(this.baseUrl).pipe(
      tap(crops => {
        if (crops && Array.isArray(crops)) this.saveLocalCrops(crops);
      }),
      catchError(() => of(this.getLocalCrops()))
    );
  }

  getCropById(id: string): Observable<Crop> {
    return this.http.get<Crop>(`${this.baseUrl}/${id}`).pipe(
      catchError(() => {
        const found = this.getLocalCrops().find(c => c.id === id || c.cropId === id || c.cropName.toLowerCase() === id.toLowerCase());
        return of(found || ({} as Crop));
      })
    );
  }

  getCropsByFarmer(farmerId: string): Observable<Crop[]> {
    return this.http.get<Crop[]>(`${this.baseUrl}/farmer/${farmerId}`).pipe(
      catchError(() => {
        const list = this.getLocalCrops().filter(c => c.farmerId === farmerId);
        return of(list);
      })
    );
  }

  addCrop(crop: Partial<Crop>): Observable<Crop> {
    const qty = crop.quantity || crop.availableQuantity || 100;
    const newCrop: Crop = {
      ...crop,
      id: crop.id || ('cr-' + Date.now()),
      cropName: crop.cropName || 'Fresh Harvest',
      cropType: crop.cropType || 'Cereals',
      quantity: qty,
      availableQuantity: qty,
      unit: crop.unit || 'Kg',
      pricePerUnit: crop.pricePerUnit || 20,
      location: crop.location || 'Local Mandi Yard',
      status: 'AVAILABLE',
      createdAt: new Date().toISOString()
    };
    const current = [newCrop, ...this.getLocalCrops().filter(c => c.id !== newCrop.id)];
    this.saveLocalCrops(current);

    return this.http.post<Crop>(this.baseUrl, crop).pipe(
      catchError(() => of(newCrop))
    );
  }

  updateCrop(id: string, crop: Partial<Crop>): Observable<Crop> {
    const list = this.getLocalCrops();
    const idx = this.findCropIndex(list, id);
    const qty = crop.quantity !== undefined ? crop.quantity : crop.availableQuantity;
    const finalCrop = { ...crop };
    if (qty !== undefined) {
      finalCrop.quantity = qty;
      finalCrop.availableQuantity = qty;
    }
    let updatedCrop: Crop = idx >= 0 ? { ...list[idx], ...finalCrop } : ({ ...finalCrop, id } as Crop);
    if (idx >= 0) {
      if (qty !== undefined && qty <= 0) {
        return this.deleteCrop(id).pipe(map(() => updatedCrop));
      }
      list[idx] = updatedCrop;
      this.saveLocalCrops(list);
    }

    return this.http.put<Crop>(`${this.baseUrl}/${id}`, crop).pipe(
      catchError(() => of(updatedCrop))
    );
  }

  deleteCrop(id: string): Observable<void> {
    const list = this.getLocalCrops();
    const target = String(id).trim().toLowerCase();
    const filtered = list.filter(c => {
      const cId = c.id !== undefined && c.id !== null ? String(c.id).trim().toLowerCase() : '';
      const cropId = c.cropId !== undefined && c.cropId !== null ? String(c.cropId).trim().toLowerCase() : '';
      const cName = c.cropName ? c.cropName.trim().toLowerCase() : '';
      return cId !== target && cropId !== target && cName !== target;
    });
    this.saveLocalCrops(filtered);

    return this.http.delete<void>(`${this.baseUrl}/${id}`).pipe(
      catchError(() => of(undefined as any))
    );
  }

  reduceQuantity(id: string, purchasedQuantity: number): Observable<any> {
    const list = this.getLocalCrops();
    const idx = this.findCropIndex(list, id);
    if (idx >= 0) {
      const current = list[idx].quantity !== undefined ? list[idx].quantity : (list[idx].availableQuantity || 0);
      const remaining = Math.max(0, current - purchasedQuantity);
      if (remaining <= 0) {
        return this.deleteCrop(id);
      } else {
        list[idx] = { ...list[idx], quantity: remaining, availableQuantity: remaining };
        this.saveLocalCrops(list);
      }
    }
    const numId = Number(id);
    if (!isNaN(numId) && numId > 0) {
      return this.http.patch(`${this.baseUrl}/${id}/quantity`, { purchasedQuantity }).pipe(
        catchError(() => of(null))
      );
    }
    return of(null);
  }

  deductCropStock(idOrName: string, purchasedQuantity: number): { remaining: number; deleted: boolean } {
    const list = this.getLocalCrops();
    const idx = this.findCropIndex(list, idOrName);
    if (idx === -1) {
      return { remaining: 0, deleted: false };
    }
    const current = list[idx].quantity !== undefined ? list[idx].quantity : (list[idx].availableQuantity || 0);
    const remaining = Math.max(0, current - purchasedQuantity);
    const targetId = String(list[idx].id || list[idx].cropId || idOrName);

    if (remaining <= 0) {
      this.deleteCrop(targetId).subscribe();
      return { remaining: 0, deleted: true };
    } else {
      list[idx] = { ...list[idx], quantity: remaining, availableQuantity: remaining };
      this.saveLocalCrops(list);
      this.http.patch(`${this.baseUrl}/${targetId}/quantity`, { purchasedQuantity }).pipe(
        catchError(() => of(null))
      ).subscribe();
      return { remaining, deleted: false };
    }
  }

  // APMC Government Market Prices
  getGovernmentPrices(): Observable<GovernmentPrice[]> {
    return this.http.get<GovernmentPrice[]>(`${this.priceUrl}/all`).pipe(
      catchError(() => of([]))
    );
  }

  syncGovernmentPrices(): Observable<any> {
    return this.http.post<any>(`${this.priceUrl}/sync`, {}).pipe(
      catchError(() => of({ message: 'Synchronized with local APMC market database.' }))
    );
  }

  getGovernmentPriceByCommodity(commodity: string): Observable<GovernmentPrice[]> {
    return this.http.get<GovernmentPrice[]>(`${this.priceUrl}/commodity/${commodity}`).pipe(
      catchError(() => of([]))
    );
  }

  // Crop Price Alert endpoints
  checkLoginPriceAlerts(userId: string): Observable<CropAlert[]> {
    return this.http.get<CropAlert[]>(`${this.priceUrl}/alerts/check-login/${userId}`).pipe(
      catchError(() => of([]))
    );
  }

  getUserPriceAlerts(userId: string): Observable<CropAlert[]> {
    return this.http.get<CropAlert[]>(`${this.priceUrl}/alerts/user/${userId}`).pipe(
      catchError(() => of([]))
    );
  }

  createPriceAlert(alert: Partial<CropAlert>): Observable<CropAlert> {
    return this.http.post<CropAlert>(`${this.priceUrl}/alerts`, alert).pipe(
      catchError(() => of(alert as CropAlert))
    );
  }

  deletePriceAlert(alertId: string): Observable<void> {
    return this.http.delete<void>(`${this.priceUrl}/alerts/${alertId}`).pipe(
      catchError(() => of(undefined as any))
    );
  }
}
