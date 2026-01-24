/**
 * Tooltips Module - Interactive Help System
 * Finanpy - Personal Finance Management System
 *
 * This module provides:
 * - Pure CSS/JS tooltips without external libraries
 * - Hover and focus interactions
 * - Automatic positioning (top, bottom, left, right)
 * - Smooth fade in/out animations
 * - Keyboard accessible (Escape to close)
 * - Responsive positioning based on viewport
 */

(function() {
    'use strict';

    /**
     * Tooltip class handles individual tooltip behavior
     */
    class Tooltip {
        constructor(element) {
            this.element = element;
            this.text = element.getAttribute('data-tooltip');
            this.position = element.getAttribute('data-tooltip-position') || 'top';
            this.tooltipElement = null;
            this.isVisible = false;
            this.showDelay = 200;
            this.hideDelay = 100;
            this.showTimeout = null;
            this.hideTimeout = null;

            // Bind methods
            this.show = this.show.bind(this);
            this.hide = this.hide.bind(this);
            this.handleKeyDown = this.handleKeyDown.bind(this);

            this.init();
        }

        /**
         * Initialize tooltip handlers
         */
        init() {
            if (!this.text) {
                console.warn('Tooltip element missing data-tooltip attribute', this.element);
                return;
            }

            // Add hover handlers
            this.element.addEventListener('mouseenter', () => this.scheduleShow());
            this.element.addEventListener('mouseleave', () => this.scheduleHide());

            // Add focus handlers for accessibility
            this.element.addEventListener('focus', () => this.scheduleShow());
            this.element.addEventListener('blur', () => this.scheduleHide());

            // Add keyboard handler
            document.addEventListener('keydown', this.handleKeyDown);

            // Add ARIA attributes
            this.element.setAttribute('aria-describedby', this.getTooltipId());
        }

        /**
         * Get unique tooltip ID
         * @returns {string} Unique tooltip ID
         */
        getTooltipId() {
            if (!this.element.id) {
                this.element.id = `tooltip-trigger-${Math.random().toString(36).substr(2, 9)}`;
            }
            return `${this.element.id}-tooltip`;
        }

        /**
         * Schedule tooltip show with delay
         */
        scheduleShow() {
            // Clear any pending hide
            if (this.hideTimeout) {
                clearTimeout(this.hideTimeout);
                this.hideTimeout = null;
            }

            // Schedule show
            this.showTimeout = setTimeout(() => {
                this.show();
            }, this.showDelay);
        }

        /**
         * Schedule tooltip hide with delay
         */
        scheduleHide() {
            // Clear any pending show
            if (this.showTimeout) {
                clearTimeout(this.showTimeout);
                this.showTimeout = null;
            }

            // Schedule hide
            this.hideTimeout = setTimeout(() => {
                this.hide();
            }, this.hideDelay);
        }

        /**
         * Show the tooltip
         */
        show() {
            if (this.isVisible) {
                return;
            }

            this.isVisible = true;

            // Create tooltip element
            this.createTooltip();

            // Add to DOM
            document.body.appendChild(this.tooltipElement);

            // Position tooltip
            this.positionTooltip();

            // Animate in
            requestAnimationFrame(() => {
                this.tooltipElement.classList.add('tooltip-visible');
            });
        }

        /**
         * Hide the tooltip
         */
        hide() {
            if (!this.isVisible || !this.tooltipElement) {
                return;
            }

            this.isVisible = false;

            // Animate out
            this.tooltipElement.classList.remove('tooltip-visible');

            // Remove from DOM after animation
            setTimeout(() => {
                if (this.tooltipElement && this.tooltipElement.parentNode) {
                    this.tooltipElement.remove();
                }
                this.tooltipElement = null;
            }, 200);
        }

        /**
         * Create tooltip DOM element
         */
        createTooltip() {
            const tooltip = document.createElement('div');
            tooltip.id = this.getTooltipId();
            tooltip.className = 'tooltip';
            tooltip.setAttribute('role', 'tooltip');
            tooltip.setAttribute('aria-hidden', 'false');

            // Tooltip content
            const content = document.createElement('div');
            content.className = 'tooltip-content';
            content.textContent = this.text;

            // Tooltip arrow
            const arrow = document.createElement('div');
            arrow.className = 'tooltip-arrow';

            tooltip.appendChild(content);
            tooltip.appendChild(arrow);

            this.tooltipElement = tooltip;
        }

        /**
         * Position the tooltip relative to trigger element
         */
        positionTooltip() {
            if (!this.tooltipElement) {
                return;
            }

            const triggerRect = this.element.getBoundingClientRect();
            const tooltipRect = this.tooltipElement.getBoundingClientRect();
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;

            // Gap between tooltip and trigger
            const gap = 8;

            let top, left, actualPosition;

            // Try preferred position first, then fallback
            actualPosition = this.position;
            const positions = this.calculatePositions(triggerRect, tooltipRect, scrollTop, scrollLeft, gap);

            // Check if preferred position fits in viewport
            if (!this.fitsInViewport(positions[this.position], tooltipRect)) {
                // Try other positions
                const preferredOrder = ['top', 'bottom', 'right', 'left'];
                for (const pos of preferredOrder) {
                    if (this.fitsInViewport(positions[pos], tooltipRect)) {
                        actualPosition = pos;
                        break;
                    }
                }
            }

            // Set position
            const finalPosition = positions[actualPosition];
            this.tooltipElement.style.top = `${finalPosition.top}px`;
            this.tooltipElement.style.left = `${finalPosition.left}px`;

            // Set arrow position class
            this.tooltipElement.setAttribute('data-position', actualPosition);
        }

        /**
         * Calculate all possible tooltip positions
         * @returns {Object} Position coordinates for each direction
         */
        calculatePositions(triggerRect, tooltipRect, scrollTop, scrollLeft, gap) {
            return {
                top: {
                    top: triggerRect.top + scrollTop - tooltipRect.height - gap,
                    left: triggerRect.left + scrollLeft + (triggerRect.width / 2) - (tooltipRect.width / 2)
                },
                bottom: {
                    top: triggerRect.bottom + scrollTop + gap,
                    left: triggerRect.left + scrollLeft + (triggerRect.width / 2) - (tooltipRect.width / 2)
                },
                left: {
                    top: triggerRect.top + scrollTop + (triggerRect.height / 2) - (tooltipRect.height / 2),
                    left: triggerRect.left + scrollLeft - tooltipRect.width - gap
                },
                right: {
                    top: triggerRect.top + scrollTop + (triggerRect.height / 2) - (tooltipRect.height / 2),
                    left: triggerRect.right + scrollLeft + gap
                }
            };
        }

        /**
         * Check if tooltip fits in viewport at given position
         * @returns {boolean} True if fits
         */
        fitsInViewport(position, tooltipRect) {
            const viewportWidth = window.innerWidth;
            const viewportHeight = window.innerHeight;
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;

            const padding = 8; // Padding from viewport edges

            return (
                position.left - scrollLeft >= padding &&
                position.left - scrollLeft + tooltipRect.width <= viewportWidth - padding &&
                position.top - scrollTop >= padding &&
                position.top - scrollTop + tooltipRect.height <= viewportHeight - padding
            );
        }

        /**
         * Handle keyboard events
         */
        handleKeyDown(e) {
            if ((e.key === 'Escape' || e.keyCode === 27) && this.isVisible) {
                this.hide();
            }
        }

        /**
         * Destroy tooltip and clean up
         */
        destroy() {
            // Clear timeouts
            if (this.showTimeout) {
                clearTimeout(this.showTimeout);
            }
            if (this.hideTimeout) {
                clearTimeout(this.hideTimeout);
            }

            // Remove event listeners
            document.removeEventListener('keydown', this.handleKeyDown);

            // Hide tooltip
            this.hide();
        }
    }

    /**
     * TooltipManager class manages all tooltips on the page
     */
    class TooltipManager {
        constructor() {
            this.tooltips = new Map();
            this.init();
        }

        /**
         * Initialize all tooltips on the page
         */
        init() {
            // Find all tooltip triggers
            this.initializeTooltips();

            // Watch for dynamically added tooltips
            this.observeNewTooltips();

            // Add CSS styles
            this.injectStyles();
        }

        /**
         * Initialize existing tooltip triggers
         */
        initializeTooltips() {
            const tooltipTriggers = document.querySelectorAll('[data-tooltip]');

            tooltipTriggers.forEach(element => {
                if (!this.tooltips.has(element)) {
                    const tooltip = new Tooltip(element);
                    this.tooltips.set(element, tooltip);
                }
            });
        }

        /**
         * Watch for dynamically added tooltips
         */
        observeNewTooltips() {
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1) {
                            // Check if node itself has tooltip
                            if (node.hasAttribute('data-tooltip')) {
                                if (!this.tooltips.has(node)) {
                                    const tooltip = new Tooltip(node);
                                    this.tooltips.set(node, tooltip);
                                }
                            }

                            // Check for tooltip triggers in children
                            const children = node.querySelectorAll('[data-tooltip]');
                            children.forEach(child => {
                                if (!this.tooltips.has(child)) {
                                    const tooltip = new Tooltip(child);
                                    this.tooltips.set(child, tooltip);
                                }
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
         * Inject tooltip CSS styles
         */
        injectStyles() {
            // Check if styles already injected
            if (document.getElementById('finanpy-tooltip-styles')) {
                return;
            }

            const style = document.createElement('style');
            style.id = 'finanpy-tooltip-styles';
            style.textContent = `
                /* Tooltip Base Styles */
                .tooltip {
                    position: absolute;
                    z-index: 9999;
                    opacity: 0;
                    visibility: hidden;
                    transition: opacity 200ms ease-out, visibility 200ms ease-out;
                    pointer-events: none;
                }

                .tooltip.tooltip-visible {
                    opacity: 1;
                    visibility: visible;
                }

                .tooltip-content {
                    background-color: rgba(31, 41, 55, 0.95);
                    color: #f3f4f6;
                    font-size: 0.875rem;
                    line-height: 1.5;
                    padding: 0.5rem 0.75rem;
                    border-radius: 0.5rem;
                    border: 1px solid rgba(75, 85, 99, 0.5);
                    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.15);
                    max-width: 250px;
                    word-wrap: break-word;
                    backdrop-filter: blur(8px);
                }

                /* Tooltip Arrow */
                .tooltip-arrow {
                    position: absolute;
                    width: 0;
                    height: 0;
                    border: 6px solid transparent;
                }

                /* Arrow positioning based on tooltip position */
                .tooltip[data-position="top"] .tooltip-arrow {
                    bottom: -12px;
                    left: 50%;
                    transform: translateX(-50%);
                    border-top-color: rgba(31, 41, 55, 0.95);
                    border-bottom: none;
                }

                .tooltip[data-position="bottom"] .tooltip-arrow {
                    top: -12px;
                    left: 50%;
                    transform: translateX(-50%);
                    border-bottom-color: rgba(31, 41, 55, 0.95);
                    border-top: none;
                }

                .tooltip[data-position="left"] .tooltip-arrow {
                    right: -12px;
                    top: 50%;
                    transform: translateY(-50%);
                    border-left-color: rgba(31, 41, 55, 0.95);
                    border-right: none;
                }

                .tooltip[data-position="right"] .tooltip-arrow {
                    left: -12px;
                    top: 50%;
                    transform: translateY(-50%);
                    border-right-color: rgba(31, 41, 55, 0.95);
                    border-left: none;
                }

                /* Help icon styles */
                .tooltip-help-icon {
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    width: 1rem;
                    height: 1rem;
                    color: #9ca3af;
                    cursor: help;
                    transition: color 200ms ease;
                    vertical-align: middle;
                    margin-left: 0.25rem;
                }

                .tooltip-help-icon:hover,
                .tooltip-help-icon:focus {
                    color: #d1d5db;
                    outline: none;
                }

                .tooltip-help-icon svg {
                    width: 100%;
                    height: 100%;
                }
            `;

            document.head.appendChild(style);
        }

        /**
         * Destroy all tooltips
         */
        destroyAll() {
            this.tooltips.forEach(tooltip => tooltip.destroy());
            this.tooltips.clear();
        }
    }

    /**
     * Initialize on DOM ready
     */
    function init() {
        // Create TooltipManager instance
        const manager = new TooltipManager();

        // Export for external use
        window.FinanpyTooltips = {
            manager: manager,
            destroyAll: () => manager.destroyAll()
        };
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
