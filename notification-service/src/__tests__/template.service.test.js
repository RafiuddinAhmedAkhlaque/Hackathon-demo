const { expect } = require('chai');
const { TemplateService } = require('../services/template.service');

describe('TemplateService', () => {
  let service;

  beforeEach(() => {
    service = new TemplateService();
  });

  describe('createTemplate', () => {
    it('should create a template successfully', () => {
      const template = service.createTemplate({
        name: 'order-confirmation',
        channel: 'email',
        subject: 'Order #{{orderNumber}} Confirmed',
        bodyTemplate: 'Hi {{userName}}, your order #{{orderNumber}} has been confirmed.',
        variables: ['userName', 'orderNumber'],
      });

      expect(template.name).to.equal('order-confirmation');
      expect(template.isActive).to.be.true;
    });

    it('should reject duplicate name', () => {
      service.createTemplate({
        name: 'order-confirmation',
        channel: 'email',
        subject: 'Test',
        bodyTemplate: 'Test body',
      });

      expect(() => {
        service.createTemplate({
          name: 'order-confirmation',
          channel: 'sms',
          subject: 'Test',
          bodyTemplate: 'Another body',
        });
      }).to.throw('already exists');
    });

    it('should reject empty name', () => {
      expect(() => {
        service.createTemplate({
          name: '',
          channel: 'email',
          subject: 'Test',
          bodyTemplate: 'Body',
        });
      }).to.throw('name is required');
    });

    it('should reject empty body template', () => {
      expect(() => {
        service.createTemplate({
          name: 'test',
          channel: 'email',
          subject: 'Test',
          bodyTemplate: '',
        });
      }).to.throw('Body template');
    });
  });

  describe('renderTemplate', () => {
    it('should render template with variables', () => {
      const template = service.createTemplate({
        name: 'welcome',
        channel: 'email',
        subject: 'Welcome {{userName}}!',
        bodyTemplate: 'Hello {{userName}}, welcome to our store!',
        variables: ['userName'],
      });

      const rendered = service.renderTemplate(template.id, { userName: 'John' });
      expect(rendered.subject).to.equal('Welcome John!');
      expect(rendered.body).to.equal('Hello John, welcome to our store!');
    });

    it('should throw for unresolved variables', () => {
      const template = service.createTemplate({
        name: 'order-update',
        channel: 'email',
        subject: 'Order {{orderNumber}}',
        bodyTemplate: 'Your order {{orderNumber}} status: {{status}}',
        variables: ['orderNumber', 'status'],
      });

      expect(() => {
        service.renderTemplate(template.id, { orderNumber: '12345' });
      }).to.throw('Unresolved');
    });

    it('should throw for nonexistent template', () => {
      expect(() => {
        service.renderTemplate('nonexistent', {});
      }).to.throw('not found');
    });

    it('should throw for inactive template', () => {
      const template = service.createTemplate({
        name: 'old-template',
        channel: 'email',
        subject: 'Test',
        bodyTemplate: 'Body',
      });
      service.updateTemplate(template.id, { isActive: false });

      expect(() => {
        service.renderTemplate(template.id, {});
      }).to.throw('inactive');
    });
  });

  describe('updateTemplate', () => {
    it('should update template fields', () => {
      const template = service.createTemplate({
        name: 'test',
        channel: 'email',
        subject: 'Old Subject',
        bodyTemplate: 'Old body',
      });

      const updated = service.updateTemplate(template.id, {
        subject: 'New Subject',
        bodyTemplate: 'New body',
      });

      expect(updated.subject).to.equal('New Subject');
      expect(updated.bodyTemplate).to.equal('New body');
    });

    it('should return null for nonexistent template', () => {
      const result = service.updateTemplate('nonexistent', { name: 'Test' });
      expect(result).to.be.null;
    });
  });

  describe('listTemplates', () => {
    it('should list all templates', () => {
      service.createTemplate({ name: 't1', channel: 'email', subject: 'S', bodyTemplate: 'B' });
      service.createTemplate({ name: 't2', channel: 'sms', subject: 'S', bodyTemplate: 'B' });
      expect(service.listTemplates()).to.have.length(2);
    });

    it('should filter by channel', () => {
      service.createTemplate({ name: 't1', channel: 'email', subject: 'S', bodyTemplate: 'B' });
      service.createTemplate({ name: 't2', channel: 'sms', subject: 'S', bodyTemplate: 'B' });
      expect(service.listTemplates('email')).to.have.length(1);
    });
  });

  describe('deleteTemplate', () => {
    it('should delete existing template', () => {
      const template = service.createTemplate({
        name: 'test',
        channel: 'email',
        subject: 'S',
        bodyTemplate: 'B',
      });
      expect(service.deleteTemplate(template.id)).to.be.true;
      expect(service.getTemplate(template.id)).to.be.null;
    });

    it('should return false for nonexistent', () => {
      expect(service.deleteTemplate('nonexistent')).to.be.false;
    });
  });
});

