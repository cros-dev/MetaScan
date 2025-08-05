import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Observable, of } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  constructor(private router: Router, private http: HttpClient) {}

  login(email: string, password: string): Observable<any> {
    return this.http.post<any>(`${environment.apiUrl}login/`, { email, password });
  }

  saveTokens(access: string, refresh: string, userInfo?: { role?: string; user_id?: number; email?: string }): void {
    if (access && refresh) {
      localStorage.setItem('token', access);
      localStorage.setItem('refresh', refresh);

      if (userInfo) {
        if (userInfo.role) localStorage.setItem('userRole', userInfo.role);
        if (userInfo.user_id !== undefined) localStorage.setItem('userId', String(userInfo.user_id));
        if (userInfo.email) localStorage.setItem('userEmail', userInfo.email);
      }
    }
  }

  get accessToken(): string | null {
    return localStorage.getItem('token');
  }

  get refreshToken(): string | null {
    return localStorage.getItem('refresh');
  }

  refreshAccessToken(): Observable<any> {
    const refresh = this.refreshToken;
    if (!refresh) return of(null);
    return this.http.post<any>(`${environment.apiUrl}token/refresh/`, { refresh });
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh');
    localStorage.removeItem('userRole');
    localStorage.removeItem('userId');
    localStorage.removeItem('userEmail');
    this.router.navigate(['/login']).then(() => {
      console.log('Usuário redirecionado para /login');
    });
  }

  getUserRole(): string {
    const localRole = localStorage.getItem('userRole');
    if (localRole) {
      return localRole;
    }

    const payload = this.decodeTokenPayload();
    if (payload?.role) {
      console.log('Token payload:', payload);
      return payload.role;
    }

    return '';
  }

  getUserId(): number | null {
    const localId = localStorage.getItem('userId');
    if (localId) {
      return Number(localId);
    }

    const payload = this.decodeTokenPayload();
    if (payload?.user_id !== undefined) {
      console.log('Token payload:', payload);
      return payload.user_id;
    }

    return null;
  }

  private decodeTokenPayload(): any | null {
    const token = this.accessToken;
    if (!token) return null;

    try {
      const payloadBase64 = token.split('.')[1];
      const payloadJson = atob(payloadBase64);
      return JSON.parse(payloadJson);
    } catch (error) {
      console.error(error);
      return null;
    }
  }
}
