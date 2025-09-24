import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UserService } from '../../services/user.service';
import { User } from '../../models/user.model';
import { CavaleteService } from '../../../cavaletes/services/cavalete.service';
import { NotificationService } from '../../../../shared/services/notification.service';
import { LoadingService } from '../../../../shared/services/loading.service';
import { UserRoleService } from '../../../../shared/services/user-role.service';

@Component({
  selector: 'app-user-assignment',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './user-assignment.html',
  styleUrl: './user-assignment.scss'
})
export class UserAssignment implements OnInit {
  @Input() cavaleteId!: number;
  @Input() currentUser: User | null | undefined = null;
  @Output() closeModal = new EventEmitter<void>();

  users: User[] = [];
  assigning = false;
  showUserSelection = false;
  selectedUserId: number | null = null;

  constructor(
    private userService: UserService,
    private cavaleteService: CavaleteService,
    private notificationService: NotificationService,
    private loadingService: LoadingService,
    private userRoleService: UserRoleService
  ) {}

  ngOnInit() {
    this.loadUsers();
  }

  loadUsers() {
    this.loadingService.show();

    this.userService.getUsers({ is_active: true }).subscribe({
      next: (response) => {
        this.users = response.results;
        this.loadingService.hide();
      },
      error: (error) => {
        console.error('Erro ao carregar usuários:', error);
        this.notificationService.showError('Erro ao carregar usuários');
        this.loadingService.hide();
      }
    });
  }

  selectUser(userId: number) {
    this.selectedUserId = userId;
    this.showUserSelection = false;
  }

  getSelectedUser(): User | null {
    if (!this.selectedUserId) return null;
    return this.users.find(user => user.id === this.selectedUserId) || null;
  }

  confirmAssignment() {
    if (!this.cavaleteId || !this.selectedUserId) return;

    this.assigning = true;
    this.loadingService.show();

    this.cavaleteService.assignUser(this.cavaleteId, { user_id: this.selectedUserId }).subscribe({
      next: (response) => {
        this.notificationService.showSuccess(response.detail);
        this.assigning = false;
        this.loadingService.hide();
        this.closeModalAction();
      },
      error: (error) => {
        console.error('Erro ao atribuir usuário:', error);
        this.notificationService.showError('Erro ao atribuir usuário');
        this.assigning = false;
        this.loadingService.hide();
      }
    });
  }

  releaseCavalete() {
    if (!this.cavaleteId) return;

    this.assigning = true;
    this.loadingService.show();
    this.showUserSelection = false;

    this.cavaleteService.assignUser(this.cavaleteId, { user_id: undefined }).subscribe({
      next: (response) => {
        this.notificationService.showSuccess(response.detail);
        this.assigning = false;
        this.loadingService.hide();
        this.closeModalAction();
      },
      error: (error) => {
        console.error('Erro ao liberar cavalete:', error);
        this.notificationService.showError('Erro ao liberar cavalete');
        this.assigning = false;
        this.loadingService.hide();
      }
    });
  }

  closeModalAction() {
    this.closeModal.emit();
  }

  getUserRoleLabel(role: string): string {
    return this.userRoleService.getUserRoleLabel(role);
  }
}
