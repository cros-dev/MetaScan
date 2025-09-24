import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { ProductService } from '../../services/product.service';
import { ProductResponse } from '../../models/product.model';
import { LoadingService } from '../../../../shared/services/loading.service';
import { ProductSearchModal } from '../product-search-modal/product-search-modal';
import { FormatNumberPipe } from '../../../../shared/pipes/format-number.pipe';

@Component({
  selector: 'app-product-detail',
  standalone: true,
  imports: [CommonModule, ProductSearchModal, FormatNumberPipe],
  templateUrl: './product-detail.html',
  styleUrl: './product-detail.scss'
})
export class ProductDetail implements OnInit {
  product?: ProductResponse;
  loading = false;
  productCode = '';
  showSearchModal = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public productService: ProductService,
    private loadingService: LoadingService
  ) {}

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.productCode = params['code'];

      if (this.productCode) {
        this.loadProduct();
      }
    });
  }

  loadProduct() {
    this.loading = true;
    this.loadingService.show();

    this.productService.getProduct(this.productCode).subscribe({
      next: (product) => {
        this.product = product;
        this.loading = false;
        this.loadingService.hide();
      },
      error: (error) => {
        this.productService.handleProductError(error, () => {
          this.loading = false;
          this.loadingService.hide();
          this.router.navigate(['/products']);
        });
      }
    });
  }

  goBack() {
    this.router.navigate(['/products']);
  }

  openSearchModal() {
    this.showSearchModal = true;
  }

  closeSearchModal() {
    this.showSearchModal = false;
  }

  onProductFound(product: ProductResponse) {
    this.closeSearchModal();
    this.router.navigate(['/products', product.code]);
  }


}
