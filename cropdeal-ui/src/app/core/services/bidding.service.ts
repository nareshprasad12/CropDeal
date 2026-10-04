import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, map, of, tap } from 'rxjs';
import { BidOffer, BiddingAuction } from '../models/bidding.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class BiddingService {
  private baseUrl = `${environment.apiUrl}/biddings`;
  private readonly STORAGE_KEY = 'cropdeal_bidding_auctions';

  constructor(private http: HttpClient) {}

  private loadStoredAuctions(): BiddingAuction[] {
    const raw = localStorage.getItem(this.STORAGE_KEY);
    if (raw) {
      try {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed)) return parsed;
      } catch (e) {}
    }
    return [];
  }

  private saveStoredAuctions(auctions: BiddingAuction[]): void {
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(auctions));
  }

  getActiveAuctions(): Observable<BiddingAuction[]> {
    return this.http.get<BiddingAuction[]>(this.baseUrl).pipe(
      catchError(() => of(this.loadStoredAuctions())),
      map(data => {
        if (data && data.length > 0) {
          // Merge local updates
          const local = this.loadStoredAuctions();
          const mapById = new Map<string, BiddingAuction>();
          local.forEach(a => mapById.set(a.id, a));
          data.forEach(a => { if (!mapById.has(a.id)) mapById.set(a.id, a); });
          return Array.from(mapById.values());
        }
        return this.loadStoredAuctions();
      })
    );
  }

  getAuctionById(id: string): Observable<BiddingAuction> {
    const local = this.loadStoredAuctions().find(a => a.id === id);
    if (local) return of(local);
    return this.http.get<BiddingAuction>(`${this.baseUrl}/${id}`).pipe(
      catchError(() => of({} as BiddingAuction))
    );
  }

  createAuction(auction: Partial<BiddingAuction>): Observable<BiddingAuction> {
    const list = this.loadStoredAuctions();
    const newAuction: BiddingAuction = {
      id: 'AUCT-' + Math.floor(100 + Math.random() * 900),
      cropId: auction.cropId || 'crop-' + Date.now(),
      cropName: auction.cropName || 'Fresh Harvest Crop Lot',
      farmerId: auction.farmerId || 'farmer-1',
      farmerName: auction.farmerName || 'Registered Producer',
      startingPrice: auction.startingPrice || 1000,
      currentHighestBid: auction.startingPrice || 1000,
      highestBidderId: undefined,
      highestBidderName: undefined,
      quantity: auction.quantity || 100,
      unit: auction.unit || 'Kg',
      endTime: auction.endTime || new Date(Date.now() + (auction.durationHours || 12) * 3600000).toISOString(),
      status: 'OPEN',
      bidsCount: 0,
      minIncrement: auction.minIncrement || 50,
      createdAt: new Date().toISOString()
    };

    list.unshift(newAuction);
    this.saveStoredAuctions(list);

    // Call backend
    this.http.post<BiddingAuction>(this.baseUrl, newAuction).subscribe({
      next: () => {},
      error: () => {}
    });

    return of(newAuction);
  }

  placeBid(bid: BidOffer): Observable<BiddingAuction> {
    const list = this.loadStoredAuctions();
    const index = list.findIndex(a => a.id === bid.biddingId);
    if (index !== -1) {
      list[index].currentHighestBid = bid.bidAmount;
      list[index].highestBidderId = bid.dealerId;
      list[index].highestBidderName = bid.dealerName;
      list[index].bidsCount = (list[index].bidsCount || 0) + 1;
      this.saveStoredAuctions(list);

      this.http.post<BiddingAuction>(`${this.baseUrl}/${bid.biddingId}/bid`, bid).subscribe({
        next: () => {},
        error: () => {}
      });

      return of(list[index]);
    }
    return of({} as BiddingAuction);
  }

  closeAuction(auctionId: string, orderId?: string, awardedAmount?: number): Observable<BiddingAuction> {
    const list = this.loadStoredAuctions();
    const index = list.findIndex(a => a.id === auctionId);
    if (index !== -1) {
      list[index].status = 'CLOSED';
      if (orderId) list[index].awardedOrderId = orderId;
      if (awardedAmount) list[index].awardedAmount = awardedAmount;
      this.saveStoredAuctions(list);

      this.http.put<BiddingAuction>(`${this.baseUrl}/${auctionId}/close`, {}).subscribe({
        next: () => {},
        error: () => {}
      });

      return of(list[index]);
    }
    return of({} as BiddingAuction);
  }
}

