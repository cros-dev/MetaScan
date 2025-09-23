import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ProductResponse } from '../../models/product.model';
import { ProductSearchModal } from '../product-search-modal/product-search-modal';

@Component({
  selector: 'app-product-list',
  standalone: true,
  imports: [CommonModule, FormsModule, ProductSearchModal],
  templateUrl: './product-list.html',
  styleUrl: './product-list.scss'
})
export class ProductList implements OnInit, OnDestroy {
  loading = false;
  showSearchModal = false;

  constructor(
    private router: Router
  ) {}

  ngOnInit() {
  }

  ngOnDestroy() {
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
