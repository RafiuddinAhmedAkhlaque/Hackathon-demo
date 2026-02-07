/**
 * Push notification provider - simulates sending push notifications.
 */
class PushProvider {
  constructor() {
    this.name = 'push';
    this.sentNotifications = [];
  }

  async send({ deviceToken, title, body, data = {} }) {
    if (!deviceToken || !deviceToken.trim()) {
      throw new Error('Device token is required');
    }
    if (!title || !title.trim()) {
      throw new Error('Push notification title is required');
    }
    if (!body || !body.trim()) {
      throw new Error('Push notification body is required');
    }

    const result = {
      success: true,
      messageId: `push-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      provider: this.name,
      timestamp: new Date(),
    };

    this.sentNotifications.push({ deviceToken, title, body, data, ...result });
    return result;
  }

  getSentNotifications() {
    return this.sentNotifications;
  }

  clearSentNotifications() {
    this.sentNotifications = [];
  }
}

module.exports = { PushProvider };

