const { v4: uuidv4 } = require('uuid');

class DeliveryLog {
  constructor({ notificationId, channel, status, provider, responseCode = null, responseMessage = null }) {
    this.id = uuidv4();
    this.notificationId = notificationId;
    this.channel = channel;
    this.status = status;
    this.provider = provider;
    this.responseCode = responseCode;
    this.responseMessage = responseMessage;
    this.timestamp = new Date();
  }

  toJSON() {
    return {
      id: this.id,
      notificationId: this.notificationId,
      channel: this.channel,
      status: this.status,
      provider: this.provider,
      responseCode: this.responseCode,
      responseMessage: this.responseMessage,
      timestamp: this.timestamp.toISOString(),
    };
  }
}

module.exports = { DeliveryLog };

