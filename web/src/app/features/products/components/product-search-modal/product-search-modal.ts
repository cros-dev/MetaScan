import { Component, EventEmitter, Output, AfterViewInit, ElementRef, ViewChild, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ProductService } from '../../services/product.service';
import { ProductResponse } from '../../models/product.model';
import { NotificationService } from '../../../../shared/services/notification.service';
import { LoadingService } from '../../../../shared/services/loading.service';

@Component({
  selector: 'app-product-search-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './product-search-modal.html',
  styleUrl: './product-search-modal.scss'
})
export class ProductSearchModal implements AfterViewInit {
  @Input() currentProductCode = ''; // Código do produto atual sendo exibido
  @Output() productFound = new EventEmitter<ProductResponse>();
  @Output() close = new EventEmitter<void>();
  @ViewChild('productCodeInput') productCodeInput!: ElementRef<HTMLInputElement>;

  productCode = '';
  loading = false;

  constructor(
    private productService: ProductService,
    private notificationService: NotificationService,
    private loadingService: LoadingService
  ) {}

  ngAfterViewInit() {
    setTimeout(() => {
      if (this.productCodeInput) {
        this.productCodeInput.nativeElement.focus();
      }
    }, 100);
  }

  searchProduct() {
    if (!this.productCode.trim()) {
      this.notificationService.showError('Digite um código de produto');
      return;
    }

    const trimmedCode = this.productCode.trim();

    if (this.isSameProduct(trimmedCode)) {
      return;
    }

    this.loading = true;
    this.loadingService.show();

    this.productService.getProduct(trimmedCode).subscribe({
      next: (product) => {
        this.productFound.emit(product);
        this.closeModal();
        this.loading = false;
        this.loadingService.hide();
      },
      error: (error) => {
        this.productService.handleProductError(error, () => {
          this.loading = false;
          this.loadingService.hide();
        });
      }
    });
  }

  closeModal() {
    this.productCode = '';
    this.close.emit();
  }

  isSameProduct(code: string): boolean {
    return !!(this.currentProductCode && code.trim() === this.currentProductCode);
  }

  onKeyPress(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      this.searchProduct();
    }
  }
}
