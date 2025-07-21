import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <ul class="layout-menu">
      @for (item of model; track item) {
        <li class="layout-root-menuitem">
          <span class="layout-menuitem-root-text">{{ item.label }}</span>
          <ul>
            @for (sub of item.items; track sub) {
              <li>
                <a [routerLink]="sub.routerLink" routerLinkActive="active-route" [routerLinkActiveOptions]="{ exact: true }" class="menu-link">
                  <i class="pi" [ngClass]="sub.icon"></i>
                  <span>{{ sub.label }}</span>
                </a>
              </li>
            }
          </ul>
        </li>
      }
    </ul>
  `
})
export class AppMenu implements OnInit {
  model: MenuItem[] = [];

  ngOnInit() {
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
          { label: 'Cavaletes', icon: 'pi-sitemap', routerLink: ['/cavaletes'] },
        ]
      }
    ];
  }
}
