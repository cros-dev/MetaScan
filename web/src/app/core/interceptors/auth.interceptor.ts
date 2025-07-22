import { Injectable } from '@angular/core';
import {
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError, from } from 'rxjs';
import { catchError, switchMap } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const accessToken = localStorage.getItem('token');
    let authReq = req;
    if (accessToken) {
      authReq = req.clone({
        setHeaders: { Authorization: `Bearer ${accessToken}` }
      });
    }
    return next.handle(authReq).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 401) {
          const refreshToken = localStorage.getItem('refresh');
          if (refreshToken) {
            return from(
              fetch(`${environment.apiUrl}token/refresh/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh: refreshToken })
              }).then(res => res.json())
            ).pipe(
              switchMap((data: any) => {
                if (data.access) {
                  localStorage.setItem('token', data.access);
                  const retryReq = req.clone({
                    setHeaders: { Authorization: `Bearer ${data.access}` }
                  });
                  return next.handle(retryReq);
                } else {
                  localStorage.removeItem('token');
                  localStorage.removeItem('refresh');
                  window.location.href = '/login';
                  return throwError(() => error);
                }
              })
            );
          } else {
            localStorage.removeItem('token');
            window.location.href = '/login';
          }
        }
        return throwError(() => error);
      })
    );
  }
}
