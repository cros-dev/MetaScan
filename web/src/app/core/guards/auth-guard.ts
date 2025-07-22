import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { Router } from '@angular/router';

export const authGuard: CanActivateFn = () => {
  const token = localStorage.getItem('token');
  if (token) {
    return true;
  } else {
    const router = inject(Router);
    router.navigate(['/login']).then(() => {});
    return false;
  }
};
