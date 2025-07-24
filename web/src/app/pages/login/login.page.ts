import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import {LoginFormComponent} from '../../features/login/login-form.component';
import {AuthService} from '../../core/services/auth.service';

@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [CommonModule, LoginFormComponent],
  template: `
    <div class="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 class="text-2xl mb-6">Login</h1>
      <app-login-form [loading]="loading" (login)="handleLogin($event)"></app-login-form>
    </div>
  `
})
export class LoginPage {
  loading = false;

  constructor(private auth: AuthService, private router: Router) {}

  handleLogin({ username, password }: { username: string; password: string }) {
    this.loading = true;
    this.auth.login(username, password).subscribe({
      next: (res) => {
        this.auth.saveTokens(res.access, res.refresh);
        this.loading = false;
        this.router.navigate(['/']);
      },
      error: () => {
        this.loading = false;
        alert('Usuário ou senha inválidos');
      }
    });
  }
}
