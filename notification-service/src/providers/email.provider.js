/**
 * Email provider - simulates sending emails.
 */
class EmailProvider {
  constructor() {
    this.name = 'email';
    this.sentEmails = []; // Track sent emails for testing
  }

  async send({ to, subject, body, from = 'noreply@ecommerce.com' }) {
    if (!to || !to.trim()) {
      throw new Error('Email recipient is required');
    }
    if (!subject || !subject.trim()) {
      throw new Error('Email subject is required');
    }
    if (!body || !body.trim()) {
      throw new Error('Email body is required');
    }

    // Simulate email sending
    const result = {
      success: true,
      messageId: `email-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      provider: this.name,
      timestamp: new Date(),
    };

    this.sentEmails.push({ to, subject, body, from, ...result });
    return result;
  }

  getSentEmails() {
    return this.sentEmails;
  }

  clearSentEmails() {
    this.sentEmails = [];
  }
}

module.exports = { EmailProvider };

