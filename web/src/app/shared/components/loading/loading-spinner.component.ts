import { Component, Input } from '@angular/core';
import { ProgressSpinnerModule } from 'primeng/progressspinner';

@Component({
  selector: 'app-loading-spinner',
  standalone: true,
  imports: [ProgressSpinnerModule],
  template: `
    @if (show) {
      <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
        <p-progress-spinner ariaLabel="Carregando" [style]="{width: '60px', height: '60px'}" strokeWidth="4" animationDuration=".8s"></p-progress-spinner>
      </div>
    }
  `
})
export class LoadingSpinnerComponent {
  @Input() show = false;
}
