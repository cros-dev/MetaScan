import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { ProductResponse } from '../models/product.model';
import {NotificationService} from '../../../shared/services/notification.service';

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private apiUrl = `${environment.apiUrl}`;

  constructor(
    private http: HttpClient,
    private notificationService: NotificationService
  ) {}

  /**
   * Consulta produto na Sankhya pelo código
   * @param code Código do produto
   * @returns Observable com dados completos do produto
   */
  getProduct(code: string): Observable<ProductResponse> {
    return this.http.get<ProductResponse>(`${this.apiUrl}sankhya/product/${code}/`);
  }

  /**
   * Trata erros de consulta de produto de forma centralizada
   * @param error Erro recebido da API
   * @param fallbackCallback Callback executado após mostrar a mensagem de erro
   */
  handleProductError(error: any, fallbackCallback?: () => void): void {
    console.error('Erro ao carregar produto:', error);

    if (error.status === 502) {
      this.notificationService.showError('Erro de conexão com a Sankhya. Tente novamente em alguns segundos.');
    } else if (error.status === 503) {
      this.notificationService.showError('Serviço temporariamente indisponível. Tente novamente.');
    } else if (error.status === 504) {
      this.notificationService.showError('Timeout na consulta. Tente novamente.');
    } else {
      this.notificationService.showError('Produto não encontrado');
    }

    if (fallbackCallback) {
      fallbackCallback();
    }
  }

  /**
   * Formata data para exibição
   * @param dateString String de data no formato brasileiro DD/MM/YYYY HH:mm:ss
   * @returns Data formatada em pt-BR ou string original se inválida
   */
  formatDate(dateString: string | undefined): string {
    if (!dateString) return '';

    try {
      const parts = dateString.split(' ');
      const datePart = parts[0];
      const timePart = parts[1] || '00:00:00';

      const [day, month, year] = datePart.split('/');
      const [hours, minutes, seconds] = timePart.split(':');

      const date = new Date(
        parseInt(year),
        parseInt(month) - 1,
        parseInt(day),
        parseInt(hours),
        parseInt(minutes),
        parseInt(seconds)
      );

      return date.toLocaleDateString('pt-BR');
    } catch {
      return dateString;
    }
  }

  /**
   * Seleciona apenas o valor do card clicado
   * @param event Evento de clique do mouse
   */
  selectCardText(event: Event): void {
    const target = event.currentTarget as HTMLElement;

    const valueElement = target.querySelector('.detail-value') as HTMLElement;

    if (valueElement) {
      const range = document.createRange();
      range.selectNodeContents(valueElement);

      const selection = window.getSelection();
      if (selection) {
        selection.removeAllRanges();
        selection.addRange(range);
      }
    }

    event.preventDefault();
  }
}
