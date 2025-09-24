import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CavaleteList } from '../components/cavalete-list/cavalete-list';
import { Breadcrumb } from '../../../shared/components/breadcrumb/breadcrumb';

@Component({
  selector: 'app-cavalete-list-page',
  standalone: true,
  imports: [RouterModule, CavaleteList, Breadcrumb],
  template: `
    <div class="layout-main">
      <app-breadcrumb [items]="breadcrumbItems"></app-breadcrumb>
      <app-cavalete-list></app-cavalete-list>
    </div>
  `
})
export class CavaleteListPage {
  breadcrumbItems = [
    { label: 'Dashboard', url: '/' },
    { label: 'Cavaletes' }
  ];
}
