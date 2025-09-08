import type { ValidationResult } from "$lib/types";

export const validateMessage = (message: string): ValidationResult => {
  const trimmed = message.trim();

  if (!trimmed) {
    return { isValid: false, error: "Please enter a message" };
  }

  if (trimmed.length > 500) {
    return {
      isValid: false,
      error: "Message is too long (max 500 characters)",
    };
  }

  return { isValid: true };
};

export const validateNotEmpty = (value: string): boolean =>
  value.trim().length > 0;

export const validateMaxLength = (value: string, maxLength: number): boolean =>
  value.length <= maxLength;

export const validateMinLength = (value: string, minLength: number): boolean =>
  value.length >= minLength;

export const combineValidations =
  (...validators: Array<(value: string) => ValidationResult>) =>
  (value: string): ValidationResult => {
    for (const validator of validators) {
      const result = validator(value);
      if (!result.isValid) {
        return result;
      }
    }
    return { isValid: true };
  };

export const createLengthValidator =
  (min: number, max: number) =>
  (value: string): ValidationResult => {
    if (value.length < min) {
      return { isValid: false, error: `Minimum ${min} characters required` };
    }
    if (value.length > max) {
      return { isValid: false, error: `Maximum ${max} characters allowed` };
    }
    return { isValid: true };
  };

export const createRequiredValidator =
  (message = "This field is required") =>
  (value: string): ValidationResult =>
    validateNotEmpty(value)
      ? { isValid: true }
      : { isValid: false, error: message };
