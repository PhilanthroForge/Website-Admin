/**
 * PhilanthroForge Mobile Menu
 * World-class mobile navigation with Nordic design principles
 */

(function () {
    'use strict';

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMobileMenu);
    } else {
        initMobileMenu();
    }

    function initMobileMenu() {
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
        const mobileMenuPanel = document.getElementById('mobile-menu-panel');
        const closeMobileMenuBtn = document.getElementById('close-mobile-menu');

        if (!mobileMenuBtn || !mobileMenuOverlay || !mobileMenuPanel) {
            console.warn('PhilanthroForge: Mobile menu elements not found');
            return;
        }

        // Toggle mobile menu
        function toggleMobileMenu(shouldOpen) {
            const isOpen = !mobileMenuPanel.classList.contains('translate-x-full');
            const targetState = shouldOpen !== undefined ? shouldOpen : !isOpen;

            if (targetState) {
                openMobileMenu();
            } else {
                closeMobileMenu();
            }
        }

        function openMobileMenu() {
            mobileMenuPanel.classList.remove('translate-x-full');
            mobileMenuOverlay.classList.remove('hidden', 'opacity-0');
            mobileMenuOverlay.classList.add('opacity-100');
            document.body.style.overflow = 'hidden';
            mobileMenuBtn.setAttribute('aria-expanded', 'true');

            // Focus first focusable element
            setTimeout(() => {
                const firstFocusable = mobileMenuPanel.querySelector('a, button');
                if (firstFocusable) firstFocusable.focus();
            }, 300);
        }

        function closeMobileMenu() {
            mobileMenuPanel.classList.add('translate-x-full');
            mobileMenuOverlay.classList.remove('opacity-100');
            mobileMenuOverlay.classList.add('opacity-0');

            setTimeout(() => {
                mobileMenuOverlay.classList.add('hidden');
            }, 300);

            document.body.style.overflow = '';
            mobileMenuBtn.setAttribute('aria-expanded', 'false');
            mobileMenuBtn.focus();
        }

        // Event listeners
        if (mobileMenuBtn) {
            mobileMenuBtn.addEventListener('click', () => toggleMobileMenu());
        }

        if (closeMobileMenuBtn) {
            closeMobileMenuBtn.addEventListener('click', () => toggleMobileMenu(false));
        }

        if (mobileMenuOverlay) {
            mobileMenuOverlay.addEventListener('click', () => toggleMobileMenu(false));
        }

        // Handle dropdown toggles
        const dropdownToggles = mobileMenuPanel.querySelectorAll('[data-dropdown-toggle]');
        dropdownToggles.forEach(toggle => {
            toggle.addEventListener('click', function () {
                const targetId = this.getAttribute('data-dropdown-toggle');
                const dropdown = document.getElementById(targetId);
                const arrow = this.querySelector('[data-dropdown-arrow]');

                if (dropdown) {
                    dropdown.classList.toggle('hidden');
                    if (arrow) {
                        arrow.classList.toggle('rotate-180');
                    }

                    // Update ARIA
                    const isExpanded = !dropdown.classList.contains('hidden');
                    this.setAttribute('aria-expanded', isExpanded);
                }
            });
        });

        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                const isOpen = !mobileMenuPanel.classList.contains('translate-x-full');
                if (isOpen) {
                    toggleMobileMenu(false);
                }
            }
        });

        // Close on navigation
        const mobileLinks = mobileMenuPanel.querySelectorAll('a:not([data-dropdown-toggle])');
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                // Small delay to allow navigation
                setTimeout(() => closeMobileMenu(), 100);
            });
        });

        // Handle resize - close menu if viewport becomes desktop
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                if (window.innerWidth >= 768) { // md breakpoint
                    const isOpen = !mobileMenuPanel.classList.contains('translate-x-full');
                    if (isOpen) {
                        closeMobileMenu();
                    }
                }
            }, 250);
        });

        // Prevent body scroll when menu is open
        mobileMenuPanel.addEventListener('touchmove', (e) => {
            e.stopPropagation();
        }, { passive: false });
    }
})();
