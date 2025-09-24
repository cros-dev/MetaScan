import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CavaleteDetail } from '../components/cavalete-detail/cavalete-detail';
import { Breadcrumb } from '../../../shared/components/breadcrumb/breadcrumb';

@Component({
  selector: 'app-cavalete-detail-page',
  standalone: true,
  imports: [RouterModule, CavaleteDetail, Breadcrumb],
  template: `
    <div class="layout-main">
      <app-breadcrumb [items]="breadcrumbItems"></app-breadcrumb>
      <app-cavalete-detail></app-cavalete-detail>
    </div>
  `
})
export class CavaleteDetailPage {
  breadcrumbItems = [
    { label: 'Dashboard', url: '/' },
    { label: 'Cavaletes', url: '/cavaletes' },
    { label: 'Detalhes' }
  ];
}
