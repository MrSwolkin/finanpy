/**
 * Form Loading Module - Loading States for Forms
 * Finanpy - Personal Finance Management System
 *
 * This module provides:
 * - Automatic form submission interception
 * - Loading spinner on submit buttons
 * - Disable all form inputs during submission
 * - Prevent double-submit
 * - Support for forms with data-loading attribute
 */

(function() {
    'use strict';

    /**
     * FormLoading class handles form loading states
     */
    class FormLoading {
        constructor(form) {
            this.form = form;
            this.submitButton = null;
            this.originalButtonHTML = '';
            this.loadingText = '';
            this.isSubmitting = false;

            // Find submit button
            this.findSubmitButton();

            // Initialize if submit button exists
            if (this.submitButton) {
                this.init();
            }
        }

        /**
         * Find the submit button in the form
         */
        findSubmitButton() {
            // Look for button[type="submit"] or input[type="submit"]
            this.submitButton = this.form.querySelector('button[type="submit"]') ||
                                this.form.querySelector('input[type="submit"]');
        }

        /**
         * Initialize form loading handlers
         */
        init() {
            // Get loading text from button's data attribute or use default
            this.loadingText = this.submitButton.getAttribute('data-loading-text') || 'Processando...';

            // Store original button HTML
            this.originalButtonHTML = this.submitButton.innerHTML;

            // Add submit handler
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        }

        /**
         * Handle form submission
         * @param {Event} e - Submit event
         */
        handleSubmit(e) {
            // Prevent double-submit
            if (this.isSubmitting) {
                e.preventDefault();
                return;
            }

            // Set submitting state
            this.isSubmitting = true;

            // Show loading state
            this.showLoading();

            // Note: We don't prevent default here, so the form submits normally
            // The page will reload after submission, resetting the state
        }

        /**
         * Show loading state
         */
        showLoading() {
            // Disable the submit button
            this.submitButton.disabled = true;

            // Add disabled styles
            this.submitButton.classList.add('opacity-50', 'cursor-not-allowed');

            // Replace button content with spinner + loading text
            this.submitButton.innerHTML = this.getLoadingHTML();

            // Disable all form inputs
            this.disableFormInputs();
        }

        /**
         * Get loading HTML (spinner + text)
         * @returns {string} HTML string
         */
        getLoadingHTML() {
            return `
                <svg class="w-5 h-5 animate-spin -ml-1 mr-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                ${this.loadingText}
            `;
        }

        /**
         * Disable all form inputs
         */
        disableFormInputs() {
            // Get all input elements
            const inputs = this.form.querySelectorAll('input, select, textarea, button');

            inputs.forEach(input => {
                // Skip if already disabled
                if (!input.disabled) {
                    input.disabled = true;
                    // Mark as disabled by us for potential restoration
                    input.setAttribute('data-disabled-by-loading', 'true');
                }
            });
        }

        /**
         * Restore original state (for client-side validation failures, etc.)
         * Note: In most cases, the page will reload after submission
         */
        restore() {
            // Re-enable the submit button
            this.submitButton.disabled = false;

            // Remove disabled styles
            this.submitButton.classList.remove('opacity-50', 'cursor-not-allowed');

            // Restore original button HTML
            this.submitButton.innerHTML = this.originalButtonHTML;

            // Re-enable form inputs
            this.enableFormInputs();

            // Reset submitting state
            this.isSubmitting = false;
        }

        /**
         * Re-enable form inputs
         */
        enableFormInputs() {
            // Get all inputs that were disabled by us
            const inputs = this.form.querySelectorAll('[data-disabled-by-loading="true"]');

            inputs.forEach(input => {
                input.disabled = false;
                input.removeAttribute('data-disabled-by-loading');
            });
        }
    }

    /**
     * FormLoadingManager class manages all forms with loading states
     */
    class FormLoadingManager {
        constructor() {
            this.forms = [];
            this.init();
        }

        /**
         * Initialize the manager
         */
        init() {
            // Find all forms with data-loading attribute
            this.initializeForms();

            // Watch for dynamically added forms
            this.observeNewForms();
        }

        /**
         * Initialize existing forms on page load
         */
        initializeForms() {
            const formElements = document.querySelectorAll('form[data-loading]');

            formElements.forEach(formElement => {
                const formLoading = new FormLoading(formElement);
                this.forms.push(formLoading);
            });
        }

        /**
         * Watch for dynamically added forms
         */
        observeNewForms() {
            // Use MutationObserver to detect new forms
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1) {
                            // Check if the node itself is a form
                            if (node.matches && node.matches('form[data-loading]')) {
                                const formLoading = new FormLoading(node);
                                this.forms.push(formLoading);
                            }

                            // Check for forms within the added node
                            if (node.querySelectorAll) {
                                const forms = node.querySelectorAll('form[data-loading]');
                                forms.forEach(formElement => {
                                    const formLoading = new FormLoading(formElement);
                                    this.forms.push(formLoading);
                                });
                            }
                        }
                    });
                });
            });

            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }

        /**
         * Get all managed forms
         * @returns {Array} Array of FormLoading instances
         */
        getForms() {
            return this.forms;
        }
    }

    /**
     * Initialize on DOM ready
     */
    function init() {
        // Create FormLoadingManager instance
        const manager = new FormLoadingManager();

        // Export for external use
        window.FinanpyFormLoading = {
            manager: manager,
            getForms: () => manager.getForms()
        };
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
