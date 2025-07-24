import { Routes } from '@angular/router';
import { AppLayout } from './layout/component/app.layout';
import { Dashboard } from './features/dashboard/dashboard';
import { Notfound } from './pages/not-found/not-found';
import { authGuard } from './core/guards/auth-guard';
import { LoginPage } from './pages/login/login.page';
import { CavaleteListPage } from './pages/cavalete/cavalete-list.page';
import { CavaleteDetailPage } from './pages/cavalete/cavalete-detail.page';

export const routes: Routes = [
  {
    path: '',
    component: AppLayout,
    children: [
      { path: '', component: Dashboard, canActivate: [authGuard] },
      { path: 'cavaletes', component: CavaleteListPage, canActivate: [authGuard] },
      { path: 'cavaletes/:code', component: CavaleteDetailPage, canActivate: [authGuard] }
    ]
  },
  { path: 'login', component: LoginPage },
  { path: 'notfound', component: Notfound },
  { path: '**', redirectTo: '/notfound' }
];
