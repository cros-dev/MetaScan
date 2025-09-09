import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { LayoutService } from './services/layout.service';
import { Topbar } from './components/topbar/topbar';
import { Sidebar } from './components/sidebar/sidebar';
import {NgClass} from '@angular/common';
import { ConfirmationService } from 'primeng/api';
import { LoadingSpinnerComponent } from '../shared/components/loading/loading-spinner.component';
import { LoadingService } from '../shared/services/loading.service';
import { AsyncPipe } from '@angular/common';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { NotificationContainerComponent } from '../shared/components/notification/notification-container.component';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [RouterOutlet, Topbar, Sidebar, NgClass, LoadingSpinnerComponent, AsyncPipe, ConfirmDialogModule, NotificationContainerComponent],
  providers: [ConfirmationService],
  templateUrl: './app-layout.component.html'
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
