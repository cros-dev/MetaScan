import { Component, Input, Output, EventEmitter, ViewChild, ElementRef, AfterViewInit, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ProductService } from '../../../products/services/product.service';
import { ProductResponse } from '../../../products/models/product.model';
import { Slot } from '../../models/cavalete.model';
import { NotificationService } from '../../../../shared/services/notification.service';
import { LoadingService } from '../../../../shared/services/loading.service';
import { CavaleteService } from '../../services/cavalete.service';
import { FormatNumberPipe } from '../../../../shared/pipes/format-number.pipe';

@Component({
  selector: 'app-slot-product-association',
  standalone: true,
  imports: [CommonModule, FormsModule, FormatNumberPipe],
  templateUrl: './slot-product-association.html',
  styleUrl: './slot-product-association.scss'
})
export class SlotProductAssociation implements AfterViewInit, OnChanges {
  @Input() slot: Slot | null = null;
  @Input() show = false;
  @Output() close = new EventEmitter<void>();
  @Output() productAssociated = new EventEmitter<Slot>();
  @ViewChild('productCodeInput') productCodeInput!: ElementRef<HTMLInputElement>;

  productCode = '';
  foundProduct: ProductResponse | null = null;
  loading = false;

  constructor(
    private productService: ProductService,
    private notificationService: NotificationService,
    private loadingService: LoadingService,
    private cavaleteService: CavaleteService
  ) {}

  ngAfterViewInit() {
    this.focusInput();
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['show'] && changes['show'].currentValue === true) {
      this.focusInput();
    }
  }

  focusInput() {
    setTimeout(() => {
      if (this.productCodeInput && this.show && !this.foundProduct) {
        this.productCodeInput.nativeElement.focus();
      }
    }, 100);
  }

  closeModal() {
    this.show = false;
    this.foundProduct = null;
    this.productCode = '';
    this.close.emit();
  }

  clearFoundProduct() {
    this.foundProduct = null;
    this.productCode = '';
    this.focusInput();
  }

  searchProduct() {
    if (!this.productCode.trim()) {
      this.notificationService.showError('Digite um código de produto');
      return;
    }

    this.loading = true;
    this.loadingService.show();

    this.productService.getProduct(this.productCode.trim()).subscribe({
      next: (product) => {
        this.foundProduct = product;
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

  onKeyPress(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      this.searchProduct();
    }
  }

  associateProduct() {
    if (!this.slot || !this.foundProduct) return;

    this.loading = true;
    this.loadingService.show();

    this.cavaleteService.startSlotConfirmation(this.slot.id).subscribe({
      next: () => {
        const slotData = {
          product_code: this.foundProduct!.code,
          product_description: this.foundProduct!.description,
          quantity: 1
        };

        this.cavaleteService.updateSlot(this.slot!.id, slotData).subscribe({
          next: (updatedSlot) => {
            const updatedSlotData: Slot = {
              ...this.slot!,
              ...updatedSlot
            };

            this.loading = false;
            this.loadingService.hide();

            this.notificationService.showSuccess(`Produto ${this.foundProduct!.code} associado ao slot ${this.slot!.location_code} com sucesso!`);

            this.productAssociated.emit(updatedSlotData);

            this.closeModal();
          },
          error: (error) => {
            console.error('Erro ao atualizar slot com produto:', error);

            this.loading = false;
            this.loadingService.hide();

            if (error.status === 400) {
              this.notificationService.showError(error.error.detail || 'Erro na validação dos dados');
            } else if (error.status === 403) {
              this.notificationService.showError('Você não tem permissão para esta operação');
            } else if (error.status === 502) {
              this.notificationService.showError('Erro de conexão com a Sankhya. Tente novamente.');
            } else {
              this.notificationService.showError('Erro ao associar produto ao slot. Tente novamente.');
            }
          }
        });
      },
      error: (error) => {
        console.error('Erro ao iniciar conferência do slot:', error);

        this.loading = false;
        this.loadingService.hide();

        if (error.status === 400) {
          this.notificationService.showError(error.error.detail || 'Erro ao iniciar conferência do slot');
        } else if (error.status === 403) {
          this.notificationService.showError('Você não tem permissão para iniciar conferência');
        } else {
          this.notificationService.showError('Erro ao iniciar conferência. Tente novamente.');
        }
      }
    });
  }
}
