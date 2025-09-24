import {Component, OnDestroy, OnInit} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {Router} from '@angular/router';
import {Subject} from 'rxjs';
import {debounceTime, distinctUntilChanged, takeUntil} from 'rxjs/operators';
import {User, UserService} from '../../services/user.service';
import {LoadingService} from '../../../../shared/services/loading.service';
import {UserRoleService} from '../../../../shared/services/user-role.service';
import {ErrorHandlerUtil} from '../../../../shared/utils/error-handler.util';

@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './user-list.html',
  styleUrl: './user-list.scss'
})
export class UserList implements OnInit, OnDestroy {
  users: User[] = [];

  filters = {
    role: '',
    search: '',
    is_active: true
  };

  roleOptions = [
    {label: 'Todos', value: ''},
    {label: 'Administrador', value: 'admin'},
    {label: 'Gestor', value: 'manager'},
    {label: 'Conferente', value: 'auditor'}
  ];

  private searchSubject = new Subject<string>();
  private destroy$ = new Subject<void>();

  constructor(
    private userService: UserService,
    private loadingService: LoadingService,
    private router: Router,
    private userRoleService: UserRoleService,
    private errorHandler: ErrorHandlerUtil
  ) {
  }

  ngOnInit() {
    this.loadUsers();
    this.setupLiveSearch();
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private setupLiveSearch() {
    this.searchSubject
      .pipe(
        debounceTime(300),
        distinctUntilChanged(),
        takeUntil(this.destroy$)
      )
      .subscribe(searchTerm => {
        this.filters.search = searchTerm;
        this.loadUsers();
      });
  }

  loadUsers() {
    this.loadingService.show();

    this.userService.getUsers(this.filters).subscribe({
      next: (response) => {
        this.users = response.results;
        this.loadingService.hide();
      },
      error: (error) => {
        console.error('Erro ao carregar usuários:', error);
        this.errorHandler.showError(error, 'Erro ao carregar usuários');
        this.loadingService.hide();
      }
    });
  }

  onSearchInput(event: Event) {
    const target = event.target as HTMLInputElement;
    this.searchSubject.next(target.value);
  }

  applyFilters() {
    this.loadUsers();
  }

  createUser() {
    this.router.navigate(['/users/new']);
  }

  viewUser(userId: number) {
    this.router.navigate(['/users', userId, 'edit']);
  }

  getUserRoleClass(role: string): string {
    return this.userRoleService.getUserRoleClass(role);
  }

  getUserRoleLabel(role: string): string {
    return this.userRoleService.getUserRoleLabel(role);
  }
}
