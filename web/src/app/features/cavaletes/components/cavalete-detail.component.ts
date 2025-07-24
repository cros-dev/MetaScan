import {Component, Input} from '@angular/core';
import {Cavalete} from '../models/cavalete.model';
import {CardModule} from 'primeng/card';
import {TagModule} from 'primeng/tag';

@Component({
  selector: 'app-cavalete-detail',
  standalone: true,
  imports: [CardModule, TagModule],
  template: `
    @if (cavalete) {
      <p-card>
        <div class="flex justify-between items-center mb-2">
          <span class="font-bold text-lg">{{ cavalete.name }}</span>
          <p-tag [value]="cavalete.status"></p-tag>
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
      </p-card>
    }
  `
})
export class CavaleteDetailComponent {
  @Input() cavalete?: Cavalete;
}
