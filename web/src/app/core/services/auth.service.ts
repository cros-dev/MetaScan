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

  saveTokens(access: string, refresh: string): void {
    if (access && refresh) {
      localStorage.setItem('token', access);
      localStorage.setItem('refresh', refresh);
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
    this.router.navigate(['/login']).then(() => {
      console.log('Usuário redirecionado para /login');
    });
  }

  isAuthenticated(): boolean {
    return !!this.accessToken;
  }
}
