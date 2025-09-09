import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  notifications: any[] = [];

  showSuccess(message: string): void {
    const notification = {
      id: Date.now().toString(),
      type: 'success',
      message: message
    };
    this.notifications.push(notification);

    setTimeout(() => {
      this.removeNotification(notification.id);
    }, 3000);
  }

  showError(message: string): void {
    const notification = {
      id: Date.now().toString(),
      type: 'error',
      message: message
    };
    this.notifications.push(notification);

    setTimeout(() => {
      this.removeNotification(notification.id);
    }, 5000);
  }

  showWarning(message: string): void {
    const notification = {
      id: Date.now().toString(),
      type: 'warning',
      message: message
    };
    this.notifications.push(notification);

    setTimeout(() => {
      this.removeNotification(notification.id);
    }, 4000);
  }

  showInfo(message: string): void {
    const notification = {
      id: Date.now().toString(),
      type: 'info',
      message: message
    };
    this.notifications.push(notification);

    setTimeout(() => {
      this.removeNotification(notification.id);
    }, 3000);
  }

  removeNotification(id: string): void {
    this.notifications = this.notifications.filter(notification => notification.id !== id);
  }

  clearAll(): void {
    this.notifications = [];
  }
}
