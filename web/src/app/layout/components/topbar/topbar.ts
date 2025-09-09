import {Component, Input} from '@angular/core';
import {MenuItem} from 'primeng/api';
import {Router, RouterModule} from '@angular/router';
import {CommonModule} from '@angular/common';
import {StyleClassModule} from 'primeng/styleclass';
import {MenuModule} from 'primeng/menu';
import {ConfirmDialogModule} from 'primeng/confirmdialog';
import {LayoutService} from '../../services/layout.service';
import {AuthService} from '../../../core/services/auth.service';
import {LoadingService} from '../../../shared/services/loading.service';
import {ConfirmDialogService} from '../../../shared/services/confirm-dialog.service';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [RouterModule, CommonModule, StyleClassModule, MenuModule, ConfirmDialogModule],
  templateUrl: './topbar.html'
})
export class Topbar {
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
