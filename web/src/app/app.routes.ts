import { Routes } from '@angular/router';
import { AppLayout } from './layout/app.layout';
import { DashboardPage } from './features/dashboard/pages/dashboard.page';
import { CavaleteListPage } from './features/cavaletes/pages/cavalete-list.page';
import { CavaleteDetailPage } from './features/cavaletes/pages/cavalete-detail.page';
import { ProductViewPage } from './features/cavaletes/pages/product-view.page';
import { UserListPage } from './features/users/pages/user-list-page';
import { UserFormPage } from './features/users/pages/user-form-page';
import { Products } from './features/products/products';
import { ProductDetail } from './features/products/components/product-detail/product-detail';
import { Notfound } from './pages/not-found/not-found';
import { authGuard } from './core/guards/auth-guard';
import {LoginPage} from './features/login/pages/login.page';

export const routes: Routes = [
    {
        path: '',
        component: AppLayout,
        children: [
            { path: '', component: DashboardPage, canActivate: [authGuard] },
            { path: 'cavaletes', component: CavaleteListPage, canActivate: [authGuard] },
            { path: 'cavaletes/:id', component: CavaleteDetailPage, canActivate: [authGuard] },
            { path: 'cavaletes/:cavaleteId/products/:code/slots/:slotLocation', component: ProductViewPage, canActivate: [authGuard] },
            { path: 'products', component: Products, canActivate: [authGuard] },
            { path: 'products/:code', component: ProductDetail, canActivate: [authGuard] },
            { path: 'users', component: UserListPage, canActivate: [authGuard] },
            { path: 'users/new', component: UserFormPage, canActivate: [authGuard] },
            { path: 'users/:id/edit', component: UserFormPage, canActivate: [authGuard] },
        ]
    },
    { path: 'login', component: LoginPage },
    { path: 'notfound', component: Notfound },
    { path: '**', redirectTo: '/notfound' }
];
