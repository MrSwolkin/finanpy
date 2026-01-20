/**
 * Transactions Module - JavaScript for Transaction Forms
 * Finanpy - Personal Finance Management System
 *
 * This module provides:
 * - Dynamic category filtering based on transaction type
 * - Date picker enhancements
 * - Numeric value validation and formatting
 */

(function() {
    'use strict';

    /**
     * TransactionForm class handles form interactions
     */
    class TransactionForm {
        constructor() {
            // Form elements - using standard Django form IDs
            this.form = document.querySelector('form');
            this.transactionTypeSelect = document.getElementById('id_transaction_type');
            this.categorySelect = document.getElementById('id_category');
            this.amountInput = document.getElementById('id_amount');
            this.dateInput = document.getElementById('id_transaction_date');

            // Store original category options for filtering
            this.allCategoryOptions = [];
            this.emptyOption = null;

            // Initialize if elements exist
            if (this.form) {
                this.init();
            }
        }

        /**
         * Initialize all form handlers
         */
        init() {
            this.initCategoryFilter();
            this.initAmountValidation();
            this.initDatePicker();
        }

        /**
         * Initialize category filtering based on transaction type
         * Task 32.2
         */
        initCategoryFilter() {
            if (!this.transactionTypeSelect || !this.categorySelect) {
                return;
            }

            // Store all category options (skip the empty one)
            const options = Array.from(this.categorySelect.options);
            this.emptyOption = options[0];
            this.allCategoryOptions = options.slice(1);

            // Add change listener
            this.transactionTypeSelect.addEventListener('change', () => this.filterCategories());

            // Initial filter on page load
            this.filterCategories();
        }

        /**
         * Filter category options based on selected transaction type
         */
        filterCategories() {
            const selectedType = this.transactionTypeSelect.value;

            // Clear current options
            this.categorySelect.innerHTML = '';

            // Add empty option back
            if (this.emptyOption) {
                this.categorySelect.appendChild(this.emptyOption.cloneNode(true));
            }

            // If no type selected, show all categories
            if (!selectedType) {
                this.allCategoryOptions.forEach(option => {
                    this.categorySelect.appendChild(option.cloneNode(true));
                });
                return;
            }

            // Filter and add matching categories
            let hasOptions = false;
            this.allCategoryOptions.forEach(option => {
                const categoryType = option.getAttribute('data-type');
                if (categoryType === selectedType) {
                    this.categorySelect.appendChild(option.cloneNode(true));
                    hasOptions = true;
                }
            });

            // Show warning if no categories available for selected type
            if (!hasOptions) {
                const warningOption = document.createElement('option');
                warningOption.value = '';
                warningOption.textContent = 'Nenhuma categoria disponivel para este tipo';
                warningOption.disabled = true;
                this.categorySelect.appendChild(warningOption);
            }

            // Reset category selection if current value doesn't match the type
            const currentSelectedOption = this.categorySelect.querySelector(`option[value="${this.categorySelect.value}"]`);
            if (currentSelectedOption) {
                const currentType = currentSelectedOption.getAttribute('data-type');
                if (currentType && currentType !== selectedType) {
                    this.categorySelect.value = '';
                }
            }
        }

        /**
         * Initialize amount field validation
         * Task 32.4
         */
        initAmountValidation() {
            if (!this.amountInput) {
                return;
            }

            // Prevent negative values on input
            this.amountInput.addEventListener('input', (e) => this.handleAmountInput(e));

            // Format on blur
            this.amountInput.addEventListener('blur', (e) => this.handleAmountBlur(e));

            // Handle keyboard input - allow only valid characters
            this.amountInput.addEventListener('keydown', (e) => this.handleAmountKeydown(e));
        }

        /**
         * Handle amount input - prevent negative values and invalid characters
         */
        handleAmountInput(e) {
            let value = e.target.value;

            // Remove any non-numeric characters except decimal point
            value = value.replace(/[^0-9.]/g, '');

            // Ensure only one decimal point
            const parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }

            // Limit decimal places to 2
            if (parts.length === 2 && parts[1].length > 2) {
                value = parts[0] + '.' + parts[1].substring(0, 2);
            }

            // Prevent negative values
            const numValue = parseFloat(value);
            if (!isNaN(numValue) && numValue < 0) {
                value = '';
            }

            // Update input value
            if (e.target.value !== value) {
                e.target.value = value;
            }
        }

        /**
         * Handle amount blur - format to 2 decimal places
         */
        handleAmountBlur(e) {
            const value = e.target.value;

            if (value && !isNaN(parseFloat(value))) {
                const numValue = parseFloat(value);
                if (numValue > 0) {
                    e.target.value = numValue.toFixed(2);
                } else if (numValue === 0) {
                    e.target.value = '';
                }
            }
        }

        /**
         * Handle amount keydown - block invalid keys
         */
        handleAmountKeydown(e) {
            // Allow: backspace, delete, tab, escape, enter, decimal point
            const allowedKeys = [
                'Backspace', 'Delete', 'Tab', 'Escape', 'Enter',
                'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown',
                'Home', 'End'
            ];

            if (allowedKeys.includes(e.key)) {
                return;
            }

            // Allow decimal point (only one)
            if (e.key === '.' || e.key === ',') {
                if (e.target.value.includes('.')) {
                    e.preventDefault();
                } else {
                    // Convert comma to period
                    if (e.key === ',') {
                        e.preventDefault();
                        const start = e.target.selectionStart;
                        const end = e.target.selectionEnd;
                        const value = e.target.value;
                        e.target.value = value.substring(0, start) + '.' + value.substring(end);
                        e.target.setSelectionRange(start + 1, start + 1);
                    }
                }
                return;
            }

            // Allow: Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
            if (e.ctrlKey || e.metaKey) {
                return;
            }

            // Block non-numeric keys
            if (!/^[0-9]$/.test(e.key)) {
                e.preventDefault();
            }
        }

        /**
         * Initialize date picker enhancements
         * Task 32.3
         */
        initDatePicker() {
            if (!this.dateInput) {
                return;
            }

            // Set max date to today (prevent future dates if needed)
            // Commented out as per business rule - future dates may be allowed
            // const today = new Date().toISOString().split('T')[0];
            // this.dateInput.setAttribute('max', today);

            // Set default value to today if empty and creating new transaction
            const isEditMode = this.form.querySelector('input[name="pk"]') ||
                              window.location.pathname.includes('/edit/');

            if (!isEditMode && !this.dateInput.value) {
                const today = new Date().toISOString().split('T')[0];
                this.dateInput.value = today;
            }

            // Add visual feedback for date selection
            this.dateInput.addEventListener('change', () => {
                this.dateInput.classList.add('date-selected');
            });
        }
    }

    /**
     * TransactionFilter class handles filter form interactions
     * Used on transaction list page
     */
    class TransactionFilter {
        constructor() {
            this.filterForm = document.querySelector('form[method="get"]');
            this.dateFromInput = document.getElementById('id_date_from');
            this.dateToInput = document.getElementById('id_date_to');
            this.transactionTypeSelect = document.getElementById('id_transaction_type');
            this.categorySelect = document.getElementById('id_category');

            // Store category options for filtering
            this.allCategoryOptions = [];
            this.emptyOption = null;

            if (this.filterForm && this.dateFromInput) {
                this.init();
            }
        }

        /**
         * Initialize filter form handlers
         */
        init() {
            this.initDateValidation();
            this.initCategoryFilterByType();
        }

        /**
         * Initialize date validation for filters
         */
        initDateValidation() {
            if (!this.dateFromInput || !this.dateToInput) {
                return;
            }

            // Validate that date_from is not after date_to
            const validateDates = () => {
                if (this.dateFromInput.value && this.dateToInput.value) {
                    if (this.dateFromInput.value > this.dateToInput.value) {
                        this.dateToInput.setCustomValidity('A data final deve ser maior ou igual a data inicial');
                    } else {
                        this.dateToInput.setCustomValidity('');
                    }
                } else {
                    this.dateToInput.setCustomValidity('');
                }
            };

            this.dateFromInput.addEventListener('change', validateDates);
            this.dateToInput.addEventListener('change', validateDates);
        }

        /**
         * Initialize category filtering by transaction type in filter form
         */
        initCategoryFilterByType() {
            if (!this.transactionTypeSelect || !this.categorySelect) {
                return;
            }

            // Check if categories have data-type attribute
            const hasDataType = Array.from(this.categorySelect.options)
                .some(opt => opt.getAttribute('data-type'));

            if (!hasDataType) {
                return;
            }

            // Store options
            const options = Array.from(this.categorySelect.options);
            this.emptyOption = options[0];
            this.allCategoryOptions = options.slice(1);

            // Add listener
            this.transactionTypeSelect.addEventListener('change', () => this.filterCategories());
        }

        /**
         * Filter categories in filter form based on transaction type
         */
        filterCategories() {
            const selectedType = this.transactionTypeSelect.value;

            this.categorySelect.innerHTML = '';

            if (this.emptyOption) {
                this.categorySelect.appendChild(this.emptyOption.cloneNode(true));
            }

            if (!selectedType) {
                this.allCategoryOptions.forEach(option => {
                    this.categorySelect.appendChild(option.cloneNode(true));
                });
                return;
            }

            this.allCategoryOptions.forEach(option => {
                const categoryType = option.getAttribute('data-type');
                if (categoryType === selectedType) {
                    this.categorySelect.appendChild(option.cloneNode(true));
                }
            });
        }
    }

    /**
     * Utility functions
     */
    const Utils = {
        /**
         * Format number as Brazilian currency
         */
        formatCurrency(value) {
            return new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            }).format(value);
        },

        /**
         * Parse Brazilian currency string to number
         */
        parseCurrency(str) {
            if (!str) return 0;
            // Remove R$, spaces, and convert comma to period
            const cleaned = str
                .replace(/R\$\s?/g, '')
                .replace(/\./g, '')
                .replace(',', '.')
                .trim();
            return parseFloat(cleaned) || 0;
        },

        /**
         * Format date as Brazilian format (dd/mm/yyyy)
         */
        formatDate(dateStr) {
            if (!dateStr) return '';
            const date = new Date(dateStr + 'T00:00:00');
            return date.toLocaleDateString('pt-BR');
        }
    };

    /**
     * Initialize on DOM ready
     */
    function init() {
        // Initialize transaction form handlers
        new TransactionForm();

        // Initialize filter form handlers
        new TransactionFilter();
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Export for external use if needed
    window.FinanpyTransactions = {
        TransactionForm,
        TransactionFilter,
        Utils
    };

})();
