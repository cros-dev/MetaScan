import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { CavaleteService } from '../../../cavaletes/services/cavalete.service';
import { UserService } from '../../../users/services/user.service';
import { LoadingService } from '../../../../shared/services/loading.service';

@Component({
  selector: 'app-dashboard-content',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard-content.html',
  styleUrl: './dashboard-content.scss'
})
export class DashboardContent implements OnInit {
  stats = {
    totalCavaletes: 0,
    totalUsers: 0,
    assignedCavaletes: 0,
    uniqueProducts: 0
  };

  constructor(
    private cavaleteService: CavaleteService,
    private userService: UserService,
    private loadingService: LoadingService
  ) {}

  ngOnInit() {
    this.loadStats();
  }

  private loadStats() {
    this.loadingService.show();

    this.cavaleteService.getCavaletes().subscribe({
      next: (response) => {
        this.stats.totalCavaletes = response.count;
        this.stats.assignedCavaletes = response.results.filter(c => c.status === 'assigned').length;
        this.loadingService.hide();
      },
      error: (error) => {
        console.error('Erro ao carregar estatísticas de cavaletes:', error);
        this.loadingService.hide();
      }
    });

    this.userService.getUsers().subscribe({
      next: (response) => {
        this.stats.totalUsers = response.count;
      },
      error: (error) => {
        console.error('Erro ao carregar estatísticas de usuários:', error);
      }
    });

    this.cavaleteService.getProductStats().subscribe({
      next: (response) => {
        this.stats.uniqueProducts = response.unique_products;
      },
      error: (error) => {
        console.error('Erro ao carregar estatísticas de produtos:', error);
      }
    });
  }
}
