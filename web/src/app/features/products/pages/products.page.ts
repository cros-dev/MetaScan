import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ProductList } from '../components/product-list/product-list';
import { Breadcrumb } from '../../../shared/components/breadcrumb/breadcrumb';

@Component({
  selector: 'app-products-page',
  standalone: true,
  imports: [RouterModule, ProductList, Breadcrumb],
  template: `
    <div class="layout-main">
      <app-breadcrumb [items]="breadcrumbItems"></app-breadcrumb>
      <app-product-list></app-product-list>
    </div>
  `
})
export class ProductsPage {
  breadcrumbItems = [
    { label: 'Dashboard', url: '/' },
    { label: 'Produtos' }
  ];
}
