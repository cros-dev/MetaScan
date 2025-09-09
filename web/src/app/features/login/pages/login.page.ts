import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginFormComponent } from '../login-form.component';
import { LoadingService } from '../../../shared/services/loading.service';
import { AuthService } from '../../../core/services/auth.service';
import { AsyncPipe } from '@angular/common';
import { LoadingSpinnerComponent } from '../../../shared/components/loading/loading-spinner.component';
import { NotificationContainerComponent } from '../../../shared/components/notification/notification-container.component';
import {Topbar} from '../../../layout/components/topbar/topbar';

@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [CommonModule, LoginFormComponent, AsyncPipe, LoadingSpinnerComponent, NotificationContainerComponent, Topbar],
  template: `
    <app-topbar [minimal]="true" />
    <app-loading-spinner [show]="(loadingService.loading$ | async) ?? false" />
    <div class="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 class="text-2xl mb-6">Login</h1>
      <app-login-form [loading]="(loadingService.loading$ | async) ?? false" (login)="handleLogin($event)"></app-login-form>
    </div>
    <app-notification-container></app-notification-container>
  `
})
export class LoginPage implements OnInit {
  constructor(
    private authService: AuthService,
    public loadingService: LoadingService,
  ) {}

  ngOnInit() {
  }

  async handleLogin({ email, password }: { email: string; password: string }) {
    await this.authService.loginWithFeedback(email, password);
  }
}
