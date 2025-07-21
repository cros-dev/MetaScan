import { Routes } from '@angular/router';
import { AppLayout } from './layout/component/app.layout';
import { Dashboard } from './features/dashboard/dashboard';
import { Cavaletes } from './features/cavaletes/cavaletes';
import { Notfound } from './pages/not-found/not-found';

export const routes: Routes = [
    {
        path: '',
        component: AppLayout,
        children: [
            { path: '', component: Dashboard },
            { path: 'cavaletes', component: Cavaletes },
        ]
    },
    { path: 'notfound', component: Notfound },
    { path: '**', redirectTo: '/notfound' }
];
