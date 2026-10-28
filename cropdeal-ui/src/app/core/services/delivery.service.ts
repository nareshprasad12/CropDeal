import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, catchError, map, of, tap } from 'rxjs';
import { Delivery } from '../models/delivery.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DeliveryService {
  private baseUrl = `${environment.apiUrl}/deliveries`;
  private readonly DELIVERIES_KEY = 'cropdeal_active_deliveries';

  private deliveriesSubject = new BehaviorSubject<Delivery[]>(this.loadStoredDeliveries());
  public deliveries$ = this.deliveriesSubject.asObservable();

  constructor(private http: HttpClient) {
    if (typeof window !== 'undefined') {
      window.addEventListener('storage', (e: StorageEvent) => {
        if (e.key === this.DELIVERIES_KEY) {
          this.refreshDeliveries();
        }
      });
    }
    this.refreshFromBackend();
  }

  refreshDeliveries(): Delivery[] {
    const list = this.loadStoredDeliveries();
    this.deliveriesSubject.next(list);
    return list;
  }

  refreshFromBackend(): void {
    this.http.get<any[]>(this.baseUrl).pipe(
      catchError(() => of([]))
    ).subscribe(serverItems => {
      if (serverItems && serverItems.length > 0) {
        const mapped = serverItems
          .filter(d => d.fulfillmentType !== 'SELF_PICKUP' && d.status !== 'SELF_PICKUP')
          .map(d => this.mapBackendDelivery(d));
        this.saveDeliveries(mapped);
      }
    });
  }

  getAllDeliveries(): Observable<Delivery[]> {
    return this.http.get<any[]>(this.baseUrl).pipe(
      map(res => {
        if (res && res.length > 0) {
          const mapped = res
            .filter(d => d.fulfillmentType !== 'SELF_PICKUP' && d.status !== 'SELF_PICKUP')
            .map(d => this.mapBackendDelivery(d));
          this.saveDeliveries(mapped);
          return mapped;
        }
        return this.deliveriesSubject.value.filter(d => d.fulfillmentType !== 'SELF_PICKUP' && d.status !== 'SELF_PICKUP');
      }),
      catchError(() => of(this.deliveriesSubject.value.filter(d => d.fulfillmentType !== 'SELF_PICKUP' && d.status !== 'SELF_PICKUP')))
    );
  }

  getDeliveryPool(): Observable<Delivery[]> {
    return this.http.get<any[]>(`${this.baseUrl}/pool`).pipe(
      map((res) => {
        if (res && res.length > 0) {
          const mapped = res
            .filter(d => d.fulfillmentType !== 'SELF_PICKUP' && d.status !== 'SELF_PICKUP')
            .map(d => this.mapBackendDelivery(d));
          return mapped;
        }
        return this.deliveriesSubject.value.filter(d =>
          d.fulfillmentType !== 'SELF_PICKUP' &&
          d.status !== 'SELF_PICKUP' &&
          (d.status === 'PENDING_ASSIGNMENT' || d.status === 'AVAILABLE_FOR_PICKUP')
        );
      }),
      catchError(() => {
        return of(this.deliveriesSubject.value.filter(d =>
          d.fulfillmentType !== 'SELF_PICKUP' &&
          d.status !== 'SELF_PICKUP' &&
          (d.status === 'PENDING_ASSIGNMENT' || d.status === 'AVAILABLE_FOR_PICKUP')
        ));
      })
    );
  }

  getDeliveriesByPartner(partnerId: string): Observable<Delivery[]> {
    const numericId = parseInt(String(partnerId || '').replace(/\D/g, ''), 10) || 3;
    return this.http.get<any[]>(`${this.baseUrl}/agent/${numericId}`).pipe(
      map(res => {
        if (res && res.length > 0) {
          return res.map(d => this.mapBackendDelivery(d));
        }
        return this.deliveriesSubject.value.filter(d =>
          d.fulfillmentType !== 'SELF_PICKUP' &&
          d.status !== 'SELF_PICKUP' &&
          (d.partnerId === partnerId || d.status === 'ASSIGNED' || d.status === 'IN_TRANSIT' || d.status === 'PICKED_UP' || d.status === 'DELIVERED')
        );
      }),
      catchError(() => {
        return of(this.deliveriesSubject.value.filter(d =>
          d.fulfillmentType !== 'SELF_PICKUP' &&
          d.status !== 'SELF_PICKUP' &&
          (d.partnerId === partnerId || d.status === 'ASSIGNED' || d.status === 'IN_TRANSIT' || d.status === 'PICKED_UP' || d.status === 'DELIVERED')
        ));
      })
    );
  }

  getDeliveryByOrder(orderId: string): Observable<Delivery | undefined> {
    const cleanId = String(orderId || '').trim();
    const numericId = parseInt(cleanId.replace(/\D/g, ''), 10);
    if (numericId) {
      return this.http.get<any>(`${this.baseUrl}/order/${numericId}`).pipe(
        map(d => d ? this.mapBackendDelivery(d) : this.findLocalDelivery(cleanId)),
        catchError(() => of(this.findLocalDelivery(cleanId)))
      );
    }
    return of(this.findLocalDelivery(cleanId));
  }

  private findLocalDelivery(cleanId: string): Delivery | undefined {
    return this.deliveriesSubject.value.find(d => {
      const dId = String(d.orderId || '').trim();
      return dId === cleanId ||
             ('ORD-' + dId) === cleanId ||
             dId === ('ORD-' + cleanId) ||
             dId.replace('ORD-', '') === cleanId.replace('ORD-', '');
    });
  }

  claimDelivery(deliveryId: string, partnerId: string, partnerName: string): Observable<Delivery> {
    const cleanId = parseInt(String(deliveryId || '').replace(/\D/g, ''), 10) || 1;
    const numericPartner = parseInt(String(partnerId || '').replace(/\D/g, ''), 10) || 3;

    return this.http.post<any>(`${this.baseUrl}/${cleanId}/claim?deliveryAgentId=${numericPartner}`, {}).pipe(
      map(res => {
        const mapped = this.mapBackendDelivery(res);
        this.updateLocalDelivery(mapped);
        return mapped;
      }),
      catchError(() => {
        const list = [...this.deliveriesSubject.value];
        const index = list.findIndex(d => d.id === deliveryId);
        if (index !== -1) {
          list[index] = {
            ...list[index],
            partnerId,
            partnerName,
            status: 'ASSIGNED',
            updatedAt: new Date().toISOString()
          };
          this.saveDeliveries(list);
          return of(list[index]);
        }
        return of(list[0] || ({} as Delivery));
      })
    );
  }

  updateDeliveryStatus(deliveryId: string, status: 'PENDING_ASSIGNMENT' | 'ASSIGNED' | 'PICKED_UP' | 'IN_TRANSIT' | 'DELIVERED'): Observable<Delivery> {
    const cleanId = parseInt(String(deliveryId || '').replace(/\D/g, ''), 10) || 1;
    const backendStatus = status === 'PENDING_ASSIGNMENT' ? 'AVAILABLE_FOR_PICKUP' : status;

    return this.http.put<any>(`${this.baseUrl}/${cleanId}/status`, { status: backendStatus, notes: 'Updated from portal' }).pipe(
      map(res => {
        const mapped = this.mapBackendDelivery(res);
        this.updateLocalDelivery(mapped);
        return mapped;
      }),
      catchError(() => {
        const list = [...this.deliveriesSubject.value];
        const index = list.findIndex(d => d.id === deliveryId);
        if (index !== -1) {
          list[index] = {
            ...list[index],
            status,
            updatedAt: new Date().toISOString()
          };
          this.saveDeliveries(list);
          return of(list[index]);
        }
        return of(list[0] || ({} as Delivery));
      })
    );
  }

  createDelivery(delivery: Partial<Delivery>): Observable<Delivery> {
    const estimatedKm = (delivery.distanceKm != null && Number(delivery.distanceKm) > 0)
      ? Number(delivery.distanceKm)
      : (delivery.deliveryFee != null && Number(delivery.deliveryFee) > 0
          ? Math.round(Number(delivery.deliveryFee) / 10)
          : this.estimateDistanceKm(delivery.pickupAddress, delivery.dropAddress));

    const chosenFee = (delivery.deliveryFee != null && Number(delivery.deliveryFee) > 0)
      ? Number(delivery.deliveryFee)
      : (estimatedKm * 10);

    const orderNum = parseInt(String(delivery.orderId || '').replace(/\D/g, ''), 10) || Math.floor(1000 + Math.random() * 9000);
    const agentNum = delivery.partnerId ? parseInt(String(delivery.partnerId).replace(/\D/g, ''), 10) : null;

    const newDelivery: Delivery = {
      id: 'DEL-' + orderNum,
      orderId: delivery.orderId || 'ORD-' + orderNum,
      dealerId: delivery.dealerId || null as any,
      farmerId: delivery.farmerId || null as any,
      partnerId: delivery.partnerId || null as any,
      partnerName: delivery.partnerName || null as any,
      cropName: delivery.cropName || 'Agricultural Produce',
      cropQuantity: delivery.cropQuantity != null ? delivery.cropQuantity : 50,
      cropUnit: delivery.cropUnit || 'Kg',
      farmerName: delivery.farmerName || 'Ramesh Kumar (Farmer)',
      farmerPhone: delivery.farmerPhone || '+91 98765 43210',
      pickupAddress: delivery.pickupAddress || 'Khanna Mandi Gate, Ludhiana, Punjab',
      dealerName: delivery.dealerName || 'Super Agros (Dealer)',
      dealerPhone: delivery.dealerPhone || '+91 98765 43211',
      dropAddress: delivery.dropAddress || 'Commercial Grain Terminal, Yard 2, New Delhi',
      distanceKm: estimatedKm,
      deliveryFee: chosenFee,
      fulfillmentType: delivery.fulfillmentType || 'DELIVERY_AGENT',
      status: delivery.fulfillmentType === 'SELF_PICKUP' ? 'DELIVERED' : (delivery.status || 'PENDING_ASSIGNMENT'),
      trackingNumber: 'TRK-IN-' + Math.floor(10000 + Math.random() * 90000),
      updatedAt: new Date().toISOString()
    };

    // Save locally
    const list = [newDelivery, ...this.deliveriesSubject.value];
    this.saveDeliveries(list);

    // Call backend
    if (delivery.fulfillmentType === 'SELF_PICKUP') {
      return this.http.post<any>(`${this.baseUrl}/self-pickup?orderId=${orderNum}&pickupAddress=${encodeURIComponent(newDelivery.pickupAddress || 'Farm Gate')}`, {}).pipe(
        map(res => {
          const mapped = this.mapBackendDelivery(res);
          this.updateLocalDelivery(mapped);
          return mapped;
        }),
        catchError(() => of(newDelivery))
      );
    } else {
      const payload = {
        orderId: orderNum,
        deliveryAgentId: agentNum,
        pickupAddress: newDelivery.pickupAddress || null,
        deliveryAddress: newDelivery.dropAddress || null,
        dealerId: delivery.dealerId ? parseInt(String(delivery.dealerId).replace(/\D/g, ''), 10) : null,
        dealerName: delivery.dealerName || null,
        dealerPhone: delivery.dealerPhone || null,
        farmerId: delivery.farmerId ? parseInt(String(delivery.farmerId).replace(/\D/g, ''), 10) : null,
        farmerName: delivery.farmerName || null,
        farmerPhone: delivery.farmerPhone || null,
        cropName: delivery.cropName || null,
        cropQuantity: delivery.cropQuantity != null ? delivery.cropQuantity : null,
        cropUnit: delivery.cropUnit || null,
        deliveryFee: chosenFee,
        distanceKm: estimatedKm
      };

      return this.http.post<any>(this.baseUrl, payload).pipe(
        map(res => {
          const mapped = this.mapBackendDelivery(res);
          // Preserve our calculated/chosen distanceKm and deliveryFee if backend returned null or default
          if (!mapped.distanceKm || mapped.distanceKm <= 0) {
            mapped.distanceKm = estimatedKm;
          }
          if (!mapped.deliveryFee || mapped.deliveryFee <= 0) {
            mapped.deliveryFee = chosenFee;
          }
          this.updateLocalDelivery(mapped);
          return mapped;
        }),
        catchError(() => of(newDelivery))
      );
    }
  }

  private updateLocalDelivery(del: Delivery): void {
    const list = [...this.deliveriesSubject.value];
    const idx = list.findIndex(d => String(d.id) === String(del.id) || String(d.orderId) === String(del.orderId));
    if (idx !== -1) {
      list[idx] = { ...list[idx], ...del };
    } else {
      list.unshift(del);
    }
    this.saveDeliveries(list);
  }

  private saveDeliveries(list: Delivery[]): void {
    const sanitized = list.filter(d => d.fulfillmentType !== 'SELF_PICKUP' && d.status !== 'SELF_PICKUP');
    localStorage.setItem(this.DELIVERIES_KEY, JSON.stringify(sanitized));
    this.deliveriesSubject.next(sanitized);
  }

  public estimateDistanceKm(pickup?: string | null, drop?: string | null): number {
    if (!pickup && !drop) return 35;
    const p = (pickup || '').toLowerCase();
    const d = (drop || '').toLowerCase();

    if ((p.includes('karnal') && d.includes('delhi')) || (p.includes('delhi') && d.includes('karnal'))) return 130;
    if ((p.includes('ludhiana') && d.includes('delhi')) || (p.includes('delhi') && d.includes('ludhiana'))) return 310;
    if ((p.includes('khanna') && d.includes('delhi')) || (p.includes('delhi') && d.includes('khanna'))) return 285;
    if ((p.includes('amritsar') && d.includes('delhi')) || (p.includes('delhi') && d.includes('amritsar'))) return 450;
    if ((p.includes('dindigul') && d.includes('delhi')) || (p.includes('tamil nadu') && d.includes('delhi'))) return 420;
    if ((p.includes('coimbatore') && d.includes('chennai')) || (p.includes('chennai') && d.includes('coimbatore'))) return 500;
    if ((p.includes('erode') && d.includes('coimbatore')) || (p.includes('coimbatore') && d.includes('erode'))) return 100;
    if ((p.includes('koyambedu') && d.includes('chennai')) || (p.includes('chennai') && d.includes('koyambedu'))) return 15;
    if ((p.includes('pune') && d.includes('mumbai')) || (p.includes('mumbai') && d.includes('pune'))) return 150;
    if ((p.includes('nashik') && d.includes('mumbai')) || (p.includes('mumbai') && d.includes('nashik'))) return 165;
    if ((p.includes('jaipur') && d.includes('delhi')) || (p.includes('delhi') && d.includes('jaipur'))) return 270;

    if (p.includes('haryana') && d.includes('haryana')) return 35;
    if (p.includes('punjab') && d.includes('punjab')) return 40;
    if (p.includes('tamil nadu') && d.includes('tamil nadu')) return 45;

    return 35;
  }

  public mapBackendDelivery(d: any): Delivery {
    const delId = d.deliveryId || d.id;
    let distanceKm = (d.distanceKm && Number(d.distanceKm) > 0)
      ? Number(d.distanceKm)
      : (d.distance && Number(d.distance) > 0 ? Number(d.distance) : 0);

    let fee = (d.deliveryFee && Number(d.deliveryFee) > 0) ? Number(d.deliveryFee) : 0;

    if (distanceKm > 0 && fee <= 0) {
      fee = distanceKm * 10;
    } else if (fee > 0 && distanceKm <= 0) {
      distanceKm = Math.round(fee / 10);
    } else if (distanceKm <= 0 && fee <= 0) {
      distanceKm = this.estimateDistanceKm(d.pickupAddress, d.deliveryAddress || d.dropAddress);
      fee = distanceKm * 10;
    }

    return {
      id: delId ? 'DEL-' + delId : 'DEL-101',
      orderId: d.orderId ? 'ORD-' + d.orderId : 'ORD-1001',
      partnerId: d.deliveryAgentId ? String(d.deliveryAgentId) : undefined,
      partnerName: d.deliveryAgentName || null,
      cropName: d.cropName != null ? d.cropName : 'Agricultural Produce',
      cropQuantity: d.cropQuantity != null ? Number(d.cropQuantity) : 50,
      cropUnit: d.cropUnit != null ? d.cropUnit : 'Kg',
      farmerId: d.farmerId ? String(d.farmerId) : '1',
      farmerName: d.farmerName != null ? d.farmerName : 'Ramesh Kumar (Farmer)',
      farmerPhone: d.farmerPhone != null ? d.farmerPhone : '+91 98765 43210',
      dealerId: d.dealerId ? String(d.dealerId) : '2',
      dealerName: d.dealerName != null ? d.dealerName : 'Super Agros (Dealer)',
      dealerPhone: d.dealerPhone != null ? d.dealerPhone : '+91 98765 43211',
      pickupAddress: d.pickupAddress != null ? d.pickupAddress : 'Khanna Mandi Gate, Ludhiana, Punjab',
      dropAddress: d.deliveryAddress || d.dropAddress || 'Commercial Grain Terminal, Yard 2, New Delhi',
      distanceKm: distanceKm,
      deliveryFee: fee,
      status: d.status === 'AVAILABLE_FOR_PICKUP' ? 'PENDING_ASSIGNMENT' : (d.status || 'PENDING_ASSIGNMENT'),
      fulfillmentType: d.fulfillmentType || 'DELIVERY_AGENT',
      trackingNumber: 'TRK-' + (delId || Math.floor(1000 + Math.random() * 9000)),
      updatedAt: d.updatedAt || d.createdAt || new Date().toISOString()
    };
  }

  private loadStoredDeliveries(): Delivery[] {
    const raw = localStorage.getItem(this.DELIVERIES_KEY);
    if (raw) {
      try {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed)) {
          return parsed
            .filter(d => d.fulfillmentType !== 'SELF_PICKUP' && d.status !== 'SELF_PICKUP')
            .map(d => {
              let km = (d.distanceKm && Number(d.distanceKm) > 0) ? Number(d.distanceKm) : 0;
              let fee = (d.deliveryFee && Number(d.deliveryFee) > 0) ? Number(d.deliveryFee) : 0;

              if (km > 0 && fee <= 0) {
                fee = km * 10;
              } else if (fee > 0 && km <= 0) {
                km = Math.round(fee / 10);
              } else if (km <= 0 && fee <= 0) {
                km = this.estimateDistanceKm(d.pickupAddress, d.dropAddress);
                fee = km * 10;
              }

              d.distanceKm = km;
              d.deliveryFee = fee;
              return d;
            });
        }
      } catch {}
    }

    return [];
  }
}
