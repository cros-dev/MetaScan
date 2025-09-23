import {Component, OnInit} from '@angular/core';
import {RouterOutlet} from '@angular/router';
import {ConfirmDialog} from 'primeng/confirmdialog';
import {MenuAutoCollapseService} from './layout/services/menu-auto-collapse.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, ConfirmDialog],
  template: `
    <p-confirmDialog></p-confirmDialog>
    <router-outlet></router-outlet>
  `
})
export class App implements OnInit {
  constructor(private menuAutoCollapseService: MenuAutoCollapseService) {}

  ngOnInit() {
    this.menuAutoCollapseService.ngOnInit();
  }
}
