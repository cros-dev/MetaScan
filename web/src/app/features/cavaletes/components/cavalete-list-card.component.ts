import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Cavalete } from '../models/cavalete.model';
import { CardModule } from 'primeng/card';
import { TagModule } from 'primeng/tag';
import { ButtonModule } from 'primeng/button';
import { CAVALETE_STATUS_LABELS } from '../utils/status.utils';

@Component({
  selector: 'app-cavaletes-list-card',
  standalone: true,
  imports: [CardModule, TagModule, ButtonModule],
  template: `
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      @for (cavalete of cavaletes; track cavalete) {
        <p-card class="border border-surface-200 dark:border-surface-700 bg-surface-0 dark:bg-surface-900 rounded">
          <div class="flex justify-between items-center mb-2">
            <span class="font-bold text-lg">{{ cavalete.name }}</span>
            <p-tag [value]="statusLabels[cavalete.status] || cavalete.status" [severity]="getStatusSeverity(cavalete.status)"></p-tag>
          </div>
          <div class="mb-2">
            <span class="text-sm text-surface-500">Código:</span> {{ cavalete.code }}
          </div>
          <div class="mb-2 flex items-center">
            <i class="pi pi-user mr-1"></i>
            <span>{{ cavalete.user ? cavalete.user : 'Não atribuído' }}</span>
          </div>
          <div class="mb-2">
            <span class="text-sm text-surface-500">Ocupação:</span> {{ cavalete.occupancy }}
          </div>
          <div class="flex gap-2 mt-4">
            <p-button
              icon="pi pi-pencil"
              aria-label="Edit"
              styleClass="p-button-text p-button-sm"
              (onClick)="edit.emit(cavalete)"
            ></p-button>
            <p-button
              icon="pi pi-eye"
              aria-label="View"
              styleClass="p-button-text p-button-sm p-button-info"
              (onClick)="view.emit(cavalete)"
            ></p-button>
          </div>
        </p-card>
      }
    </div>
  `
})
export class CavaletesListCardComponent {
  @Input() cavaletes: Cavalete[] = [];
  @Output() view = new EventEmitter<Cavalete>();
  @Output() edit = new EventEmitter<Cavalete>();
  statusLabels = CAVALETE_STATUS_LABELS;

  getStatusSeverity(status: string): string {
    switch (status) {
      case 'available':
        return 'success';
      case 'in_use':
        return 'warning';
      case 'maintenance':
        return 'danger';
      default:
        return 'info';
    }
  }
}
