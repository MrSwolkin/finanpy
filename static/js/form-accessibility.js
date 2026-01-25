/**
 * Form Accessibility Enhancement Script
 *
 * This script enhances form accessibility by:
 * - Adding aria-describedby to fields with help text and errors
 * - Adding aria-invalid to fields with errors
 * - Ensuring aria-required is set on required fields
 * - Dynamically updating aria attributes when errors occur
 */

(function() {
    'use strict';

    /**
     * Enhance a single form field with accessibility attributes
     */
    function enhanceFormField(field) {
        if (!field || !field.id) return;

        const fieldId = field.id;
        const describedByIds = [];

        // Check for help text
        const helpTextEl = document.getElementById(fieldId + '_help');
        if (helpTextEl) {
            describedByIds.push(fieldId + '_help');
        }

        // Check for error messages
        const errorEl = document.getElementById(fieldId + '_error');
        if (errorEl) {
            describedByIds.push(fieldId + '_error');
            field.setAttribute('aria-invalid', 'true');

            // Add error styling if not already present
            if (!field.classList.contains('border-red-500')) {
                field.classList.remove('border-gray-600');
                field.classList.add('border-red-500');
                field.classList.remove('focus:ring-purple-500');
                field.classList.add('focus:ring-red-500');
            }
        } else {
            field.setAttribute('aria-invalid', 'false');
        }

        // Set aria-describedby if we have any IDs
        if (describedByIds.length > 0) {
            const existingDescribedBy = field.getAttribute('aria-describedby');
            // Merge with existing aria-describedby if present
            if (existingDescribedBy) {
                const existingIds = existingDescribedBy.split(' ');
                describedByIds.forEach(id => {
                    if (!existingIds.includes(id)) {
                        existingIds.push(id);
                    }
                });
                field.setAttribute('aria-describedby', existingIds.join(' '));
            } else {
                field.setAttribute('aria-describedby', describedByIds.join(' '));
            }
        }

        // Check if field is required
        if (field.hasAttribute('required') || field.hasAttribute('data-required')) {
            field.setAttribute('aria-required', 'true');
        }
    }

    /**
     * Enhance all form fields on the page
     */
    function enhanceAllFormFields() {
        // Get all input, select, and textarea elements
        const fields = document.querySelectorAll('input, select, textarea');

        fields.forEach(field => {
            // Skip submit buttons, reset buttons, and hidden fields
            if (
                field.type === 'submit' ||
                field.type === 'reset' ||
                field.type === 'button' ||
                field.type === 'hidden'
            ) {
                return;
            }

            enhanceFormField(field);
        });
    }

    /**
     * Add live validation feedback
     */
    function setupLiveValidation() {
        const forms = document.querySelectorAll('form[data-validate]');

        forms.forEach(form => {
            const fields = form.querySelectorAll('input[data-validate], select[data-validate], textarea[data-validate]');

            fields.forEach(field => {
                // Validate on blur
                field.addEventListener('blur', function() {
                    validateField(this);
                });

                // Clear validation on input
                field.addEventListener('input', function() {
                    if (this.getAttribute('aria-invalid') === 'true') {
                        clearFieldError(this);
                    }
                });
            });
        });
    }

    /**
     * Validate a single field
     */
    function validateField(field) {
        // Skip if no validation rules
        if (!field.hasAttribute('data-validate')) return;

        let isValid = true;
        let errorMessage = '';

        // Check required
        if (field.hasAttribute('data-required') || field.hasAttribute('required')) {
            if (!field.value.trim()) {
                isValid = false;
                errorMessage = 'Este campo é obrigatório';
            }
        }

        // Check email
        if (isValid && field.hasAttribute('data-email') && field.value) {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(field.value)) {
                isValid = false;
                errorMessage = 'Digite um e-mail válido';
            }
        }

        // Check min length
        if (isValid && field.hasAttribute('data-min-length') && field.value) {
            const minLength = parseInt(field.getAttribute('data-min-length'));
            if (field.value.length < minLength) {
                isValid = false;
                errorMessage = `Mínimo de ${minLength} caracteres`;
            }
        }

        // Check positive number
        if (isValid && field.hasAttribute('data-positive') && field.value) {
            const value = parseFloat(field.value);
            if (isNaN(value) || value <= 0) {
                isValid = false;
                errorMessage = 'Digite um valor maior que zero';
            }
        }

        // Update aria-invalid
        field.setAttribute('aria-invalid', isValid ? 'false' : 'true');

        // Update visual feedback
        if (!isValid) {
            field.classList.remove('border-gray-600');
            field.classList.add('border-red-500');
            field.classList.remove('focus:ring-purple-500');
            field.classList.add('focus:ring-red-500');

            // Show inline error if it doesn't exist
            const errorId = field.id + '_error';
            let errorEl = document.getElementById(errorId);
            if (!errorEl) {
                errorEl = document.createElement('div');
                errorEl.id = errorId;
                errorEl.className = 'mt-2';
                errorEl.setAttribute('role', 'alert');
                errorEl.innerHTML = `<p class="text-sm text-red-400">${errorMessage}</p>`;
                field.parentElement.appendChild(errorEl);

                // Update aria-describedby
                const helpId = field.id + '_help';
                const hasHelp = document.getElementById(helpId) !== null;
                field.setAttribute('aria-describedby', hasHelp ? `${helpId} ${errorId}` : errorId);
            }
        }
    }

    /**
     * Clear field error
     */
    function clearFieldError(field) {
        field.setAttribute('aria-invalid', 'false');
        field.classList.remove('border-red-500');
        field.classList.add('border-gray-600');
        field.classList.remove('focus:ring-red-500');
        field.classList.add('focus:ring-purple-500');

        // Remove inline error if it exists and was added by JS
        const errorId = field.id + '_error';
        const errorEl = document.getElementById(errorId);
        if (errorEl && !errorEl.hasAttribute('data-server-error')) {
            errorEl.remove();

            // Update aria-describedby
            const helpId = field.id + '_help';
            const hasHelp = document.getElementById(helpId) !== null;
            if (hasHelp) {
                field.setAttribute('aria-describedby', helpId);
            } else {
                field.removeAttribute('aria-describedby');
            }
        }
    }

    /**
     * Initialize accessibility enhancements
     */
    function init() {
        // Enhance all existing fields on page load
        enhanceAllFormFields();

        // Setup live validation
        setupLiveValidation();

        // Re-enhance fields when new content is loaded (for dynamic forms)
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length) {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1) { // Element node
                            if (node.matches('input, select, textarea')) {
                                enhanceFormField(node);
                            } else {
                                const fields = node.querySelectorAll('input, select, textarea');
                                fields.forEach(enhanceFormField);
                            }
                        }
                    });
                }
            });
        });

        // Observe the document body for changes
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
