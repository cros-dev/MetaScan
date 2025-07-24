import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login-form',
  standalone: true,
  imports: [CommonModule, FormsModule, InputTextModule, ButtonModule],
  template: `
    <form (ngSubmit)="submit()" class="flex flex-col gap-4">
      <input pInputText [(ngModel)]="username" name="username" placeholder="Usuário" required />
      <input pInputText [(ngModel)]="password" name="password" type="password" placeholder="Senha" required />
      <button pButton type="submit" label="Entrar" [disabled]="loading"></button>
    </form>
  `
})
export class LoginFormComponent {
  @Input() loading = false;
  @Output() login = new EventEmitter<{ username: string; password: string }>();

  username = '';
  password = '';

  submit() {
    this.login.emit({ username: this.username, password: this.password });
  }
}
