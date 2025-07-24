import { Component, Input, Output, EventEmitter } from '@angular/core';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { Cavalete } from '../models/cavalete.model';
import { CAVALETE_STATUS_LABELS } from '../utils/status.utils';

@Component({
  selector: 'app-cavaletes-list-table',
  standalone: true,
  imports: [TableModule, ButtonModule],
  template: `
    <p-table
      class="p-datatable-gridlines"
      [value]="cavaletes"
      [virtualScroll]="true"
      [virtualScrollItemSize]="50"
      scrollHeight="400px"
    >
      <ng-template pTemplate="header">
        <tr>
          <th>Código</th>
          <th>Cavalete</th>
          <th>Conferente</th>
          <th>Ocupação</th>
          <th>Status</th>
          <th>Ações</th>
        </tr>
      </ng-template>
      <ng-template pTemplate="body" let-row>
        <tr>
          <td>{{ row.code }}</td>
          <td>{{ row.name }}</td>
          <td>
            <i class="pi pi-user mr-1"></i>
            {{ row.user ? row.user : 'Não atribuído' }}
          </td>
          <td>{{ row.occupancy }}</td>
          <td>{{ statusLabels[row.status] || row.status }}</td>
          <td>
            <p-button
              icon="pi pi-pencil"
              aria-label="Edit"
              styleClass="p-button-text p-button-sm mr-2"
              (onClick)="edit.emit(row)"
            ></p-button>
            <p-button
              icon="pi pi-eye"
              aria-label="View"
              styleClass="p-button-text p-button-sm p-button-info"
              (onClick)="view.emit(row)"
            ></p-button>
          </td>
        </tr>
      </ng-template>
    </p-table>
  `
})
export class CavaletesListTableComponent {
  @Input() cavaletes: Cavalete[] = [];
  @Output() view = new EventEmitter<Cavalete>();
  @Output() edit = new EventEmitter<Cavalete>();
  statusLabels = CAVALETE_STATUS_LABELS;
}
