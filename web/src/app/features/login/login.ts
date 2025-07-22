import {Component} from '@angular/core';
import {Router} from '@angular/router';
import {FormsModule} from '@angular/forms';
import {AuthService} from '../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  template: `
    <div class="flex flex-col items-center justify-center min-h-screen">
      <div class="bg-white p-8 rounded shadow-md w-full max-w-sm">
        <h2 class="text-2xl font-bold mb-6 text-center">Login</h2>
        <form (ngSubmit)="login()" #loginForm="ngForm">
          <div class="mb-4">
            <label class="block mb-1 font-medium">E-mail</label>
            <input type="email" class="w-full border rounded px-3 py-2" [(ngModel)]="email" name="email" required />
          </div>
          <div class="mb-6">
            <label class="block mb-1 font-medium">Senha</label>
            <input type="password" class="w-full border rounded px-3 py-2" [(ngModel)]="password" name="password" required />
          </div>
          <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition">Entrar</button>
        </form>
        @if (error) {
          <div class="text-red-600 mt-4 text-center">{{ error }}</div>
        }
      </div>
    </div>
  `,
  styles: []
})
export class Login {
  email = '';
  password = '';
  error = '';

  constructor(private router: Router, private auth: AuthService) {}

  async login() {
    try {
      const data = await this.auth.login(this.email, this.password);
      if (data.access && data.refresh) {
        this.auth.saveTokens(data.access, data.refresh);
        this.router.navigate(['/']).then(() => {});
      } else {
        this.error = 'E-mail ou senha inválidos';
      }
    } catch {
      this.error = 'Erro ao conectar com o servidor';
    }
  }
}
