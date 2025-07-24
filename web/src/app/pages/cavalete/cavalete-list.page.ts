import { Component, OnInit } from '@angular/core';
import { Cavalete } from '../../features/cavaletes/models/cavalete.model';
import {CavaleteListComponent} from '../../features/cavaletes/components/cavalete-list.component';
import {CavaleteService} from '../../features/cavaletes/services/cavalete.service';

@Component({
  selector: 'app-cavalete-list',
  standalone: true,
  imports: [CavaleteListComponent],
  template: `
    <app-cavaletes-list [cavaletes]="cavaletes"></app-cavaletes-list>
  `
})
export class CavaleteListPage implements OnInit {
  cavaletes: Cavalete[] = [];

  constructor(private cavaletesService: CavaleteService) {}

  ngOnInit(): void {
    this.cavaletesService.getAll().subscribe({
      next: (data) => (this.cavaletes = data),
      error: (err) => console.error('Erro ao buscar cavaletes', err)
    });
  }
}
