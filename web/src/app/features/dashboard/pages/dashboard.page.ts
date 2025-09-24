import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { DashboardContent } from '../components/dashboard-content/dashboard-content';

@Component({
  selector: 'app-dashboard-page',
  standalone: true,
  imports: [RouterModule, DashboardContent],
  template: `
    <div class="layout-main">
      <app-dashboard-content></app-dashboard-content>
    </div>
  `
})
export class DashboardPage {}
