import { Component, OnInit } from '@angular/core';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { UserFormComponent } from '../components/user-form/user-form';
import { Breadcrumb } from '../../../shared/components/breadcrumb/breadcrumb';

@Component({
  selector: 'app-user-form-page',
  standalone: true,
  imports: [RouterModule, UserFormComponent, Breadcrumb],
  template: `
    <div class="layout-main">
      <app-breadcrumb [items]="breadcrumbItems"></app-breadcrumb>
      <app-user-form [isEditing]="isEditing" [userId]="userId"></app-user-form>
    </div>
  `
})
export class UserFormPage implements OnInit {
  isEditing = false;
  userId?: number;

  breadcrumbItems = [
    { label: 'Dashboard', url: '/' },
    { label: 'Usuários', url: '/users' },
    { label: 'Criar Usuário' }
  ];

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.userId = this.route.snapshot.params['id'];
    this.isEditing = !!this.userId;

    if (this.isEditing) {
      this.breadcrumbItems = [
        { label: 'Dashboard', url: '/' },
        { label: 'Usuários', url: '/users' },
        { label: 'Editar Usuário' }
      ];
    }
  }
}
