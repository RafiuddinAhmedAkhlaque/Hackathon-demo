const { expect } = require('chai');
const { EmailProvider } = require('../providers/email.provider');
const { SmsProvider } = require('../providers/sms.provider');
const { PushProvider } = require('../providers/push.provider');

describe('EmailProvider', () => {
  let provider;

  beforeEach(() => {
    provider = new EmailProvider();
  });

  it('should send email successfully', async () => {
    const result = await provider.send({
      to: 'user@example.com',
      subject: 'Test',
      body: 'Test body',
    });
    expect(result.success).to.be.true;
    expect(result.messageId).to.be.a('string');
  });

  it('should reject empty recipient', async () => {
    try {
      await provider.send({ to: '', subject: 'Test', body: 'Body' });
      expect.fail('Should have thrown');
    } catch (error) {
      expect(error.message).to.include('recipient');
    }
  });

  it('should reject empty subject', async () => {
    try {
      await provider.send({ to: 'user@test.com', subject: '', body: 'Body' });
      expect.fail('Should have thrown');
    } catch (error) {
      expect(error.message).to.include('subject');
    }
  });

  it('should track sent emails', async () => {
    await provider.send({ to: 'a@test.com', subject: 'S1', body: 'B1' });
    await provider.send({ to: 'b@test.com', subject: 'S2', body: 'B2' });
    expect(provider.getSentEmails()).to.have.length(2);
  });
});

describe('SmsProvider', () => {
  let provider;

  beforeEach(() => {
    provider = new SmsProvider();
  });

  it('should send SMS successfully', async () => {
    const result = await provider.send({ to: '+1234567890', body: 'Hello!' });
    expect(result.success).to.be.true;
    expect(result.segments).to.equal(1);
  });

  it('should calculate segments for long messages', async () => {
    const longBody = 'A'.repeat(320);
    const result = await provider.send({ to: '+1234567890', body: longBody });
    expect(result.segments).to.equal(2);
  });

  it('should reject empty phone number', async () => {
    try {
      await provider.send({ to: '', body: 'Hello' });
      expect.fail('Should have thrown');
    } catch (error) {
      expect(error.message).to.include('Phone number');
    }
  });
});

describe('PushProvider', () => {
  let provider;

  beforeEach(() => {
    provider = new PushProvider();
  });

  it('should send push notification successfully', async () => {
    const result = await provider.send({
      deviceToken: 'token-123',
      title: 'Alert',
      body: 'New notification',
    });
    expect(result.success).to.be.true;
  });

  it('should reject empty device token', async () => {
    try {
      await provider.send({ deviceToken: '', title: 'Test', body: 'Body' });
      expect.fail('Should have thrown');
    } catch (error) {
      expect(error.message).to.include('Device token');
    }
  });

  it('should reject empty title', async () => {
    try {
      await provider.send({ deviceToken: 'token', title: '', body: 'Body' });
      expect.fail('Should have thrown');
    } catch (error) {
      expect(error.message).to.include('title');
    }
  });
});

