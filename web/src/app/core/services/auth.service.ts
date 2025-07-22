import {Injectable} from '@angular/core';
import {environment} from '../../../environments/environment';
import {Router} from '@angular/router';

@Injectable({ providedIn: 'root' })
export class AuthService {
  constructor(private router: Router) {}

  async login(email: string, password: string): Promise<any> {
    const res = await fetch(`${environment.apiUrl}login/`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email, password})
    });
    return await res.json();
  }

  saveTokens(access: string, refresh: string) {
    localStorage.setItem('token', access);
    localStorage.setItem('refresh', refresh);
  }

  async refreshToken(): Promise<any> {
    const refresh = localStorage.getItem('refresh');
    if (!refresh) return Promise.reject('No refresh token');
    return fetch(`${environment.apiUrl}token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh })
    }).then(res => res.json());
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh');
    this.router.navigate(['/login']).then(() => {});
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }
}
