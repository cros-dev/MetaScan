import { Component, OnInit } from '@angular/core';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { ProductDetail } from '../components/product-detail/product-detail';
import { Breadcrumb } from '../../../shared/components/breadcrumb/breadcrumb';

@Component({
  selector: 'app-product-detail-page',
  standalone: true,
  imports: [RouterModule, ProductDetail, Breadcrumb],
  template: `
    <div class="layout-main">
      <app-breadcrumb [items]="breadcrumbItems"></app-breadcrumb>
      <app-product-detail></app-product-detail>
    </div>
  `
})
export class ProductDetailPage implements OnInit {
  breadcrumbItems: any[] = [];

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.updateBreadcrumb();
  }

  private updateBreadcrumb() {
    const productCode = this.route.snapshot.params['code'];

    this.breadcrumbItems = [
      { label: 'Dashboard', url: '/' },
      { label: 'Produtos', url: '/products' },
      { label: `Produto ${productCode}` }
    ];
  }
}
