import { Component } from '@angular/core';
import { MenuItem } from 'primeng/api';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { StyleClassModule } from 'primeng/styleclass';
import { LayoutService } from '../service/layout.service';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [RouterModule, CommonModule, StyleClassModule],
  template: `
    <div class="layout-topbar">
      <div class="layout-topbar-logo-container">
        <button class="layout-menu-button layout-topbar-action" (click)="layoutService.onMenuToggle()">
          <i class="pi pi-bars"></i>
        </button>
        <a class="layout-topbar-logo" routerLink="/">
          <span>LOGO</span>
        </a>
      </div>
      <div class="layout-topbar-actions">
        <button type="button" class="layout-topbar-action" (click)="toggleDarkMode()">
          <i class="pi" [ngClass]="themeIcon"></i>
        </button>
        @for (item of items; track item) {
          <button class="layout-topbar-action" [routerLink]="item.routerLink">
            <i class="pi" [ngClass]="item.icon"></i>
          </button>
        }
      </div>
    </div>
  `
})
export class AppTopbar {
  items: MenuItem[] = [
    { label: 'Calendar', icon: 'pi-calendar', routerLink: '/calendar' },
    { label: 'Messages', icon: 'pi-inbox', routerLink: '/messages' },
    { label: 'Profile', icon: 'pi-user', routerLink: '/profile' }
  ];

  constructor(public layoutService: LayoutService) {}

  get themeIcon(): string {
    return this.layoutService.layoutConfig().darkTheme ? 'pi-moon' : 'pi-sun';
  }

  toggleDarkMode() {
    this.layoutService.toggleTheme();
  }
} 