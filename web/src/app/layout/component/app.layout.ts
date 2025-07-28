import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { LayoutService } from '../service/layout.service';
import { AppTopbar } from './app.topbar';
import { AppSidebar } from './app.sidebar';
import {NgClass} from '@angular/common';
import { ToastModule } from 'primeng/toast';
import { MessageService, ConfirmationService } from 'primeng/api';
import { LoadingSpinnerComponent } from '../../shared/components/loading/loading-spinner.component';
import { LoadingService } from '../../shared/services/loading.service';
import { AsyncPipe } from '@angular/common';
import { ConfirmDialogModule } from 'primeng/confirmdialog';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [RouterOutlet, AppTopbar, AppSidebar, NgClass, ToastModule, LoadingSpinnerComponent, AsyncPipe, ConfirmDialogModule],
  providers: [MessageService, ConfirmationService],
  template: `
    <div class="layout-wrapper" [ngClass]="containerClass">
      <app-topbar></app-topbar>
      <p-toast position="bottom-right" />
      <p-confirmDialog position="topright"></p-confirmDialog>
      <app-loading-spinner [show]="(loading$ | async) ?? false" />
      <app-sidebar></app-sidebar>
      <div class="layout-main-container">
        <div class="layout-main">
          <router-outlet></router-outlet>
        </div>
      </div>
    </div>
  `
})
export class AppLayout {
  loading$;
  constructor(public layoutService: LayoutService, public loadingService: LoadingService) {
    this.loading$ = this.loadingService.loading$;
  }

  get containerClass() {
    return {
      'layout-static-inactive': this.layoutService.layoutState().staticMenuDesktopInactive
    };
  }
}
