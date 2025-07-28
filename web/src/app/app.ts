import {Component} from '@angular/core';
import {RouterOutlet} from '@angular/router';
import {ConfirmDialog} from 'primeng/confirmdialog';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, ConfirmDialog],
  template: `
    <p-confirmDialog></p-confirmDialog>
    <router-outlet></router-outlet>
  `
})
export class App {
}
