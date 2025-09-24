import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ProductView } from '../components/product-view/product-view';

@Component({
  selector: 'app-product-view-page',
  standalone: true,
  imports: [RouterModule, ProductView],
  template: `
    <div class="layout-main">
      <app-product-view></app-product-view>
    </div>
  `
})
export class ProductViewPage {}
