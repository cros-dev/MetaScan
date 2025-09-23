import { Injectable } from '@angular/core';
import { NotificationService } from '../services/notification.service';

@Injectable({
  providedIn: 'root'
})
export class ErrorHandlerUtil {
  constructor(private notificationService: NotificationService) {}

  /**
   * Mostra mensagem de erro específica da API ou uma mensagem padrão
   */
  showError(error: any, defaultMessage: string): void {
    let errorMessage = defaultMessage;

    if (error.error && typeof error.error === 'object') {
      const apiErrors = error.error;

      if (apiErrors.email && Array.isArray(apiErrors.email)) {
        errorMessage = apiErrors.email[0];
      }
      else if (apiErrors.first_name && Array.isArray(apiErrors.first_name)) {
        errorMessage = apiErrors.first_name[0];
      }
      else if (apiErrors.last_name && Array.isArray(apiErrors.last_name)) {
        errorMessage = apiErrors.last_name[0];
      }
      else if (apiErrors.role && Array.isArray(apiErrors.role)) {
        errorMessage = apiErrors.role[0];
      }
      else if (apiErrors.non_field_errors && Array.isArray(apiErrors.non_field_errors)) {
        errorMessage = apiErrors.non_field_errors[0];
      }
      else if (apiErrors.detail) {
        errorMessage = apiErrors.detail;
      }
    }
    else if (error.status === 0) {
      errorMessage = 'Erro de conexão. Verifique sua internet';
    }
    else if (error.status >= 500) {
      errorMessage = 'Erro interno do servidor. Tente novamente';
    }

    this.notificationService.showError(errorMessage);
  }
}
