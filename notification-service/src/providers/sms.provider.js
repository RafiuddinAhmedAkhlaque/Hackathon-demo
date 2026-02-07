/**
 * SMS provider - simulates sending SMS messages.
 */
class SmsProvider {
  constructor() {
    this.name = 'sms';
    this.sentMessages = [];
    this.maxMessageLength = 160;
  }

  async send({ to, body }) {
    if (!to || !to.trim()) {
      throw new Error('Phone number is required');
    }
    if (!body || !body.trim()) {
      throw new Error('SMS body is required');
    }

    const segments = Math.ceil(body.length / this.maxMessageLength);

    const result = {
      success: true,
      messageId: `sms-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      provider: this.name,
      segments,
      timestamp: new Date(),
    };

    this.sentMessages.push({ to, body, ...result });
    return result;
  }

  getSentMessages() {
    return this.sentMessages;
  }

  clearSentMessages() {
    this.sentMessages = [];
  }
}

module.exports = { SmsProvider };

