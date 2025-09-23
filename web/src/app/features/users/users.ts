import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { UserList } from './components/user-list/user-list';
import { Breadcrumb } from '../../shared/components/breadcrumb/breadcrumb';

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [RouterModule, UserList, Breadcrumb],
  template: `
    <div class="layout-main">
      <app-breadcrumb [items]="breadcrumbItems"></app-breadcrumb>
      <app-user-list></app-user-list>
    </div>
  `
})
export class Users {
  breadcrumbItems = [
    { label: 'Dashboard', url: '/' },
    { label: 'Usuários' }
  ];
}
