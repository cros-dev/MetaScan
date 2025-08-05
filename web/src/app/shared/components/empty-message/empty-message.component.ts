import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-empty-message',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="flex flex-col items-center justify-center p-8 text-center">
      <i class="pi pi-inbox text-4xl text-surface-400 mb-4"></i>
      <h3 class="text-lg font-medium text-surface-600 dark:text-surface-300 mb-2">{{ title }}</h3>
      <p class="text-surface-500 dark:text-surface-400">{{ message }}</p>
      @if (showAction && actionLabel) {
        <div class="mt-4">
          <ng-content select="[action]"></ng-content>
        </div>
      }
    </div>
  `,
  styles: []
})
export class EmptyMessageComponent {
  @Input() title: string = 'Nenhum item encontrado';
  @Input() message: string = 'Não há dados para exibir no momento.';
  @Input() showAction: boolean = false;
  @Input() actionLabel: string = '';
}
