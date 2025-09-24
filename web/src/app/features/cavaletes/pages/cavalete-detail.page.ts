import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CavaleteDetail } from '../components/cavalete-detail/cavalete-detail';

@Component({
  selector: 'app-cavalete-detail-page',
  standalone: true,
  imports: [RouterModule, CavaleteDetail],
  template: `
    <div class="layout-main">
      <app-cavalete-detail></app-cavalete-detail>
    </div>
  `
})
export class CavaleteDetailPage {}
