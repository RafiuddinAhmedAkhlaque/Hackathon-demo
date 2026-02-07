import { Request, Response, NextFunction } from 'express';

export interface ValidationRule {
  field: string;
  required?: boolean;
  type?: string;
  minLength?: number;
  maxLength?: number;
  min?: number;
  max?: number;
  pattern?: RegExp;
  message?: string;
}

export function validate(rules: ValidationRule[]) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const errors: string[] = [];

    for (const rule of rules) {
      const value = req.body[rule.field];

      // Check required
      if (rule.required && (value === undefined || value === null || value === '')) {
        errors.push(rule.message || `${rule.field} is required`);
        continue;
      }

      if (value === undefined || value === null) continue;

      // Check type
      if (rule.type && typeof value !== rule.type) {
        errors.push(rule.message || `${rule.field} must be of type ${rule.type}`);
        continue;
      }

      // Check string length
      if (typeof value === 'string') {
        if (rule.minLength && value.length < rule.minLength) {
          errors.push(
            rule.message || `${rule.field} must be at least ${rule.minLength} characters`
          );
        }
        if (rule.maxLength && value.length > rule.maxLength) {
          errors.push(
            rule.message || `${rule.field} must be at most ${rule.maxLength} characters`
          );
        }
        if (rule.pattern && !rule.pattern.test(value)) {
          errors.push(rule.message || `${rule.field} has an invalid format`);
        }
      }

      // Check numeric range
      if (typeof value === 'number') {
        if (rule.min !== undefined && value < rule.min) {
          errors.push(rule.message || `${rule.field} must be at least ${rule.min}`);
        }
        if (rule.max !== undefined && value > rule.max) {
          errors.push(rule.message || `${rule.field} must be at most ${rule.max}`);
        }
      }
    }

    if (errors.length > 0) {
      res.status(400).json({ errors });
      return;
    }

    next();
  };
}

