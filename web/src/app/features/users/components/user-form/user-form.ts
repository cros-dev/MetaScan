import { Component, OnInit, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { UserService } from '../../services/user.service';
import { NotificationService } from '../../../../shared/services/notification.service';
import { LoadingService } from '../../../../shared/services/loading.service';
import { ErrorHandlerUtil } from '../../../../shared/utils/error-handler.util';
import { User } from '../../models/user.model';
import { ConfirmDialogService } from '../../../../shared/services/confirm-dialog.service';

@Component({
  selector: 'app-user-form',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './user-form.html',
  styleUrl: './user-form.scss'
})
export class UserFormComponent implements OnInit {
  @Input() isEditing = false;
  @Input() userId?: number;

  userForm!: FormGroup;
  currentUser: User | null = null;
  originalFormData: any = null;

  roleOptions = [
    { label: 'Administrador', value: 'admin' },
    { label: 'Gestor', value: 'manager' },
    { label: 'Conferente', value: 'auditor' }
  ];

  constructor(
    private fb: FormBuilder,
    private userService: UserService,
    private notificationService: NotificationService,
    private loadingService: LoadingService,
    private router: Router,
    private errorHandler: ErrorHandlerUtil,
    private confirmDialogService: ConfirmDialogService
  ) {}

  ngOnInit() {
    this.initializeForm();
    if (this.isEditing && this.userId) {
      this.loadUser();
    }

    setTimeout(() => {
      this.focusFirstName();
    }, 100);
  }

  private initializeForm() {
    this.userForm = this.fb.group({
      first_name: ['', [Validators.required]],
      last_name: ['', [Validators.required]],
      email: [''],
      role: ['auditor', Validators.required],
      is_active: [true]
    });

    if (!this.isEditing) {
      this.userForm.get('first_name')?.valueChanges.subscribe(() => {
        this.generateEmail();
      });

      this.userForm.get('last_name')?.valueChanges.subscribe(() => {
        this.generateEmail();
      });
    }
  }


  private loadUser() {
    if (!this.userId) return;

    this.loadingService.show();
    this.userService.getUser(this.userId).subscribe({
      next: (user) => {
        this.currentUser = user;
        this.userForm.patchValue({
          first_name: user.first_name || '',
          last_name: user.last_name || '',
          email: user.email,
          role: user.role,
          is_active: user.is_active
        });

        this.originalFormData = { ...this.userForm.value };

        this.loadingService.hide();
      },
      error: (error) => {
        console.error('Erro ao carregar usuário:', error);
        this.notificationService.showError('Erro ao carregar usuário');
        this.loadingService.hide();
        this.router.navigate(['/users']);
      }
    });
  }

  private generateEmail() {
    if (this.isEditing) return;

    const firstName = this.userForm.get('first_name')?.value?.toLowerCase().trim();
    const lastName = this.userForm.get('last_name')?.value?.toLowerCase().trim();

    if (firstName && lastName) {
      const cleanFirstName = this.removeAccents(firstName).replace(/[^a-z0-9]/g, '');
      const cleanLastName = this.removeAccents(lastName).replace(/[^a-z0-9]/g, '');

      const generatedEmail = `${cleanFirstName}.${cleanLastName}@metalaluminio.com.br`;
      this.userForm.get('email')?.setValue(generatedEmail, { emitEvent: false });
    }
  }

  private removeAccents(str: string): string {
    return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  private capitalizeFirstLetter(str: string): string {
    if (!str) return str;
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
  }

  onFirstNameInput(event: any) {
    if (!this.isEditing) {
      const value = event.target.value;
      const capitalized = this.capitalizeFirstLetter(value);
      this.userForm.get('first_name')?.setValue(capitalized, { emitEvent: false });
      this.generateEmail();
    }
  }

  onLastNameInput(event: any) {
    if (!this.isEditing) {
      const value = event.target.value;
      const capitalized = this.capitalizeFirstLetter(value);
      this.userForm.get('last_name')?.setValue(capitalized, { emitEvent: false });
      this.generateEmail();
    }
  }

  createUser() {
    if (this.userForm.valid) {
      this.loadingService.show();

      const formData = { ...this.userForm.value };

      if (!this.isEditing) {
        delete formData.email;
      }

      if (this.isEditing && this.userId) {
        this.userService.updateUser(this.userId, formData).subscribe({
          next: () => {
            this.notificationService.showSuccess('Usuário atualizado com sucesso!');
            this.loadingService.hide();
            this.router.navigate(['/users']);
          },
          error: (error) => {
            console.error('Erro ao atualizar usuário:', error);
            this.errorHandler.showError(error, 'Erro ao atualizar usuário');
            this.loadingService.hide();
          }
        });
      } else {
        this.userService.createUser(formData).subscribe({
          next: () => {
            this.notificationService.showSuccess('Usuário criado com sucesso!');
            this.loadingService.hide();
            this.router.navigate(['/users']);
          },
          error: (error) => {
            console.error('Erro ao criar usuário:', error);
            this.errorHandler.showError(error, 'Erro ao criar usuário');
            this.loadingService.hide();
          }
        });
      }
    } else {
      this.markFormGroupTouched();
    }
  }

  private markFormGroupTouched() {
    Object.keys(this.userForm.controls).forEach(key => {
      const control = this.userForm.get(key);
      control?.markAsTouched();
    });
  }

  hasError(): boolean {
    return false;
  }

  getErrorMessage(): string {
    return '';
  }

  hasFormChanges(): boolean {
    if (!this.isEditing || !this.originalFormData) {
      return true;
    }

    const currentData = this.userForm.value;
    return JSON.stringify(currentData) !== JSON.stringify(this.originalFormData);
  }

  private focusFirstName(): void {
    const firstNameInput = document.querySelector('input[formControlName="first_name"]') as HTMLInputElement;
    if (firstNameInput) {
      firstNameInput.focus();
    }
  }

  deleteUser() {
    if (this.userId) {
      this.confirmDialogService.confirm({
        message: `Tem certeza que deseja excluir o usuário ${this.currentUser?.first_name} ${this.currentUser?.last_name}? Esta ação não pode ser desfeita.`,
        header: 'Excluir Usuário',
        acceptLabel: 'Excluir',
        rejectLabel: 'Cancelar',
        acceptButtonStyleClass: 'p-button-danger',
        rejectButtonStyleClass: 'p-button-secondary'
      }).then((confirmed) => {
        if (confirmed) {
          this.loadingService.show();
          this.userService.deleteUser(this.userId!).subscribe({
            next: () => {
              this.notificationService.showSuccess('Usuário excluído com sucesso!');
              this.loadingService.hide();
              this.router.navigate(['/users']);
            },
            error: (error) => {
              console.error('Erro ao excluir usuário:', error);
              this.errorHandler.showError(error, 'Erro ao excluir usuário');
              this.loadingService.hide();
            }
          });
        }
      });
    }
  }
}
