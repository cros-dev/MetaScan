import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NotificationService } from '../../services/notification.service';

@Component({
  selector: 'app-notification-container',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './notification-container.component.html',
  styleUrls: ['./notification-container.component.css']
})
export class NotificationContainerComponent {
  constructor(public notificationService: NotificationService) {}

  getNotificationClass(type: string): string {
    if (type === 'success') {
      return 'notification-success';
    }
    if (type === 'error') {
      return 'notification-error';
    }
    if (type === 'warning') {
      return 'notification-warning';
    }
    if (type === 'info') {
      return 'notification-info';
    }
    return 'notification-default';
  }

  getIconClass(type: string): string {
    if (type === 'success') {
      return 'pi pi-check-circle';
    }
    if (type === 'error') {
      return 'pi pi-times-circle';
    }
    if (type === 'warning') {
      return 'pi pi-exclamation-triangle';
    }
    if (type === 'info') {
      return 'pi pi-info-circle';
    }
    return 'pi pi-info';
  }

  removeNotification(id: string): void {
    this.notificationService.removeNotification(id);
  }
}
