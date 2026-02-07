const { DeliveryLog } = require('../models/delivery-log.model');

class DeliveryService {
  constructor() {
    this.logs = [];
  }

  addLog(logData) {
    const log = new DeliveryLog(logData);
    this.logs.push(log);
    return log;
  }

  getLogsByNotification(notificationId) {
    return this.logs.filter(l => l.notificationId === notificationId);
  }

  getLogsByChannel(channel) {
    return this.logs.filter(l => l.channel === channel);
  }

  getLogsByStatus(status) {
    return this.logs.filter(l => l.status === status);
  }

  getDeliveryRate() {
    if (this.logs.length === 0) return 100;
    const delivered = this.logs.filter(l => l.status === 'sent' || l.status === 'delivered').length;
    return Math.round((delivered / this.logs.length) * 100 * 100) / 100;
  }

  getStats() {
    const channelStats = {};
    for (const log of this.logs) {
      if (!channelStats[log.channel]) {
        channelStats[log.channel] = { total: 0, sent: 0, failed: 0 };
      }
      channelStats[log.channel].total++;
      if (log.status === 'sent' || log.status === 'delivered') {
        channelStats[log.channel].sent++;
      } else if (log.status === 'failed') {
        channelStats[log.channel].failed++;
      }
    }
    return {
      totalLogs: this.logs.length,
      deliveryRate: this.getDeliveryRate(),
      channelStats,
    };
  }
}

module.exports = { DeliveryService };

