import { Routes } from '@angular/router';
import { AppLayout } from './layout/component/app.layout';
import { Dashboard } from './features/dashboard/dashboard';
import { Cavaletes } from './features/cavaletes/cavaletes';
import { Notfound } from './pages/not-found/not-found';
import { authGuard } from './core/guards/auth-guard';
import { Login } from './features/login/login';

export const routes: Routes = [
    {
        path: '',
        component: AppLayout,
        children: [
            { path: '', component: Dashboard, canActivate: [authGuard] },
            { path: 'cavaletes', component: Cavaletes, canActivate: [authGuard] },
        ]
    },
    { path: 'login', component: Login },
    { path: 'notfound', component: Notfound },
    { path: '**', redirectTo: '/notfound' }
];
