import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MenuItem } from 'primeng/api';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './menu.html'
})
export class Menu implements OnInit {
  model: MenuItem[] = [];

  constructor(private authService: AuthService) {}

  ngOnInit() {
    const userRole = this.authService.getUserRole();

    this.model = [
      {
        label: 'Home',
        items: [
          { label: 'Dashboard', icon: 'pi pi-fw pi-home', routerLink: ['/'] }
        ]
      },
      {
        label: 'Gestão',
        items: [
          { label: 'Cavaletes', icon: 'pi pi-fw pi-sitemap', routerLink: ['/cavaletes'] },
          { label: 'Produtos', icon: 'pi pi-fw pi-box', routerLink: ['/products'] },
          ...(userRole === 'admin' ? [{ label: 'Usuários', icon: 'pi pi-fw pi-users', routerLink: ['/users'] }] : [])
        ]
      }
    ];
  }
}
