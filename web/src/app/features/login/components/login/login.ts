import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginForm } from '../login-form/login-form';
import { LoadingService } from '../../../../shared/services/loading.service';
import { AuthService } from '../../../../core/services/auth.service';
import { AsyncPipe } from '@angular/common';
import { LoadingSpinner } from '../../../../shared/components/loading/loading-spinner';
import { NotificationContainer } from '../../../../shared/components/notification/notification-container';
import { Topbar } from '../../../../layout/components/topbar/topbar';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, LoginForm, AsyncPipe, LoadingSpinner, NotificationContainer, Topbar],
  templateUrl: './login.html',
  styleUrl: './login.scss'
})
export class Login implements OnInit {
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
