import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {CommonModule} from '@angular/common';
import {CavaleteService} from '../../features/cavaletes/services/cavalete.service';
import {Cavalete} from '../../features/cavaletes/models/cavalete.model';
import {CavaleteDetailComponent} from '../../features/cavaletes/components/cavalete-detail.component';

@Component({
  selector: 'app-cavalete-detail-page',
  standalone: true,
  imports: [CommonModule, CavaleteDetailComponent],
  template: `
    <div class="p-4">
      @if (loading) {
        <p>Carregando...</p>
      } @else {
        <app-cavalete-detail [cavalete]="cavalete" />
      }
    </div>
  `
})
export class CavaleteDetailPage implements OnInit {
  cavalete?: Cavalete;
  loading = true;

  constructor(
    private route: ActivatedRoute,
    private cavaleteService: CavaleteService
  ) {}

  ngOnInit(): void {
    const code = this.route.snapshot.paramMap.get('code');
    if (code) {
      this.cavaleteService.getByCode(code).subscribe({
        next: (data) => {
          this.cavalete = data;
          this.loading = false;
        },
        error: (err) => {
          console.error('Erro ao buscar cavalete', err);
          this.loading = false;
        }
      });
    } else {
      console.error('Código do cavalete não informado');
      this.loading = false;
    }
  }
}
