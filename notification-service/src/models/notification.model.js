const { v4: uuidv4 } = require('uuid');

const NotificationChannel = {
  EMAIL: 'email',
  SMS: 'sms',
  PUSH: 'push',
};

const NotificationStatus = {
  PENDING: 'pending',
  SENT: 'sent',
  DELIVERED: 'delivered',
  FAILED: 'failed',
  RETRYING: 'retrying',
};

const NotificationPriority = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  URGENT: 'urgent',
};

class Notification {
  constructor({ userId, channel, subject, body, templateId = null, metadata = {}, priority = NotificationPriority.MEDIUM }) {
    this.id = uuidv4();
    this.userId = userId;
    this.channel = channel;
    this.subject = subject;
    this.body = body;
    this.templateId = templateId;
    this.metadata = metadata;
    this.priority = priority;
    this.status = NotificationStatus.PENDING;
    this.retryCount = 0;
    this.maxRetries = 3;
    this.createdAt = new Date();
    this.sentAt = null;
    this.deliveredAt = null;
    this.failureReason = null;
  }

  markSent() {
    this.status = NotificationStatus.SENT;
    this.sentAt = new Date();
  }

  markDelivered() {
    this.status = NotificationStatus.DELIVERED;
    this.deliveredAt = new Date();
  }

  markFailed(reason) {
    if (this.retryCount < this.maxRetries) {
      this.status = NotificationStatus.RETRYING;
      this.retryCount++;
    } else {
      this.status = NotificationStatus.FAILED;
    }
    this.failureReason = reason;
  }

  canRetry() {
    return this.retryCount < this.maxRetries;
  }

  toJSON() {
    return {
      id: this.id,
      userId: this.userId,
      channel: this.channel,
      subject: this.subject,
      body: this.body,
      templateId: this.templateId,
      metadata: this.metadata,
      priority: this.priority,
      status: this.status,
      retryCount: this.retryCount,
      createdAt: this.createdAt.toISOString(),
      sentAt: this.sentAt ? this.sentAt.toISOString() : null,
      deliveredAt: this.deliveredAt ? this.deliveredAt.toISOString() : null,
      failureReason: this.failureReason,
    };
  }
}

module.exports = { Notification, NotificationChannel, NotificationStatus, NotificationPriority };

