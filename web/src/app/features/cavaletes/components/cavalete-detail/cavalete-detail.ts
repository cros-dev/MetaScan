import {Component, OnInit} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ActivatedRoute, Router, RouterModule} from '@angular/router';
import {CavaleteService} from '../../services/cavalete.service';
import {Cavalete, Slot} from '../../models/cavalete.model';
import {NotificationService} from '../../../../shared/services/notification.service';
import {LoadingService} from '../../../../shared/services/loading.service';
import {CAVALETE_STATUS_CLASSES, CAVALETE_STATUS_LABELS} from '../../constants/cavalete.constants';
import {UserAssignment} from '../../../users/components/user-assignment/user-assignment';
import {SlotProductAssociation} from '../slot-product-association/slot-product-association';
import {TruncatePipe} from '../../../../shared/pipes/truncate.pipe';

@Component({
  selector: 'app-cavalete-detail',
  standalone: true,
  imports: [CommonModule, RouterModule, UserAssignment, SlotProductAssociation, TruncatePipe],
  templateUrl: './cavalete-detail.html',
  styleUrl: './cavalete-detail.scss'
})
export class CavaleteDetail implements OnInit {
  cavalete: Cavalete | null = null;
  cavaleteId: number | null = null;
  showUserAssignment = false;
  selectedSide: 'A' | 'B' = 'A';
  showSlotProductAssociation = false;
  selectedSlotForProduct: Slot | null = null;


  constructor(
    private cavaleteService: CavaleteService,
    private route: ActivatedRoute,
    private router: Router,
    private notificationService: NotificationService,
    private loadingService: LoadingService
  ) {}

  ngOnInit() {
    this.cavaleteId = Number(this.route.snapshot.paramMap.get('id'));
    if (this.cavaleteId) {
      this.loadCavalete();
    }
  }

  loadCavalete() {
    if (!this.cavaleteId) return;

    this.loadingService.show();

    this.cavaleteService.getCavalete(this.cavaleteId).subscribe({
      next: (cavalete) => {
        this.cavalete = cavalete;
        this.loadingService.hide();
      },
      error: (error) => {
        console.error('Erro ao carregar cavalete:', error);
        this.notificationService.showError('Erro ao carregar detalhes do cavalete');
        this.loadingService.hide();
        this.router.navigate(['/cavaletes']);
      }
    });
  }

  getStatusClass(status: string): string {
    return CAVALETE_STATUS_CLASSES[status] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
  }

  getStatusLabel(status: string): string {
    return CAVALETE_STATUS_LABELS[status] || status;
  }

  getSlotStatusClass(slot: Slot): string {
    if (slot.product_code && slot.product_code.trim() !== '') {
      return 'slot-filled';
    }
    return 'slot-empty';
  }

  getSlotsBySide(side: 'A' | 'B'): Slot[] {
    if (!this.cavalete) return [];
    return this.cavalete.slots.filter(slot => slot.side === side);
  }

  exportCavalete() {
    if (!this.cavalete) return;

    this.loadingService.show();

    this.cavaleteService.exportToExcel([this.cavalete.id], [this.cavalete.name]).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${this.cavalete?.code}.xlsx`;
        link.click();
        window.URL.revokeObjectURL(url);

        this.notificationService.showSuccess('Exportação realizada com sucesso!');
        this.loadingService.hide();
      },
      error: (error) => {
        console.error('Erro ao exportar:', error);
        this.notificationService.showError('Erro ao exportar dados');
        this.loadingService.hide();
      }
    });
  }

  openUserAssignment() {
    this.showUserAssignment = true;
  }

  closeUserAssignment() {
    this.showUserAssignment = false;
    if (this.cavaleteId) {
      this.loadCavalete();
    }
  }

  onSlotClick(slot: Slot) {

    if (slot.product_code) {
      this.router.navigate(['/cavaletes', this.cavaleteId, 'products', slot.product_code, 'slots', slot.location_code]);
    } else {
      this.selectedSlotForProduct = slot;
      this.showSlotProductAssociation = true;
    }
  }

  closeSlotProductAssociation() {
    this.showSlotProductAssociation = false;
    this.selectedSlotForProduct = null;
  }

  onProductAssociated() {
    if (!this.cavalete) return;

    this.loadCavalete();

    this.closeSlotProductAssociation();
  }
}
