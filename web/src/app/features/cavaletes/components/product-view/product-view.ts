import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { ProductService } from '../../../products/services/product.service';
import { ProductResponse } from '../../../products/models/product.model';
import { FormatNumberPipe } from '../../../../shared/pipes/format-number.pipe';
import { CavaleteService } from '../../services/cavalete.service';
import { Cavalete } from '../../models/cavalete.model';

@Component({
  selector: 'app-product-view',
  standalone: true,
  imports: [CommonModule, FormatNumberPipe],
  templateUrl: './product-view.html',
  styleUrl: './product-view.scss'
})
export class ProductView implements OnInit {
  product?: ProductResponse;
  cavalete?: Cavalete;
  loading = false;
  productCode = '';
  cavaleteId: number | null = null;
  slotLocation = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public productService: ProductService,
    private cavaleteService: CavaleteService
  ) {}

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.productCode = params['code'];
      this.cavaleteId = params['cavaleteId'] ? Number(params['cavaleteId']) : null;
      this.slotLocation = params['slotLocation'] || '';

      if (this.cavaleteId) {
        this.loadCavalete();
      }

      if (this.productCode) {
        this.loadProduct();
      }
    });
  }

  loadCavalete() {
    if (!this.cavaleteId) return;

    this.cavaleteService.getCavalete(this.cavaleteId).subscribe({
      next: (cavalete) => {
        this.cavalete = cavalete;
      },
      error: (error) => {
        console.error('Erro ao carregar cavalete:', error);
      }
    });
  }


  loadProduct() {
    this.loading = true;

    this.productService.getProduct(this.productCode).subscribe({
      next: (product) => {
        this.product = product;
        this.loading = false;
      },
      error: (error) => {
        this.productService.handleProductError(error, () => {
          this.loading = false;
          this.goBack();
        });
      }
    });
  }

  goBack() {
    if (this.cavaleteId) {
      this.router.navigate(['/cavaletes', this.cavaleteId]);
    } else {
      this.router.navigate(['/cavaletes']);
    }
  }
}
