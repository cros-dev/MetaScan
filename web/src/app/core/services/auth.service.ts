import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Observable, of, firstValueFrom } from 'rxjs';
import { LoadingService } from '../../shared/services/loading.service';
import { NotificationService } from '../../shared/services/notification.service';

@Injectable({ providedIn: 'root' })
export class AuthService {
  constructor(
    private router: Router,
    private http: HttpClient,
    private loadingService: LoadingService,
    private notificationService: NotificationService
  ) {}

  login(email: string, password: string): Observable<any> {
    return this.http.post<any>(`${environment.apiUrl}login/`, { email, password });
  }

  async loginWithFeedback(email: string, password: string): Promise<void> {
    this.loadingService.show();

    try {
      const response = await firstValueFrom(this.login(email, password));

      this.saveTokens(response.access, response.refresh, {
        role: response.role,
        user_id: response.user_id,
        email: response.email
      });

      this.notificationService.showSuccess('Login realizado com sucesso!');

      setTimeout(() => {
        this.router.navigate(['/']);
      }, 1000);

    } catch (error: any) {
      this.handleLoginError(error);
    } finally {
      this.loadingService.hide();
    }
  }

  private handleLoginError(error: any): void {
    console.error('Login error:', error);

    if (error.status === 401) {
      this.notificationService.showError('Email ou senha incorretos');
    } else if (error.status === 0) {
      this.notificationService.showError('Erro de conexão. Verifique sua internet');
    } else if (error.status >= 500) {
      this.notificationService.showError('Erro interno do servidor. Tente novamente');
    } else {
      this.notificationService.showError('Erro inesperado. Tente novamente');
    }
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
