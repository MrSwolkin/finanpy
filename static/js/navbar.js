/**
 * Navbar Module - JavaScript for Responsive Navigation
 * Finanpy - Personal Finance Management System
 *
 * This module provides:
 * - Mobile menu toggle functionality
 * - User dropdown menu interactions
 * - Sticky navbar with scroll shadow effect
 * - Click outside to close menus
 */

(function() {
    'use strict';

    /**
     * Navbar class handles all navigation interactions
     */
    class Navbar {
        constructor() {
            // Navbar elements
            this.navbar = document.getElementById('navbar');

            // Mobile menu elements
            this.mobileMenuButton = document.getElementById('mobile-menu-button');
            this.mobileMenu = document.getElementById('mobile-menu');
            this.hamburgerIcon = document.getElementById('hamburger-icon');
            this.closeIcon = document.getElementById('close-icon');

            // User dropdown elements (desktop)
            this.userMenuButton = document.getElementById('user-menu-button');
            this.userMenuDropdown = document.getElementById('user-menu-dropdown');
            this.userMenuIcon = document.getElementById('user-menu-icon');

            // State
            this.isMobileMenuOpen = false;
            this.isUserMenuOpen = false;

            // Initialize if elements exist
            if (this.navbar) {
                this.init();
            }
        }

        /**
         * Initialize all navbar handlers
         */
        init() {
            this.initMobileMenu();
            this.initUserDropdown();
            this.initStickyNavbar();
            this.initClickOutside();
            this.initEscapeKey();
        }

        /**
         * Initialize mobile menu toggle - Task 39.4, 39.6
         */
        initMobileMenu() {
            if (!this.mobileMenuButton || !this.mobileMenu) {
                return;
            }

            // Toggle mobile menu on button click
            this.mobileMenuButton.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleMobileMenu();
            });

            // Close mobile menu when clicking on links
            const mobileLinks = this.mobileMenu.querySelectorAll('a');
            mobileLinks.forEach(link => {
                link.addEventListener('click', () => {
                    this.closeMobileMenu();
                });
            });
        }

        /**
         * Toggle mobile menu open/closed
         */
        toggleMobileMenu() {
            this.isMobileMenuOpen = !this.isMobileMenuOpen;

            if (this.isMobileMenuOpen) {
                this.openMobileMenu();
            } else {
                this.closeMobileMenu();
            }
        }

        /**
         * Open mobile menu
         */
        openMobileMenu() {
            this.isMobileMenuOpen = true;
            this.mobileMenu.classList.remove('hidden');
            this.mobileMenuButton.setAttribute('aria-expanded', 'true');

            // Toggle icons
            if (this.hamburgerIcon && this.closeIcon) {
                this.hamburgerIcon.classList.add('hidden');
                this.closeIcon.classList.remove('hidden');
            }

            // Close user dropdown if open
            this.closeUserDropdown();

            // Prevent body scroll on mobile when menu is open
            document.body.style.overflow = 'hidden';
        }

        /**
         * Close mobile menu
         */
        closeMobileMenu() {
            this.isMobileMenuOpen = false;
            this.mobileMenu.classList.add('hidden');
            this.mobileMenuButton.setAttribute('aria-expanded', 'false');

            // Toggle icons
            if (this.hamburgerIcon && this.closeIcon) {
                this.hamburgerIcon.classList.remove('hidden');
                this.closeIcon.classList.add('hidden');
            }

            // Restore body scroll
            document.body.style.overflow = '';
        }

        /**
         * Initialize user dropdown menu (desktop) - Task 39.5
         */
        initUserDropdown() {
            if (!this.userMenuButton || !this.userMenuDropdown) {
                return;
            }

            // Toggle dropdown on button click
            this.userMenuButton.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleUserDropdown();
            });
        }

        /**
         * Toggle user dropdown open/closed
         */
        toggleUserDropdown() {
            this.isUserMenuOpen = !this.isUserMenuOpen;

            if (this.isUserMenuOpen) {
                this.openUserDropdown();
            } else {
                this.closeUserDropdown();
            }
        }

        /**
         * Open user dropdown
         */
        openUserDropdown() {
            this.isUserMenuOpen = true;
            this.userMenuDropdown.classList.remove('hidden');
            this.userMenuButton.setAttribute('aria-expanded', 'true');

            // Rotate icon
            if (this.userMenuIcon) {
                this.userMenuIcon.style.transform = 'rotate(180deg)';
            }

            // Close mobile menu if open
            this.closeMobileMenu();
        }

        /**
         * Close user dropdown
         */
        closeUserDropdown() {
            this.isUserMenuOpen = false;
            this.userMenuDropdown.classList.add('hidden');
            this.userMenuButton.setAttribute('aria-expanded', 'false');

            // Reset icon rotation
            if (this.userMenuIcon) {
                this.userMenuIcon.style.transform = 'rotate(0deg)';
            }
        }

        /**
         * Initialize sticky navbar with scroll shadow - Task 39.7
         */
        initStickyNavbar() {
            if (!this.navbar) {
                return;
            }

            // Add shadow on scroll
            let lastScrollY = window.scrollY;
            let ticking = false;

            const updateNavbar = () => {
                const scrollY = window.scrollY;

                if (scrollY > 10) {
                    this.navbar.classList.add('shadow-xl');
                } else {
                    this.navbar.classList.remove('shadow-xl');
                }

                lastScrollY = scrollY;
                ticking = false;
            };

            window.addEventListener('scroll', () => {
                if (!ticking) {
                    window.requestAnimationFrame(updateNavbar);
                    ticking = true;
                }
            });

            // Initial check
            updateNavbar();
        }

        /**
         * Initialize click outside to close menus - Task 39.6
         */
        initClickOutside() {
            document.addEventListener('click', (e) => {
                // Close mobile menu if clicking outside
                if (this.isMobileMenuOpen &&
                    this.mobileMenu &&
                    !this.mobileMenu.contains(e.target) &&
                    !this.mobileMenuButton.contains(e.target)) {
                    this.closeMobileMenu();
                }

                // Close user dropdown if clicking outside
                if (this.isUserMenuOpen &&
                    this.userMenuDropdown &&
                    !this.userMenuDropdown.contains(e.target) &&
                    !this.userMenuButton.contains(e.target)) {
                    this.closeUserDropdown();
                }
            });
        }

        /**
         * Initialize escape key to close menus
         */
        initEscapeKey() {
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' || e.keyCode === 27) {
                    if (this.isMobileMenuOpen) {
                        this.closeMobileMenu();
                    }
                    if (this.isUserMenuOpen) {
                        this.closeUserDropdown();
                    }
                }
            });
        }

        /**
         * Close all menus (public method)
         */
        closeAll() {
            this.closeMobileMenu();
            this.closeUserDropdown();
        }
    }

    /**
     * Initialize on DOM ready
     */
    function init() {
        // Create navbar instance
        const navbar = new Navbar();

        // Export for external use if needed
        window.FinanpyNavbar = navbar;
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
