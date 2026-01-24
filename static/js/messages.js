/**
 * Messages Module - Enhanced Notification System
 * Finanpy - Personal Finance Management System
 *
 * This module provides:
 * - Auto-dismiss messages after 5 seconds (except errors)
 * - Smooth slide-in and fade-out animations
 * - Progress bar showing remaining time
 * - Pause timer on hover
 * - Stack management for multiple messages
 * - Accessibility support with ARIA live regions
 */

(function() {
    'use strict';

    /**
     * Message class handles individual message behavior
     */
    class Message {
        constructor(element, manager) {
            this.element = element;
            this.manager = manager;
            this.progressBar = element.querySelector('[data-message-progress]');
            this.closeButton = element.querySelector('[data-message-close]');
            this.type = element.dataset.messageType || 'info';

            // Timer configuration
            this.duration = this.getDuration();
            this.startTime = null;
            this.remainingTime = this.duration;
            this.timerId = null;
            this.progressAnimationId = null;
            this.isPaused = false;

            // State
            this.isRemoving = false;

            this.init();
        }

        /**
         * Get duration based on message type
         * @returns {number} Duration in milliseconds
         */
        getDuration() {
            // Error messages don't auto-dismiss
            if (this.type === 'error') {
                return 0;
            }
            // All other messages: 5 seconds
            return 5000;
        }

        /**
         * Initialize message handlers
         */
        init() {
            // Slide in animation
            this.slideIn();

            // Add close button handler
            if (this.closeButton) {
                this.closeButton.addEventListener('click', () => this.dismiss());
            }

            // Add hover handlers to pause/resume timer
            this.element.addEventListener('mouseenter', () => this.pause());
            this.element.addEventListener('mouseleave', () => this.resume());

            // Start auto-dismiss timer if applicable
            if (this.duration > 0) {
                this.startTimer();
            } else {
                // Hide progress bar for messages that don't auto-dismiss
                if (this.progressBar) {
                    this.progressBar.style.display = 'none';
                }
            }
        }

        /**
         * Slide in animation
         */
        slideIn() {
            // Start from right (translateX: 100%)
            this.element.style.transform = 'translateX(100%)';
            this.element.style.opacity = '0';

            // Force reflow
            this.element.offsetHeight;

            // Animate to position
            requestAnimationFrame(() => {
                this.element.style.transition = 'transform 300ms ease-out, opacity 300ms ease-out';
                this.element.style.transform = 'translateX(0)';
                this.element.style.opacity = '1';
            });
        }

        /**
         * Start the auto-dismiss timer
         */
        startTimer() {
            this.startTime = Date.now();
            this.updateProgress();

            this.timerId = setTimeout(() => {
                this.dismiss();
            }, this.remainingTime);
        }

        /**
         * Update progress bar animation
         */
        updateProgress() {
            if (!this.progressBar || this.duration === 0) {
                return;
            }

            const updateFrame = () => {
                if (this.isPaused || this.isRemoving) {
                    return;
                }

                const elapsed = Date.now() - this.startTime;
                const remaining = Math.max(0, this.duration - elapsed);
                const progress = (remaining / this.duration) * 100;

                this.progressBar.style.width = `${progress}%`;

                if (remaining > 0) {
                    this.progressAnimationId = requestAnimationFrame(updateFrame);
                }
            };

            this.progressAnimationId = requestAnimationFrame(updateFrame);
        }

        /**
         * Pause the timer (on hover)
         */
        pause() {
            if (this.duration === 0 || this.isPaused || this.isRemoving) {
                return;
            }

            this.isPaused = true;

            // Calculate remaining time
            const elapsed = Date.now() - this.startTime;
            this.remainingTime = this.duration - elapsed;

            // Clear timer
            if (this.timerId) {
                clearTimeout(this.timerId);
                this.timerId = null;
            }

            // Cancel progress animation
            if (this.progressAnimationId) {
                cancelAnimationFrame(this.progressAnimationId);
                this.progressAnimationId = null;
            }

            // Add hover effect to element
            this.element.classList.add('message-hovered');
        }

        /**
         * Resume the timer (on mouse leave)
         */
        resume() {
            if (this.duration === 0 || !this.isPaused || this.isRemoving) {
                return;
            }

            this.isPaused = false;

            // Restart timer with remaining time
            this.startTime = Date.now();
            this.startTimer();

            // Remove hover effect
            this.element.classList.remove('message-hovered');
        }

        /**
         * Dismiss the message with animation
         */
        dismiss() {
            if (this.isRemoving) {
                return;
            }

            this.isRemoving = true;

            // Clear timers
            if (this.timerId) {
                clearTimeout(this.timerId);
            }
            if (this.progressAnimationId) {
                cancelAnimationFrame(this.progressAnimationId);
            }

            // Animate out
            this.element.style.transition = 'transform 300ms ease-in, opacity 300ms ease-in';
            this.element.style.transform = 'translateX(100%)';
            this.element.style.opacity = '0';

            // Remove from DOM after animation
            setTimeout(() => {
                if (this.element.parentNode) {
                    this.element.remove();
                }

                // Notify manager
                this.manager.onMessageRemoved(this);
            }, 300);
        }

        /**
         * Clean up resources
         */
        destroy() {
            if (this.timerId) {
                clearTimeout(this.timerId);
            }
            if (this.progressAnimationId) {
                cancelAnimationFrame(this.progressAnimationId);
            }
        }
    }

    /**
     * MessagesManager class handles all messages
     */
    class MessagesManager {
        constructor() {
            this.container = null;
            this.messages = [];
            this.init();
        }

        /**
         * Initialize the messages manager
         */
        init() {
            // Find messages container
            this.container = document.querySelector('[data-messages-container]');

            if (!this.container) {
                return;
            }

            // Initialize existing messages
            this.initializeExistingMessages();

            // Watch for new messages (dynamically added)
            this.observeNewMessages();
        }

        /**
         * Initialize existing messages on page load
         */
        initializeExistingMessages() {
            const messageElements = this.container.querySelectorAll('[data-message]');

            messageElements.forEach(element => {
                const message = new Message(element, this);
                this.messages.push(message);
            });
        }

        /**
         * Watch for dynamically added messages
         */
        observeNewMessages() {
            // Use MutationObserver to detect new messages
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1 && node.hasAttribute('data-message')) {
                            const message = new Message(node, this);
                            this.messages.push(message);
                        }
                    });
                });
            });

            observer.observe(this.container, {
                childList: true,
                subtree: false
            });
        }

        /**
         * Handle message removal
         * @param {Message} message - The message that was removed
         */
        onMessageRemoved(message) {
            const index = this.messages.indexOf(message);
            if (index > -1) {
                this.messages.splice(index, 1);
            }
        }

        /**
         * Dismiss all messages
         */
        dismissAll() {
            this.messages.forEach(message => message.dismiss());
        }

        /**
         * Add a new message programmatically
         * @param {string} text - Message text
         * @param {string} type - Message type (success, error, warning, info)
         */
        addMessage(text, type = 'info') {
            if (!this.container) {
                console.warn('Messages container not found');
                return;
            }

            // Create message element
            const messageElement = this.createMessageElement(text, type);

            // Add to container
            this.container.appendChild(messageElement);

            // Message will be automatically initialized by MutationObserver
        }

        /**
         * Create message element HTML
         * @param {string} text - Message text
         * @param {string} type - Message type
         * @returns {HTMLElement} Message element
         */
        createMessageElement(text, type) {
            const div = document.createElement('div');

            // Get colors based on type
            const colors = this.getTypeColors(type);

            div.setAttribute('data-message', '');
            div.setAttribute('data-message-type', type);
            div.setAttribute('role', 'alert');
            div.setAttribute('aria-live', 'polite');

            div.className = `${colors.bg} ${colors.text} ${colors.border} rounded-lg shadow-lg backdrop-blur-sm overflow-hidden`;

            div.innerHTML = `
                <div class="flex items-start p-4">
                    <div class="flex-shrink-0">
                        ${this.getIcon(type)}
                    </div>
                    <div class="ml-3 text-sm font-medium flex-1">
                        ${text}
                    </div>
                    <button type="button"
                            data-message-close
                            class="ml-4 -mt-1 -mr-1 flex-shrink-0 p-1.5 rounded-lg hover:bg-black/20 focus:ring-2 focus:ring-white/50 transition-all duration-200"
                            aria-label="Fechar">
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                        </svg>
                    </button>
                </div>
                <div class="h-1 ${colors.progressBg}">
                    <div data-message-progress class="${colors.progress} h-full w-full transition-all duration-100 ease-linear"></div>
                </div>
            `;

            return div;
        }

        /**
         * Get colors based on message type
         * @param {string} type - Message type
         * @returns {Object} Color classes
         */
        getTypeColors(type) {
            const colorMap = {
                success: {
                    bg: 'bg-green-500/10',
                    text: 'text-green-400',
                    border: 'border border-green-500/30',
                    progressBg: 'bg-green-900/30',
                    progress: 'bg-green-500'
                },
                error: {
                    bg: 'bg-red-500/10',
                    text: 'text-red-400',
                    border: 'border border-red-500/30',
                    progressBg: 'bg-red-900/30',
                    progress: 'bg-red-500'
                },
                warning: {
                    bg: 'bg-yellow-500/10',
                    text: 'text-yellow-400',
                    border: 'border border-yellow-500/30',
                    progressBg: 'bg-yellow-900/30',
                    progress: 'bg-yellow-500'
                },
                info: {
                    bg: 'bg-blue-500/10',
                    text: 'text-blue-400',
                    border: 'border border-blue-500/30',
                    progressBg: 'bg-blue-900/30',
                    progress: 'bg-blue-500'
                }
            };

            return colorMap[type] || colorMap.info;
        }

        /**
         * Get icon SVG based on message type
         * @param {string} type - Message type
         * @returns {string} Icon SVG HTML
         */
        getIcon(type) {
            const icons = {
                success: '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>',
                error: '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path></svg>',
                warning: '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>',
                info: '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>'
            };

            return icons[type] || icons.info;
        }
    }

    /**
     * Initialize on DOM ready
     */
    function init() {
        // Create MessagesManager instance
        const manager = new MessagesManager();

        // Export for external use
        window.FinanpyMessages = {
            manager: manager,
            addMessage: (text, type) => manager.addMessage(text, type),
            dismissAll: () => manager.dismissAll()
        };
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
