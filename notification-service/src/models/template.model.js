const { v4: uuidv4 } = require('uuid');

class NotificationTemplate {
  constructor({ name, channel, subject, bodyTemplate, variables = [], isActive = true }) {
    this.id = uuidv4();
    this.name = name;
    this.channel = channel;
    this.subject = subject;
    this.bodyTemplate = bodyTemplate;
    this.variables = variables; // Expected variable names like ['userName', 'orderNumber']
    this.isActive = isActive;
    this.createdAt = new Date();
    this.updatedAt = new Date();
  }

  render(data) {
    let rendered = this.bodyTemplate;
    let renderedSubject = this.subject;

    for (const [key, value] of Object.entries(data)) {
      const placeholder = `{{${key}}}`;
      rendered = rendered.split(placeholder).join(value);
      renderedSubject = renderedSubject.split(placeholder).join(value);
    }

    // Check for unresolved placeholders
    const unresolvedBody = rendered.match(/\{\{(\w+)\}\}/g);
    const unresolvedSubject = renderedSubject.match(/\{\{(\w+)\}\}/g);
    const unresolved = [...(unresolvedBody || []), ...(unresolvedSubject || [])];

    if (unresolved.length > 0) {
      throw new Error(`Unresolved template variables: ${unresolved.join(', ')}`);
    }

    return { subject: renderedSubject, body: rendered };
  }

  toJSON() {
    return {
      id: this.id,
      name: this.name,
      channel: this.channel,
      subject: this.subject,
      bodyTemplate: this.bodyTemplate,
      variables: this.variables,
      isActive: this.isActive,
      createdAt: this.createdAt.toISOString(),
      updatedAt: this.updatedAt.toISOString(),
    };
  }
}

module.exports = { NotificationTemplate };

