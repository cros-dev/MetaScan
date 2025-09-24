import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Subject, debounceTime, distinctUntilChanged, takeUntil } from 'rxjs';
import { CavaleteService } from '../../services/cavalete.service';
import { Cavalete, CavaleteFilters } from '../../models/cavalete.model';
import { NotificationService } from '../../../../shared/services/notification.service';
import { LoadingService } from '../../../../shared/services/loading.service';
import { STATUS_FILTER_OPTIONS, CAVALETE_STATUS_CLASSES, CAVALETE_STATUS_LABELS } from '../../constants/cavalete.constants';

@Component({
  selector: 'app-cavalete-list',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './cavalete-list.html',
  styleUrl: './cavalete-list.scss'
})
export class CavaleteList implements OnInit, OnDestroy {
  cavaletes: Cavalete[] = [];
  totalCount = 0;

  filters: CavaleteFilters = {
    status: '',
    search: ''
  };

  statusOptions = STATUS_FILTER_OPTIONS;

  showCreateModal = false;
  selectedType: 'corredor' | 'torre' = 'corredor';

  typeOptions = [
    { label: 'Corredor (6 slots por lado)', value: 'corredor' },
    { label: 'Torre (12 slots por lado)', value: 'torre' }
  ];

  private searchSubject = new Subject<string>();
  private destroy$ = new Subject<void>();

  constructor(
    private cavaleteService: CavaleteService,
    private notificationService: NotificationService,
    private loadingService: LoadingService
  ) {}

  ngOnInit() {
    this.loadCavaletes();
    this.setupLiveSearch();
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

  setupLiveSearch() {
    this.searchSubject
      .pipe(
        debounceTime(100),
        distinctUntilChanged(),
        takeUntil(this.destroy$)
      )
      .subscribe(searchTerm => {
        this.filters.search = searchTerm;
        this.loadCavaletes();
      });
  }

  onSearchInput(event: Event) {
    const target = event.target as HTMLInputElement;
    this.searchSubject.next(target.value);
  }

  loadCavaletes() {
    this.loadingService.show();

    this.cavaleteService.getCavaletes(this.filters).subscribe({
      next: (response) => {
        this.cavaletes = response.results;
        this.totalCount = response.count;
        this.loadingService.hide();
      },
      error: (error) => {
        console.error('Erro ao carregar cavaletes:', error);
        this.notificationService.showError('Erro ao carregar cavaletes');
        this.loadingService.hide();
      }
    });
  }

  onFilterChange() {
    this.loadCavaletes();
  }

  getStatusClass(status: string): string {
    return CAVALETE_STATUS_CLASSES[status] || 'bg-gray-100 text-gray-800';
  }

  getStatusLabel(status: string): string {
    return CAVALETE_STATUS_LABELS[status] || status;
  }

  exportToExcel() {
    this.loadingService.show();

    this.cavaleteService.exportToExcel().subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'cavaletes.xlsx';
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

  openCreateModal() {
    this.showCreateModal = true;
    this.selectedType = 'corredor';
  }

  closeCreateModal() {
    this.showCreateModal = false;
  }

  createCavalete() {
    this.loadingService.show();

    this.cavaleteService.createCavalete({ type: this.selectedType }).subscribe({
      next: () => {
        this.notificationService.showSuccess(`Cavalete ${this.selectedType} criado com sucesso!`);
        this.loadingService.hide();
        this.closeCreateModal();
        this.loadCavaletes();
      },
      error: (error) => {
        console.error('Erro ao criar cavalete:', error);
        this.notificationService.showError('Erro ao criar cavalete');
        this.loadingService.hide();
      }
    });
  }
}
