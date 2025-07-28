import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import {LoginFormComponent} from '../../features/login/login-form.component';
import {AuthService} from '../../core/services/auth.service';
import {AppTopbar} from '../../layout/component/app.topbar';
import { LoadingService } from '../../shared/services/loading.service';
import { AsyncPipe } from '@angular/common';
import { LoadingSpinnerComponent } from '../../shared/components/loading/loading-spinner.component';
import { MessageService } from 'primeng/api';
import {Toast} from 'primeng/toast';

@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [CommonModule, LoginFormComponent, AppTopbar, AsyncPipe, LoadingSpinnerComponent, Toast],
  providers: [MessageService],
  template: `
    <app-topbar [minimal]="true" />
    <p-toast position="bottom-right" />
    <app-loading-spinner [show]="(loadingService.loading$ | async) ?? false" />
    <div class="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 class="text-2xl mb-6">Login</h1>
      <app-login-form [loading]="(loadingService.loading$ | async) ?? false" (login)="handleLogin($event)"></app-login-form>
    </div>
  `
})
export class LoginPage implements OnInit {
  constructor(
    private auth: AuthService,
    private router: Router,
    public loadingService: LoadingService,
    private messageService: MessageService
  ) {}

  ngOnInit() {
    const toast = history.state.toast;
    console.log('LoginPage ngOnInit, toast:', toast);
    if (toast) {
      setTimeout(() => this.messageService.add(toast), 0);
      history.replaceState({}, document.title);
    }
  }

  handleLogin({ username, password }: { username: string; password: string }) {
    this.loadingService.show();
    this.auth.login(username, password).subscribe({
      next: (res) => {
        this.auth.saveTokens(res.access, res.refresh);
        this.loadingService.hide();
        this.router.navigate(['/']);
      },
      error: () => {
        this.loadingService.hide();
        alert('Usuário ou senha inválidos');
      }
    });
  }
}
