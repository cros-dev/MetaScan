import { Component } from '@angular/core';

@Component({
  selector: 'app-notfound',
  standalone: true,
  template: `
    <div class="flex flex-col items-center justify-center min-h-screen p-4">
      <div class="text-center">
        <i class="pi pi-exclamation-triangle text-6xl text-warning-500 mb-4"></i>
        <h1 class="text-3xl font-bold text-surface-900 dark:text-surface-0 mb-2">Página não encontrada</h1>
        <p class="text-surface-600 dark:text-surface-400 text-lg">O endereço acessado não existe.</p>
      </div>
    </div>
  `
})
export class Notfound {}
