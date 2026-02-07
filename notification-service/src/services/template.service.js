const { NotificationTemplate } = require('../models/template.model');

class TemplateService {
  constructor() {
    this.templates = new Map();
  }

  createTemplate({ name, channel, subject, bodyTemplate, variables }) {
    this.validateTemplate({ name, channel, bodyTemplate });

    // Check for duplicate name
    const existing = Array.from(this.templates.values()).find(t => t.name === name);
    if (existing) {
      throw new Error(`Template with name '${name}' already exists`);
    }

    const template = new NotificationTemplate({ name, channel, subject, bodyTemplate, variables });
    this.templates.set(template.id, template);
    return template;
  }

  getTemplate(id) {
    return this.templates.get(id) || null;
  }

  getTemplateByName(name) {
    return Array.from(this.templates.values()).find(t => t.name === name) || null;
  }

  updateTemplate(id, updates) {
    const template = this.templates.get(id);
    if (!template) return null;

    if (updates.name !== undefined) template.name = updates.name;
    if (updates.subject !== undefined) template.subject = updates.subject;
    if (updates.bodyTemplate !== undefined) template.bodyTemplate = updates.bodyTemplate;
    if (updates.variables !== undefined) template.variables = updates.variables;
    if (updates.isActive !== undefined) template.isActive = updates.isActive;
    template.updatedAt = new Date();

    return template;
  }

  deleteTemplate(id) {
    return this.templates.delete(id);
  }

  renderTemplate(templateId, data) {
    const template = this.templates.get(templateId);
    if (!template) {
      throw new Error(`Template '${templateId}' not found`);
    }
    if (!template.isActive) {
      throw new Error(`Template '${templateId}' is inactive`);
    }
    return template.render(data);
  }

  listTemplates(channel = null) {
    let templates = Array.from(this.templates.values());
    if (channel) {
      templates = templates.filter(t => t.channel === channel);
    }
    return templates;
  }

  validateTemplate({ name, channel, bodyTemplate }) {
    if (!name || !name.trim()) {
      throw new Error('Template name is required');
    }
    if (!channel || !channel.trim()) {
      throw new Error('Channel is required');
    }
    if (!bodyTemplate || !bodyTemplate.trim()) {
      throw new Error('Body template is required');
    }
  }
}

module.exports = { TemplateService };

