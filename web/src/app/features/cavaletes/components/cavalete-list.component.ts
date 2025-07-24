import {Component, Input} from '@angular/core';
import {Cavalete} from '../models/cavalete.model';
import {ButtonModule} from 'primeng/button';
import {InputTextModule} from 'primeng/inputtext';
import {FormsModule} from '@angular/forms';
import {IconField} from 'primeng/iconfield';
import {InputIcon} from 'primeng/inputicon';
import {SelectButtonModule} from 'primeng/selectbutton';
import {Router} from '@angular/router';
import {CavaletesListTableComponent} from './cavalete-list-table.component';
import {CavaletesListCardComponent} from './cavalete-list-card.component';

@Component({
  selector: 'app-cavaletes-list',
  standalone: true,
  imports: [
    CavaletesListTableComponent,
    CavaletesListCardComponent,
    ButtonModule,
    InputTextModule,
    FormsModule,
    IconField,
    InputIcon,
    SelectButtonModule,
    CavaletesListTableComponent,
    CavaletesListCardComponent
  ],
  template: `
    <div class="p-datatable-header flex flex-col md:flex-row justify-between items-center mb-4 gap-4">
      <div class="flex items-center gap-4 w-full md:w-auto">
        <p-selectButton
          [options]="viewOptions"
          [(ngModel)]="viewMode"
          optionLabel="label"
          [optionValue]="'value'"
          class="mr-4"
        />
      </div>
      <span class="ml-auto flex items-center w-full md:w-auto">
        <p-iconfield iconPosition="left" class="w-full">
          <p-inputicon>
            <i class="pi pi-search"></i>
          </p-inputicon>
          <input pInputText type="text" placeholder="Buscar..." [(ngModel)]="globalFilter" />
        </p-iconfield>
        <p-button
          icon="pi pi-filter-slash"
          aria-label="Limpar filtro"
          styleClass="p-button-outlined ml-2"
          (onClick)="clearFilter()"
        ></p-button>
      </span>
    </div>
    @if (viewMode === 'table') {
      <app-cavaletes-list-table
        [cavaletes]="filteredCavaletes"
        (view)="viewCavalete($event)"
        (edit)="editCavalete($event)"
      ></app-cavaletes-list-table>
    }
    @if (viewMode === 'card') {
      <app-cavaletes-list-card
        [cavaletes]="filteredCavaletes"
        (view)="viewCavalete($event)"
        (edit)="editCavalete($event)"
      ></app-cavaletes-list-card>
    }
  `
})
export class CavaleteListComponent {
  @Input() cavaletes: Cavalete[] = [];
  globalFilter = '';
  viewOptions = [
    { label: 'Tabela', value: 'table', icon: 'pi pi-table' },
    { label: 'Cards', value: 'card', icon: 'pi pi-th-large' }
  ];
  viewMode: 'table' | 'card' = 'table';

  constructor(private router: Router) {}

  get filteredCavaletes(): Cavalete[] {
    if (!this.globalFilter?.trim()) {
      return this.cavaletes;
    }
    const filter = this.globalFilter.trim().toLowerCase();
    return this.cavaletes.filter(c =>
      c.code.toLowerCase().includes(filter) ||
      c.name.toLowerCase().includes(filter) ||
      (c.user ? c.user.toLowerCase().includes(filter) : false) ||
      c.status.toLowerCase().includes(filter)
    );
  }

  clearFilter() {
    this.globalFilter = '';
  }

  viewCavalete(cavalete: Cavalete) {
    this.router.navigate(['/cavaletes', cavalete.code]).then(success => {
      if (success) {
        console.log('Navegação concluída com sucesso');
      } else {
        console.warn('Navegação falhou');
      }
    });
  }

  editCavalete(cavalete: Cavalete) {
    console.log('Edit', cavalete);
  }
}
