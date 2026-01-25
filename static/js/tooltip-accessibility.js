/**
 * Tooltip Accessibility Enhancement Module
 * Finanpy - Personal Finance Management System
 *
 * This module provides enhanced keyboard support for tooltips:
 * - Enter/Space to toggle tooltip visibility
 * - Escape to close tooltips
 * - Ensures all tooltip triggers are focusable
 * - Works in conjunction with tooltips.js
 */

(function() {
    'use strict';

    /**
     * Tooltip Accessibility Enhancement Class
     */
    class TooltipAccessibility {
        constructor() {
            this.activeTooltip = null;
            this.init();
        }

        /**
         * Initialize keyboard accessibility enhancements
         */
        init() {
            this.enhanceExistingTooltips();
            this.observeNewTooltips();
        }

        /**
         * Enhance all existing tooltip triggers
         */
        enhanceExistingTooltips() {
            const tooltipTriggers = document.querySelectorAll(
                '[data-tooltip], .tooltip-help-icon, [role="tooltip-trigger"]'
            );

            tooltipTriggers.forEach(trigger => {
                this.enhanceTooltipTrigger(trigger);
            });
        }

        /**
         * Enhance a single tooltip trigger with keyboard support
         * @param {HTMLElement} trigger - The tooltip trigger element
         */
        enhanceTooltipTrigger(trigger) {
            // Make focusable if not already
            if (!trigger.hasAttribute('tabindex')) {
                trigger.setAttribute('tabindex', '0');
            }

            // Ensure proper role
            if (!trigger.hasAttribute('role')) {
                trigger.setAttribute('role', 'button');
            }

            // Add keyboard event listener (only once)
            if (!trigger.hasAttribute('data-tooltip-keyboard-enhanced')) {
                trigger.addEventListener('keydown', (e) => this.handleKeyDown(e, trigger));
                trigger.setAttribute('data-tooltip-keyboard-enhanced', 'true');
            }
        }

        /**
         * Handle keyboard events on tooltip triggers
         * @param {KeyboardEvent} e - The keyboard event
         * @param {HTMLElement} trigger - The tooltip trigger element
         */
        handleKeyDown(e, trigger) {
            // Toggle tooltip on Enter or Space
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.toggleTooltip(trigger);
            }

            // Close tooltip on Escape
            if (e.key === 'Escape') {
                this.closeTooltip(trigger);
            }

            // Arrow keys for navigation (close tooltip and move focus)
            if (e.key === 'ArrowDown' || e.key === 'ArrowUp' ||
                e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                // Close current tooltip when navigating away
                this.closeTooltip(trigger);
            }
        }

        /**
         * Toggle tooltip visibility
         * @param {HTMLElement} trigger - The tooltip trigger element
         */
        toggleTooltip(trigger) {
            const tooltipId = trigger.getAttribute('aria-describedby') ||
                             this.getTooltipId(trigger);
            const tooltip = document.getElementById(tooltipId);

            if (tooltip) {
                const isVisible = tooltip.classList.contains('tooltip-visible');

                if (isVisible) {
                    this.closeTooltip(trigger);
                } else {
                    this.openTooltip(trigger, tooltip);
                }
            } else {
                // Tooltip doesn't exist yet, trigger show via mouseenter event
                this.triggerTooltipShow(trigger);
            }
        }

        /**
         * Open tooltip
         * @param {HTMLElement} trigger - The tooltip trigger element
         * @param {HTMLElement} tooltip - The tooltip element
         */
        openTooltip(trigger, tooltip) {
            // Close any other active tooltip
            if (this.activeTooltip && this.activeTooltip !== tooltip) {
                this.activeTooltip.classList.remove('tooltip-visible');
                this.activeTooltip.classList.add('hidden');
            }

            // Show tooltip
            tooltip.classList.remove('hidden');
            tooltip.classList.add('tooltip-visible');
            tooltip.setAttribute('aria-hidden', 'false');

            // Track active tooltip
            this.activeTooltip = tooltip;
        }

        /**
         * Close tooltip
         * @param {HTMLElement} trigger - The tooltip trigger element
         */
        closeTooltip(trigger) {
            const tooltipId = trigger.getAttribute('aria-describedby') ||
                             this.getTooltipId(trigger);
            const tooltip = document.getElementById(tooltipId);

            if (tooltip && tooltip.classList.contains('tooltip-visible')) {
                tooltip.classList.remove('tooltip-visible');
                tooltip.classList.add('hidden');
                tooltip.setAttribute('aria-hidden', 'true');

                if (this.activeTooltip === tooltip) {
                    this.activeTooltip = null;
                }
            }
        }

        /**
         * Trigger tooltip show via existing tooltip.js functionality
         * @param {HTMLElement} trigger - The tooltip trigger element
         */
        triggerTooltipShow(trigger) {
            // Dispatch mouseenter to trigger the existing tooltip.js logic
            const mouseEnterEvent = new MouseEvent('mouseenter', {
                view: window,
                bubbles: true,
                cancelable: true
            });
            trigger.dispatchEvent(mouseEnterEvent);

            // Wait a bit for tooltip to be created, then make it stay visible
            setTimeout(() => {
                const tooltipId = trigger.getAttribute('aria-describedby') ||
                                 this.getTooltipId(trigger);
                const tooltip = document.getElementById(tooltipId);

                if (tooltip) {
                    this.activeTooltip = tooltip;
                }
            }, 300);
        }

        /**
         * Get tooltip ID from trigger
         * @param {HTMLElement} trigger - The tooltip trigger element
         * @returns {string} The tooltip ID
         */
        getTooltipId(trigger) {
            if (!trigger.id) {
                return null;
            }
            return `${trigger.id}-tooltip`;
        }

        /**
         * Observe DOM for new tooltip triggers
         */
        observeNewTooltips() {
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1) {
                            // Check if node itself is a tooltip trigger
                            if (this.isTooltipTrigger(node)) {
                                this.enhanceTooltipTrigger(node);
                            }

                            // Check for tooltip triggers in children
                            const children = node.querySelectorAll(
                                '[data-tooltip], .tooltip-help-icon, [role="tooltip-trigger"]'
                            );
                            children.forEach(child => {
                                this.enhanceTooltipTrigger(child);
                            });
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
         * Check if element is a tooltip trigger
         * @param {HTMLElement} element - The element to check
         * @returns {boolean} True if element is a tooltip trigger
         */
        isTooltipTrigger(element) {
            return element.hasAttribute('data-tooltip') ||
                   element.classList.contains('tooltip-help-icon') ||
                   element.getAttribute('role') === 'tooltip-trigger';
        }

        /**
         * Close all active tooltips
         */
        closeAllTooltips() {
            if (this.activeTooltip) {
                this.activeTooltip.classList.remove('tooltip-visible');
                this.activeTooltip.classList.add('hidden');
                this.activeTooltip.setAttribute('aria-hidden', 'true');
                this.activeTooltip = null;
            }
        }
    }

    /**
     * Initialize on DOM ready
     */
    function init() {
        // Create instance
        const tooltipAccessibility = new TooltipAccessibility();

        // Export for external use
        window.FinanpyTooltipAccessibility = {
            instance: tooltipAccessibility,
            closeAll: () => tooltipAccessibility.closeAllTooltips()
        };

        // Close tooltips on global Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' || e.keyCode === 27) {
                tooltipAccessibility.closeAllTooltips();
            }
        });
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
