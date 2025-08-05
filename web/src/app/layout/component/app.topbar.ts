import {Component, Input} from '@angular/core';
import {MenuItem} from 'primeng/api';
import {Router, RouterModule} from '@angular/router';
import {CommonModule} from '@angular/common';
import {StyleClassModule} from 'primeng/styleclass';
import {MenuModule} from 'primeng/menu';
import {ConfirmDialogModule} from 'primeng/confirmdialog';
import {LayoutService} from '../service/layout.service';
import {AuthService} from '../../core/services/auth.service';
import {LoadingService} from '../../shared/services/loading.service';
import {ConfirmDialogService} from '../../shared/services/confirm-dialog.service';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [RouterModule, CommonModule, StyleClassModule, MenuModule, ConfirmDialogModule],
  template: `
    <div class="layout-topbar">
      <div class="layout-topbar-logo-container">
        @if (!minimal) {
          <button class="layout-menu-button layout-topbar-action" (click)="layoutService.onMenuToggle()">
            <i class="pi pi-bars"></i>
          </button>
        }
        <a class="layout-topbar-logo" routerLink="/">
          <span>LOGO</span>
        </a>
      </div>
      <div class="layout-topbar-actions">
        <button type="button" class="layout-topbar-action" (click)="toggleDarkMode()">
          <i class="pi" [ngClass]="themeIcon"></i>
        </button>
        @if (!minimal) {
          <ng-container>
            @for (item of items; track item) {
              <button class="layout-topbar-action" [routerLink]="item.routerLink">
                <i class="pi" [ngClass]="item.icon"></i>
              </button>
            }
            <button type="button" class="layout-topbar-action" (click)="profileMenu.toggle($event)">
              <i class="pi pi-user"></i>
            </button>
            <p-menu #profileMenu [popup]="true" [model]="profileItems"></p-menu>
          </ng-container>
        }
      </div>
    </div>
  `
})
export class AppTopbar {
  @Input() minimal = false;
  items: MenuItem[] = [];

  profileItems: MenuItem[] = [
    { label: 'Perfil', icon: 'pi pi-user', routerLink: '/profile' },
    { separator: true },
    { label: 'Sair', icon: 'pi pi-sign-out', command: () => this.confirmLogout() }
  ];

  constructor(
    public layoutService: LayoutService,
    private auth: AuthService,
    private confirmDialogService: ConfirmDialogService,
    private loadingService: LoadingService,
    private router: Router
  ) {}

  get themeIcon(): string {
    return this.layoutService.layoutConfig().darkTheme ? 'pi-moon' : 'pi-sun';
  }

  toggleDarkMode() {
    this.layoutService.toggleTheme();
  }

  async confirmLogout() {
    const confirmed = await this.confirmDialogService.confirmLogout();
    if (confirmed) {
      this.smoothLogout();
    }
  }

  smoothLogout() {
    this.loadingService.show();
    setTimeout(() => {
      this.auth.logout();
      this.loadingService.hide();
      this.router.navigate(['/login']);
    }, 500);
  }
}
