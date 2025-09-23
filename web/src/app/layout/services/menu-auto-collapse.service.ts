import { Injectable, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { LayoutService } from './layout.service';

@Injectable({
  providedIn: 'root'
})
export class MenuAutoCollapseService implements OnInit {
  constructor(
    private router: Router,
    private layoutService: LayoutService
  ) {}

  ngOnInit() {
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe(() => {
        this.layoutService.collapseMenu();
      });
  }
}
