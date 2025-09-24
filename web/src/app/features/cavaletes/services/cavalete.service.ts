import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Cavalete, CreateCavaleteRequest, AssignUserRequest, AssignMassRequest, CavaleteFilters } from '../models/cavalete.model';
import {environment} from '../../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CavaleteService {
  private apiUrl = `${environment.apiUrl}cavaletes/`;

  constructor(private http: HttpClient) {}

  getCavaletes(filters?: CavaleteFilters): Observable<{ results: Cavalete[]; count: number }> {
    const params = this.buildParams(filters);
    return this.http.get<{ results: Cavalete[]; count: number }>(this.apiUrl, { params });
  }

  getCavalete(id: number): Observable<Cavalete> {
    return this.http.get<Cavalete>(`${this.apiUrl}${id}/`);
  }

  createCavalete(data: CreateCavaleteRequest): Observable<Cavalete> {
    return this.http.post<Cavalete>(this.apiUrl, data);
  }

  assignUser(id: number, data: AssignUserRequest): Observable<{ detail: string }> {
    return this.http.post<{ detail: string }>(`${this.apiUrl}${id}/assign_user/`, data);
  }

  assignMass(data: AssignMassRequest): Observable<{ detail: string; cavalete_ids: number[]; user: number | null }> {
    return this.http.post<{ detail: string; cavalete_ids: number[]; user: number | null }>(`${this.apiUrl}assign/`, data);
  }

  exportToExcel(cavaleteIds?: number[], cavaleteNames?: string[]): Observable<Blob> {
    const params = this.buildExportParams(cavaleteIds, cavaleteNames);
    return this.http.get(`${this.apiUrl}export/`, { params, responseType: 'blob' });
  }

  getProductStats(): Observable<{
    slots_with_products: number;
    unique_products: number;
  }> {
    return this.http.get<{
      slots_with_products: number;
      unique_products: number;
    }>(`${this.apiUrl}product_stats/`);
  }

  updateSlot(slotId: number, slotData: any): Observable<any> {
    const slotsUrl = `${environment.apiUrl}slots/`;
    return this.http.patch<any>(`${slotsUrl}${slotId}/`, slotData);
  }

  startSlotConfirmation(slotId: number): Observable<any> {
    const slotsUrl = `${environment.apiUrl}slots/`;
    return this.http.post<any>(`${slotsUrl}${slotId}/start_confirmation/`, {});
  }

  private buildParams(filters?: CavaleteFilters): HttpParams {
    let params = new HttpParams();

    if (filters?.status) {
      params = params.set('status', filters.status);
    }
    if (filters?.search) {
      params = params.set('search', filters.search);
    }
    if (filters?.ordering) {
      params = params.set('ordering', filters.ordering);
    }

    return params;
  }

  private buildExportParams(cavaleteIds?: number[], cavaleteNames?: string[]): HttpParams {
    let params = new HttpParams();

    if (cavaleteIds && cavaleteIds.length > 0) {
      cavaleteIds.forEach(id => {
        params = params.append('cavalete_id', id.toString());
      });
    }
    if (cavaleteNames && cavaleteNames.length > 0) {
      cavaleteNames.forEach(name => {
        params = params.append('cavalete_name', name);
      });
    }

    return params;
  }
}
