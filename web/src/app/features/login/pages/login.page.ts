import { Component } from '@angular/core';
import { Login } from '../components/login/login';

@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [Login],
  template: `<app-login></app-login>`
})
export class LoginPage {}
