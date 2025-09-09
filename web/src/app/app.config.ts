import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection, inject } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { providePrimeNG } from 'primeng/config';
import Aura from '@primeuix/themes/aura';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { ConfirmationService } from 'primeng/api';
import { AuthInterceptor } from './core/interceptors/auth.interceptor';
import { NotificationService } from './shared/services/notification.service';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideAnimationsAsync(),
    providePrimeNG({
      theme: {
        preset: Aura,
        options: { darkModeSelector: '.app-dark' }
      }
    }),
    provideHttpClient(
      withInterceptors([
        (req, next) => inject(AuthInterceptor).intercept(req, next)
      ])
    ),
    ConfirmationService,
    AuthInterceptor,
    NotificationService
  ]
};
