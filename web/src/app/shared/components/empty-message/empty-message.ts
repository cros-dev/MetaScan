import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-empty-message',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './empty-message.html',
  styleUrl: './empty-message.scss'
})
export class EmptyMessage {
  @Input() title: string = 'Nenhum item encontrado';
  @Input() message: string = 'Não há dados para exibir no momento.';
  @Input() showAction: boolean = false;
  @Input() actionLabel: string = '';
}
