const { expect } = require('chai');
const { NotificationService } = require('../services/notification.service');
const { EmailProvider } = require('../providers/email.provider');
const { SmsProvider } = require('../providers/sms.provider');
const { PushProvider } = require('../providers/push.provider');
const { NotificationChannel, NotificationStatus } = require('../models/notification.model');

describe('NotificationService', () => {
  let service;
  let emailProvider;
  let smsProvider;
  let pushProvider;

  beforeEach(() => {
    emailProvider = new EmailProvider();
    smsProvider = new SmsProvider();
    pushProvider = new PushProvider();
    service = new NotificationService(emailProvider, smsProvider, pushProvider);
  });

  describe('sendNotification', () => {
    it('should send email notification successfully', async () => {
      const result = await service.sendNotification({
        userId: 'user-1',
        channel: NotificationChannel.EMAIL,
        subject: 'Order Confirmation',
        body: 'Your order has been confirmed.',
        metadata: { email: 'user@example.com' },
      });

      expect(result.status).to.equal(NotificationStatus.SENT);
      expect(result.userId).to.equal('user-1');
      expect(emailProvider.getSentEmails()).to.have.length(1);
    });

    it('should send SMS notification successfully', async () => {
      const result = await service.sendNotification({
        userId: 'user-1',
        channel: NotificationChannel.SMS,
        subject: 'Order Update',
        body: 'Your order has shipped!',
        metadata: { phone: '+1234567890' },
      });

      expect(result.status).to.equal(NotificationStatus.SENT);
      expect(smsProvider.getSentMessages()).to.have.length(1);
    });

    it('should send push notification successfully', async () => {
      const result = await service.sendNotification({
        userId: 'user-1',
        channel: NotificationChannel.PUSH,
        subject: 'Sale Alert',
        body: '50% off today!',
        metadata: { deviceToken: 'device-abc123' },
      });

      expect(result.status).to.equal(NotificationStatus.SENT);
      expect(pushProvider.getSentNotifications()).to.have.length(1);
    });

    it('should reject missing userId', async () => {
      try {
        await service.sendNotification({
          channel: NotificationChannel.EMAIL,
          body: 'test',
        });
        expect.fail('Should have thrown');
      } catch (error) {
        expect(error.message).to.include('User ID');
      }
    });

    it('should reject invalid channel', async () => {
      try {
        await service.sendNotification({
          userId: 'user-1',
          channel: 'telegram',
          body: 'test',
        });
        expect.fail('Should have thrown');
      } catch (error) {
        expect(error.message).to.include('Invalid channel');
      }
    });

    it('should reject missing body', async () => {
      try {
        await service.sendNotification({
          userId: 'user-1',
          channel: NotificationChannel.EMAIL,
        });
        expect.fail('Should have thrown');
      } catch (error) {
        expect(error.message).to.include('Body');
      }
    });
  });

  describe('getNotificationsByUser', () => {
    it('should return notifications for a user', async () => {
      await service.sendNotification({
        userId: 'user-1',
        channel: NotificationChannel.EMAIL,
        subject: 'Test 1',
        body: 'Body 1',
      });
      await service.sendNotification({
        userId: 'user-1',
        channel: NotificationChannel.SMS,
        subject: 'Test 2',
        body: 'Body 2',
      });
      await service.sendNotification({
        userId: 'user-2',
        channel: NotificationChannel.EMAIL,
        subject: 'Test 3',
        body: 'Body 3',
      });

      const notifications = service.getNotificationsByUser('user-1');
      expect(notifications).to.have.length(2);
    });
  });

  describe('getDeliveryLogs', () => {
    it('should track delivery logs', async () => {
      const notification = await service.sendNotification({
        userId: 'user-1',
        channel: NotificationChannel.EMAIL,
        subject: 'Test',
        body: 'Test body',
      });

      const logs = service.getDeliveryLogs(notification.id);
      expect(logs).to.have.length(1);
      expect(logs[0].status).to.equal('sent');
    });
  });

  describe('getStats', () => {
    it('should return correct statistics', async () => {
      await service.sendNotification({
        userId: 'user-1',
        channel: NotificationChannel.EMAIL,
        subject: 'Test',
        body: 'Body',
      });
      await service.sendNotification({
        userId: 'user-2',
        channel: NotificationChannel.SMS,
        subject: 'Test',
        body: 'Body',
      });

      const stats = service.getStats();
      expect(stats.total).to.equal(2);
      expect(stats.sent).to.equal(2);
      expect(stats.failed).to.equal(0);
    });
  });
});

