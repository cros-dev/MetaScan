import { Component, OnInit } from '@angular/core';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { ProductView } from '../components/product-view/product-view';
import { Breadcrumb } from '../../../shared/components/breadcrumb/breadcrumb';

@Component({
  selector: 'app-product-view-page',
  standalone: true,
  imports: [RouterModule, ProductView, Breadcrumb],
  template: `
    <div class="layout-main">
      <app-breadcrumb [items]="breadcrumbItems"></app-breadcrumb>
      <app-product-view></app-product-view>
    </div>
  `
})
export class ProductViewPage implements OnInit {
  breadcrumbItems: any[] = [];

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.updateBreadcrumb();
  }

  private updateBreadcrumb() {
    const cavaleteId = this.route.snapshot.params['cavaleteId'];
    const productCode = this.route.snapshot.params['code'];

    this.breadcrumbItems = [
      { label: 'Dashboard', url: '/' },
      { label: 'Cavaletes', url: '/cavaletes' },
      { label: `Cavalete ${cavaleteId}`, url: `/cavaletes/${cavaleteId}` },
      { label: `Produto ${productCode}` }
    ];
  }
}
