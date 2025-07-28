import { Injectable, Injector } from '@angular/core';
import { HttpErrorResponse, HttpEvent, HttpHandlerFn, HttpRequest } from '@angular/common/http';
import { EMPTY, Observable, throwError } from 'rxjs';
import { catchError, switchMap } from 'rxjs/operators';
import { AuthService } from '../services/auth.service';
import { ConfirmDialogService } from '../../shared/services/confirm-dialog.service';

@Injectable()
export class AuthInterceptor {
  constructor(private injector: Injector) {}

  private get authService(): AuthService {
    return this.injector.get(AuthService);
  }

  private get confirmDialogService(): ConfirmDialogService {
    return this.injector.get(ConfirmDialogService);
  }

  private handleSessionExpired(): Observable<never> {
    this.confirmDialogService.confirmSessionExpired().then((confirmed) => {
      if (confirmed) {
        this.authService.logout();
      }
    });
    return EMPTY;
  }

  intercept(req: HttpRequest<any>, next: HttpHandlerFn): Observable<HttpEvent<any>> {
    const accessToken = this.authService.accessToken;
    const isRefreshRequest = req.url.includes('token/refresh');

    let authReq = req;
    if (accessToken && !isRefreshRequest) {
      authReq = req.clone({
        setHeaders: { Authorization: `Bearer ${accessToken}` }
      });
    }

    return next(authReq).pipe(
      catchError((error: HttpErrorResponse) => {
        if (isRefreshRequest) {
          return this.handleSessionExpired();
        }

        if (error.status === 401) {
          const refreshToken = this.authService.refreshToken;
          if (!refreshToken) {
            return this.handleSessionExpired();
          }

          return this.authService.refreshAccessToken().pipe(
            switchMap((data: any) => {
              if (data && data.access) {
                this.authService.saveTokens(data.access, refreshToken);
                const retryReq = req.clone({
                  setHeaders: { Authorization: `Bearer ${data.access}` }
                });
                return next(retryReq);
              }
              return this.handleSessionExpired();
            }),
            catchError((refreshError: HttpErrorResponse) => {
              if (refreshError.status === 401) {
                return this.handleSessionExpired();
              }
              return throwError(() => refreshError);
            })
          );
        }

        return throwError(() => error);
      })
    );
  }
}
