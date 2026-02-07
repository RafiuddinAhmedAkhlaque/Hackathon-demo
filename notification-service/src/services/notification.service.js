const { Notification, NotificationChannel, NotificationStatus } = require('../models/notification.model');
const { DeliveryLog } = require('../models/delivery-log.model');

class NotificationService {
  constructor(emailProvider, smsProvider, pushProvider) {
    this.emailProvider = emailProvider;
    this.smsProvider = smsProvider;
    this.pushProvider = pushProvider;
    this.notifications = new Map();
    this.deliveryLogs = [];
  }

  async sendNotification({ userId, channel, subject, body, templateId, metadata, priority }) {
    this.validateNotificationRequest({ userId, channel, body });

    const notification = new Notification({ userId, channel, subject, body, templateId, metadata, priority });
    this.notifications.set(notification.id, notification);

    try {
      const result = await this.dispatchToProvider(notification);
      notification.markSent();

      this.deliveryLogs.push(new DeliveryLog({
        notificationId: notification.id,
        channel,
        status: 'sent',
        provider: result.provider,
        responseCode: 200,
        responseMessage: result.messageId,
      }));

      return notification;
    } catch (error) {
      notification.markFailed(error.message);

      this.deliveryLogs.push(new DeliveryLog({
        notificationId: notification.id,
        channel,
        status: 'failed',
        provider: channel,
        responseCode: 500,
        responseMessage: error.message,
      }));

      return notification;
    }
  }

  async retryNotification(notificationId) {
    const notification = this.notifications.get(notificationId);
    if (!notification) {
      throw new Error(`Notification '${notificationId}' not found`);
    }

    if (!notification.canRetry()) {
      throw new Error('Maximum retry attempts reached');
    }

    if (notification.status !== NotificationStatus.RETRYING && notification.status !== NotificationStatus.FAILED) {
      throw new Error('Only failed or retrying notifications can be retried');
    }

    try {
      const result = await this.dispatchToProvider(notification);
      notification.markSent();
      return notification;
    } catch (error) {
      notification.markFailed(error.message);
      return notification;
    }
  }

  getNotification(id) {
    return this.notifications.get(id) || null;
  }

  getNotificationsByUser(userId) {
    return Array.from(this.notifications.values()).filter(n => n.userId === userId);
  }

  getNotificationsByStatus(status) {
    return Array.from(this.notifications.values()).filter(n => n.status === status);
  }

  getDeliveryLogs(notificationId) {
    if (notificationId) {
      return this.deliveryLogs.filter(l => l.notificationId === notificationId);
    }
    return this.deliveryLogs;
  }

  getStats() {
    const all = Array.from(this.notifications.values());
    return {
      total: all.length,
      pending: all.filter(n => n.status === NotificationStatus.PENDING).length,
      sent: all.filter(n => n.status === NotificationStatus.SENT).length,
      delivered: all.filter(n => n.status === NotificationStatus.DELIVERED).length,
      failed: all.filter(n => n.status === NotificationStatus.FAILED).length,
      retrying: all.filter(n => n.status === NotificationStatus.RETRYING).length,
    };
  }

  async dispatchToProvider(notification) {
    switch (notification.channel) {
      case NotificationChannel.EMAIL:
        return this.emailProvider.send({
          to: notification.metadata.email || `${notification.userId}@example.com`,
          subject: notification.subject,
          body: notification.body,
        });
      case NotificationChannel.SMS:
        return this.smsProvider.send({
          to: notification.metadata.phone || '+10000000000',
          body: notification.body,
        });
      case NotificationChannel.PUSH:
        return this.pushProvider.send({
          deviceToken: notification.metadata.deviceToken || 'default-token',
          title: notification.subject,
          body: notification.body,
          data: notification.metadata,
        });
      default:
        throw new Error(`Unsupported channel: ${notification.channel}`);
    }
  }

  validateNotificationRequest({ userId, channel, body }) {
    if (!userId) throw new Error('User ID is required');
    if (!channel) throw new Error('Channel is required');
    if (!body) throw new Error('Body is required');

    const validChannels = Object.values(NotificationChannel);
    if (!validChannels.includes(channel)) {
      throw new Error(`Invalid channel: ${channel}. Must be one of: ${validChannels.join(', ')}`);
    }
  }
}

module.exports = { NotificationService };

