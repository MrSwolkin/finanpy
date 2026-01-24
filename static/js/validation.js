/**
 * Form Validation Module - Real-time form field validation
 * Finanpy - Personal Finance Management System
 *
 * This module provides:
 * - Real-time validation on blur and input events
 * - Visual feedback for valid/invalid states
 * - Portuguese error messages
 * - Support for common validation rules
 * - Accessibility features (aria-invalid)
 */

(function() {
    'use strict';

    /**
     * Validation error messages in Portuguese
     */
    const ERROR_MESSAGES = {
        required: 'Este campo é obrigatório',
        email: 'Digite um email válido',
        minLength: 'Mínimo de {n} caracteres',
        maxLength: 'Máximo de {n} caracteres',
        positive: 'Digite um valor positivo',
        match: 'Os campos não coincidem',
        date: 'Digite uma data válida'
    };

    /**
     * FormValidator class handles all form validation
     */
    class FormValidator {
        constructor() {
            this.validatedFields = new Map();
            this.init();
        }

        /**
         * Initialize validation on all forms
         */
        init() {
            // Find all fields with data-validate attribute
            const fields = document.querySelectorAll('[data-validate]');

            fields.forEach(field => {
                this.setupFieldValidation(field);
            });
        }

        /**
         * Setup validation for a single field
         * @param {HTMLElement} field - The input field to validate
         */
        setupFieldValidation(field) {
            // Store validation state
            this.validatedFields.set(field, {
                touched: false,
                valid: true
            });

            // Validate on blur (when leaving field)
            field.addEventListener('blur', () => {
                const state = this.validatedFields.get(field);
                state.touched = true;
                this.validateField(field);
            });

            // Validate on input (after first blur)
            field.addEventListener('input', () => {
                const state = this.validatedFields.get(field);
                if (state.touched) {
                    this.validateField(field);
                }
            });

            // Also validate on change for select fields
            if (field.tagName === 'SELECT') {
                field.addEventListener('change', () => {
                    const state = this.validatedFields.get(field);
                    state.touched = true;
                    this.validateField(field);
                });
            }
        }

        /**
         * Validate a field and show/hide error messages
         * @param {HTMLElement} field - The field to validate
         * @returns {boolean} - Whether the field is valid
         */
        validateField(field) {
            const state = this.validatedFields.get(field);

            // Get all validation rules for this field
            const errors = [];

            // Required validation
            if (field.hasAttribute('data-required')) {
                const value = field.value.trim();
                if (!value) {
                    errors.push(ERROR_MESSAGES.required);
                }
            }

            // Only continue with other validations if field is not empty
            const value = field.value.trim();
            if (value) {
                // Email validation
                if (field.hasAttribute('data-email')) {
                    if (!this.isValidEmail(value)) {
                        errors.push(ERROR_MESSAGES.email);
                    }
                }

                // Min length validation
                if (field.hasAttribute('data-min-length')) {
                    const minLength = parseInt(field.getAttribute('data-min-length'));
                    if (value.length < minLength) {
                        errors.push(ERROR_MESSAGES.minLength.replace('{n}', minLength));
                    }
                }

                // Max length validation
                if (field.hasAttribute('data-max-length')) {
                    const maxLength = parseInt(field.getAttribute('data-max-length'));
                    if (value.length > maxLength) {
                        errors.push(ERROR_MESSAGES.maxLength.replace('{n}', maxLength));
                    }
                }

                // Positive number validation
                if (field.hasAttribute('data-positive')) {
                    const num = parseFloat(value);
                    if (isNaN(num) || num <= 0) {
                        errors.push(ERROR_MESSAGES.positive);
                    }
                }

                // Match validation (for password confirmation)
                if (field.hasAttribute('data-match')) {
                    const matchFieldId = field.getAttribute('data-match');
                    const matchField = document.getElementById(matchFieldId);
                    if (matchField && value !== matchField.value) {
                        errors.push(ERROR_MESSAGES.match);
                    }
                }
            }

            // Update validation state
            state.valid = errors.length === 0;

            // Update UI
            this.updateFieldUI(field, errors);

            return state.valid;
        }

        /**
         * Update field UI based on validation state
         * @param {HTMLElement} field - The field to update
         * @param {Array} errors - Array of error messages
         */
        updateFieldUI(field, errors) {
            const isValid = errors.length === 0;
            const state = this.validatedFields.get(field);

            // Only show validation UI if field has been touched
            if (!state.touched) {
                return;
            }

            // Remove existing error message
            this.removeErrorMessage(field);

            if (isValid) {
                // Valid state - green border
                field.classList.remove('border-red-500', 'border-gray-600');
                field.classList.add('border-green-500');
                field.setAttribute('aria-invalid', 'false');
            } else {
                // Invalid state - red border and error message
                field.classList.remove('border-green-500', 'border-gray-600');
                field.classList.add('border-red-500');
                field.setAttribute('aria-invalid', 'true');

                // Show first error message only
                this.showErrorMessage(field, errors[0]);
            }
        }

        /**
         * Show error message below field
         * @param {HTMLElement} field - The field
         * @param {string} message - The error message
         */
        showErrorMessage(field, message) {
            // Create error message element
            const errorDiv = document.createElement('div');
            errorDiv.className = 'validation-error mt-2 text-sm text-red-400';
            errorDiv.textContent = message;
            errorDiv.setAttribute('role', 'alert');

            // Insert after field
            const parent = field.parentElement;

            // Find where to insert (after help text if exists)
            let insertAfter = field;
            const nextElement = field.nextElementSibling;

            // If next element is help text (text-gray-400), insert after it
            if (nextElement && nextElement.classList.contains('text-gray-400')) {
                insertAfter = nextElement;
            }

            // Insert error message
            insertAfter.insertAdjacentElement('afterend', errorDiv);
        }

        /**
         * Remove error message from field
         * @param {HTMLElement} field - The field
         */
        removeErrorMessage(field) {
            const parent = field.parentElement;
            const existingError = parent.querySelector('.validation-error');
            if (existingError) {
                existingError.remove();
            }
        }

        /**
         * Validate email format
         * @param {string} email - Email to validate
         * @returns {boolean} - Whether email is valid
         */
        isValidEmail(email) {
            // Simple but effective email regex
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        }

        /**
         * Validate all fields in a form
         * @param {HTMLFormElement} form - The form to validate
         * @returns {boolean} - Whether all fields are valid
         */
        validateForm(form) {
            const fields = form.querySelectorAll('[data-validate]');
            let allValid = true;

            fields.forEach(field => {
                const state = this.validatedFields.get(field);
                if (state) {
                    state.touched = true;
                    const isValid = this.validateField(field);
                    if (!isValid) {
                        allValid = false;
                    }
                }
            });

            return allValid;
        }

        /**
         * Reset validation for a field
         * @param {HTMLElement} field - The field to reset
         */
        resetField(field) {
            const state = this.validatedFields.get(field);
            if (state) {
                state.touched = false;
                state.valid = true;
            }

            // Remove validation UI
            field.classList.remove('border-red-500', 'border-green-500');
            field.classList.add('border-gray-600');
            field.removeAttribute('aria-invalid');
            this.removeErrorMessage(field);
        }

        /**
         * Reset all fields in a form
         * @param {HTMLFormElement} form - The form to reset
         */
        resetForm(form) {
            const fields = form.querySelectorAll('[data-validate]');
            fields.forEach(field => {
                this.resetField(field);
            });
        }
    }

    /**
     * Initialize on DOM ready
     */
    function init() {
        // Create validator instance
        const validator = new FormValidator();

        // Export for external use
        window.FinanpyValidation = validator;
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
