import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ConfirmationService } from 'primeng/api';

export interface ConfirmDialogConfig {
  message: string;
  header?: string;
  icon?: string;
  acceptLabel?: string;
  rejectLabel?: string;
  acceptIcon?: string;
  rejectIcon?: string;
  acceptButtonStyleClass?: string;
  rejectButtonStyleClass?: string;
}

export type ConfirmDialogPosition = 'topright' | 'center' | 'top' | 'bottom' | 'left' | 'right' | 'topleft' | 'bottomleft' | 'bottomright';

@Component({
  selector: 'app-confirm-dialog',
  standalone: true,
  imports: [CommonModule, ConfirmDialogModule],
  providers: [ConfirmationService],
  template: `
    <p-confirmDialog 
      [position]="position"
      [acceptButtonStyleClass]="config.acceptButtonStyleClass || 'p-button-danger'"
      [rejectButtonStyleClass]="config.rejectButtonStyleClass || 'p-button-secondary'"
    ></p-confirmDialog>
  `
})
export class ConfirmDialogComponent {
  @Input() position: ConfirmDialogPosition = 'topright';
  @Input() config: ConfirmDialogConfig = {
    message: 'Tem certeza?',
    header: 'Confirmação',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Sim',
    rejectLabel: 'Não',
    acceptIcon: 'pi pi-check',
    rejectIcon: 'pi pi-times'
  };

  @Output() onAccept = new EventEmitter<void>();
  @Output() onReject = new EventEmitter<void>();

  constructor() {}
} 