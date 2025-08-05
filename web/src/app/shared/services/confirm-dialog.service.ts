import { Injectable, Injector } from '@angular/core';
import { ConfirmationService } from 'primeng/api';
import { ConfirmDialogConfig, ConfirmDialogPosition } from '../components/confirm-dialog/confirm-dialog.component';

export interface ConfirmDialogCallbackConfig extends ConfirmDialogConfig {
  accept?: () => void;
  reject?: () => void;
}

@Injectable({ providedIn: 'root' })
export class ConfirmDialogService {
  private confirmationService: ConfirmationService;

  constructor(private injector: Injector) {
    this.confirmationService = this.injector.get(ConfirmationService);
  }

  confirm(config: ConfirmDialogConfig, position: ConfirmDialogPosition = 'center'): Promise<boolean> {
    return new Promise((resolve) => {
      this.confirmationService.confirm({
        message: config.message,
        header: config.header || 'Confirmação',
        icon: config.icon || 'pi pi-exclamation-triangle',
        acceptLabel: config.acceptLabel || 'Sim',
        rejectLabel: config.rejectLabel || 'Não',
        acceptIcon: config.acceptIcon || 'pi pi-check',
        rejectIcon: config.rejectIcon || 'pi pi-times',
        acceptButtonStyleClass: config.acceptButtonStyleClass || 'p-button-danger',
        rejectButtonStyleClass: config.rejectButtonStyleClass || 'p-button-secondary',
        position: position,
        accept: () => resolve(true),
        reject: () => resolve(false)
      });
    });
  }

  confirmWithCallback(config: ConfirmDialogCallbackConfig, position: ConfirmDialogPosition = 'center'): void {
    this.confirmationService.confirm({
      message: config.message,
      header: config.header || 'Confirmação',
      icon: config.icon || 'pi pi-exclamation-triangle',
      acceptLabel: config.acceptLabel || 'Sim',
      rejectLabel: config.rejectLabel || 'Não',
      acceptIcon: config.acceptIcon || 'pi pi-check',
      rejectIcon: config.rejectIcon || 'pi pi-times',
      acceptButtonStyleClass: config.acceptButtonStyleClass || 'p-button-danger',
      rejectButtonStyleClass: config.rejectButtonStyleClass || 'p-button-secondary',
      position: position,
      accept: config.accept,
      reject: config.reject
    });
  }

  confirmLogout(): Promise<boolean> {
    return this.confirm({
      message: 'Tem certeza que deseja sair?',
      header: 'Confirmar Logout',
      icon: 'pi pi-sign-out',
      acceptLabel: 'Sim, sair',
      rejectLabel: 'Cancelar'
    }, 'topright');
  }

  confirmSessionExpired(): Promise<boolean> {
    return this.confirm({
      message: 'Sua sessão expirou. Deseja fazer login novamente?',
      header: 'Sessão Expirada',
      icon: 'pi pi-exclamation-triangle',
      acceptLabel: 'Sim, fazer login',
      rejectLabel: 'Cancelar',
      acceptButtonStyleClass: 'p-button-primary'
    }, 'center');
  }
}
