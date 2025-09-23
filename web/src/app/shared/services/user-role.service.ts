import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UserRoleService {

  constructor() { }

  getUserRoleClass(role: string): string {
    switch (role) {
      case 'admin':
        return 'badge';
      case 'manager':
        return 'badge';
      case 'auditor':
        return 'badge';
      default:
        return 'badge badge-secondary';
    }
  }

  getUserRoleLabel(role: string): string {
    switch (role) {
      case 'admin':
        return 'Administrador';
      case 'manager':
        return 'Gestor';
      case 'auditor':
        return 'Conferente';
      default:
        return role;
    }
  }

  getAvatarInitial(email: string): string {
    return email ? email.charAt(0).toUpperCase() : '';
  }
}
