/**
 * Delete Confirmation Module - SweetAlert2 Integration
 * Finanpy - Personal Finance Management System
 *
 * This module provides:
 * - Intercepts delete form submissions
 * - Shows SweetAlert2 confirmation modal with dark theme
 * - Uses Finanpy design system colors
 * - Supports different item types (conta, categoria, transação)
 */

(function() {
    'use strict';

    /**
     * DeleteConfirmation class handles delete confirmation modals
     */
    class DeleteConfirmation {
        constructor() {
            this.forms = null;
            this.init();
        }

        /**
         * Initialize delete confirmation handlers
         */
        init() {
            // Wait for DOM to be ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.attachHandlers());
            } else {
                this.attachHandlers();
            }
        }

        /**
         * Attach handlers to all delete confirmation forms
         */
        attachHandlers() {
            // Find all forms with data-delete-confirm attribute
            this.forms = document.querySelectorAll('form[data-delete-confirm]');

            if (!this.forms.length) {
                return;
            }

            // Attach submit handler to each form
            this.forms.forEach(form => {
                form.addEventListener('submit', (e) => this.handleSubmit(e, form));
            });
        }

        /**
         * Handle form submission
         * @param {Event} e - Submit event
         * @param {HTMLFormElement} form - The form element
         */
        handleSubmit(e, form) {
            // Prevent default form submission
            e.preventDefault();

            // Get item details from data attributes
            const itemName = form.dataset.itemName || 'este item';
            const itemType = form.dataset.itemType || 'item';

            // Show confirmation modal
            this.showConfirmation(itemName, itemType, form);
        }

        /**
         * Show SweetAlert2 confirmation modal
         * @param {string} itemName - Name/description of item to delete
         * @param {string} itemType - Type of item (conta, categoria, transação)
         * @param {HTMLFormElement} form - The form to submit if confirmed
         */
        showConfirmation(itemName, itemType, form) {
            Swal.fire({
                title: 'Confirmar Exclusão',
                html: `Tem certeza que deseja excluir <strong>${itemType}</strong>:<br><strong class="text-lg">${itemName}</strong>?<br><br><span class="text-sm text-gray-400">Esta ação não pode ser desfeita.</span>`,
                icon: 'warning',
                iconColor: '#ef4444',
                background: '#1f2937',
                color: '#f3f4f6',
                showCancelButton: true,
                confirmButtonText: 'Sim, excluir',
                cancelButtonText: 'Cancelar',
                confirmButtonColor: '#dc2626',
                cancelButtonColor: '#374151',
                focusCancel: true,
                reverseButtons: true,
                customClass: {
                    popup: 'border border-gray-700 shadow-2xl',
                    title: 'text-gray-100 text-xl font-bold',
                    htmlContainer: 'text-gray-300',
                    confirmButton: 'px-6 py-3 rounded-lg font-semibold hover:shadow-xl transition-all duration-200',
                    cancelButton: 'px-6 py-3 rounded-lg font-semibold hover:bg-gray-600 transition-all duration-200'
                },
                buttonsStyling: true,
                allowOutsideClick: true,
                allowEscapeKey: true
            }).then((result) => {
                if (result.isConfirmed) {
                    // User confirmed - submit the form
                    this.submitForm(form);
                }
                // User cancelled - do nothing, modal will close
            });
        }

        /**
         * Submit the form after confirmation
         * @param {HTMLFormElement} form - The form to submit
         */
        submitForm(form) {
            // Show loading state
            Swal.fire({
                title: 'Excluindo...',
                text: 'Por favor, aguarde.',
                icon: 'info',
                iconColor: '#3b82f6',
                background: '#1f2937',
                color: '#f3f4f6',
                allowOutsideClick: false,
                allowEscapeKey: false,
                showConfirmButton: false,
                customClass: {
                    popup: 'border border-gray-700 shadow-2xl'
                },
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            // Submit the form
            form.submit();
        }
    }

    /**
     * Initialize on DOM ready
     */
    function init() {
        // Create DeleteConfirmation instance
        const deleteConfirmation = new DeleteConfirmation();

        // Export for external use if needed
        window.FinanpyDeleteConfirmation = deleteConfirmation;
    }

    // Run initialization
    init();

})();
