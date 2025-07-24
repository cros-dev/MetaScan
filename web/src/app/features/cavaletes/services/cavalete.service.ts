import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Cavalete } from '../models/cavalete.model';
import { environment } from '../../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class CavaleteService {
  private apiUrl = environment.apiUrl + 'cavaletes/';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Cavalete[]> {
    return this.http.get<any>(this.apiUrl).pipe(
      map(data => Array.isArray(data) ? data : data.results)
    );
  }

  getByCode(code: string): Observable<Cavalete | undefined> {
    const params = new HttpParams().set('code', code);
    return this.http.get<any>(this.apiUrl, { params }).pipe(
      map(data => data.results && data.results.length > 0 ? data.results[0] : undefined)
    );
  }
}
