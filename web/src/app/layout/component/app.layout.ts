import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { LayoutService } from '../service/layout.service';
import { AppTopbar } from './app.topbar';
import { AppSidebar } from './app.sidebar';
import {NgClass} from '@angular/common';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [RouterOutlet, AppTopbar, AppSidebar, NgClass],
  template: `
    <div class="layout-wrapper" [ngClass]="containerClass">
      <app-topbar></app-topbar>
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
  constructor(public layoutService: LayoutService) {}

  get containerClass() {
    return {
      'layout-static-inactive': this.layoutService.layoutState().staticMenuDesktopInactive
    };
  }
}
