/**
 * Component Loader
 * Dynamically loads navbar and footer components
 */

(function () {
    'use strict';

    // Determine component path based on current page depth
    // Determine component path based on current page depth
    function getComponentPath(componentName) {
        const parts = window.location.pathname.split('/').filter(Boolean);
        // If empty (root) or index.html in root, depth is 0
        const isRoot = parts.length === 0 || (parts.length === 1 && parts[0] === 'index.html');
        const depth = isRoot ? 0 : parts.length - 1;
        // Adjust for /services/service-name.html -> depth 1

        // Simpler approach: count / excluding the first one?
        // Let's stick to valid relative logic
        let pathPrefix = '';
        if (parts.length > 0 && parts[0] !== 'index.html') {
            // For /about.html, depth 0. parts=['about.html']
            // For /services/foo.html, depth 1. parts=['services', 'foo.html']
            // Actually, relative path from /services/foo.html to /components/navbar.html is ../../components/navbar.html
            // Wait, standard structure:
            // /index.html -> components/navbar.html
            // /services/foo.html -> ../components/navbar.html

            // The old logic was: length - 1. 
            // ['services', 'foo.html'] len 2 - 1 = 1. Prefix '../'. Correct.
            // ['index.html'] len 1 - 1 = 0. Prefix ''. Correct.
            // [] (Root) len 0 - 1 = -1. Prefix '../../' (by fallthrough). Incorrect.

            // Fix: verify depth >= 0
        }

        const pathDepth = parts.length === 0 ? 0 : parts.length - 1;
        const prefix = pathDepth <= 0 ? '' : pathDepth === 1 ? '../' : '../../';
        return `${prefix}components/${componentName}.html`;
    }

    // Adjust asset paths based on current page depth
    function adjustAssetPaths(html, depth) {
        const prefix = depth === 0 ? '' : depth === 1 ? '../' : '../../';

        // Replace asset paths
        return html
            .replace(/src="assets\//g, `src="${prefix}assets/`)
            .replace(/href="assets\//g, `href="${prefix}assets/`)
            // Fix links that shouldn't have prefixes (they're fine as-is for same directory)
            .replace(/href="index\.html"/g, `href="${prefix}index.html"`)
            .replace(/href="about\.html"/g, `href="${prefix}about.html"`)
            .replace(/href="services\.html"/g, `href="${prefix}services.html"`)
            .replace(/href="case-studies\.html"/g, `href="${prefix}case-studies.html"`)
            .replace(/href="lets-talk\.html"/g, `href="${prefix}lets-talk.html"`)
            .replace(/href="privacy-policy\.html"/g, `href="${prefix}privacy-policy.html"`)
            .replace(/href="terms-and-conditions\.html"/g, `href="${prefix}terms-and-conditions.html"`)
            // Fix service and case study links
            .replace(/href="services\//g, `href="${prefix}services/`)
            .replace(/href="case-studies\//g, `href="${prefix}case-studies/`);
    }

    // Load component
    async function loadComponent(placeholderId, componentName) {
        try {
            const depth = window.location.pathname.split('/').filter(Boolean).length - 1;
            const componentPath = getComponentPath(componentName);

            const response = await fetch(componentPath);
            if (!response.ok) {
                throw new Error(`Failed to load ${componentName}: ${response.statusText}`);
            }

            let html = await response.text();

            // Adjust paths if we're in a subdirectory
            if (depth > 0) {
                html = adjustAssetPaths(html, depth);
            }

            const placeholder = document.getElementById(placeholderId);
            if (placeholder) {
                placeholder.innerHTML = html;

                // If navbar was loaded, reinitialize mobile menu
                if (componentName === 'navbar') {
                    initializeMobileMenu();
                }
            }
        } catch (error) {
            console.error(`Error loading ${componentName}:`, error);
        }
    }

    // Initialize mobile menu functionality
    function initializeMobileMenu() {
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const closeMobileMenu = document.getElementById('close-mobile-menu');
        const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
        const mobileMenuPanel = document.getElementById('mobile-menu-panel');

        function openMenu() {
            if (mobileMenuOverlay && mobileMenuPanel) {
                mobileMenuOverlay.classList.remove('hidden');
                mobileMenuPanel.classList.remove('translate-x-full');
                setTimeout(() => mobileMenuOverlay.classList.add('opacity-100'), 10);
                document.body.style.overflow = 'hidden';
            }
        }

        function closeMenu() {
            if (mobileMenuOverlay && mobileMenuPanel) {
                mobileMenuOverlay.classList.remove('opacity-100');
                mobileMenuPanel.classList.add('translate-x-full');
                setTimeout(() => {
                    mobileMenuOverlay.classList.add('hidden');
                    document.body.style.overflow = '';
                }, 300);
            }
        }

        if (mobileMenuBtn) {
            mobileMenuBtn.addEventListener('click', openMenu);
        }

        if (closeMobileMenu) {
            closeMobileMenu.addEventListener('click', closeMenu);
        }

        if (mobileMenuOverlay) {
            mobileMenuOverlay.addEventListener('click', closeMenu);
        }

        // Dropdown toggles
        document.querySelectorAll('[data-dropdown-toggle]').forEach(button => {
            button.addEventListener('click', function () {
                const targetId = this.getAttribute('data-dropdown-toggle');
                const dropdown = document.getElementById(targetId);
                const arrow = this.querySelector('[data-dropdown-arrow]');

                if (dropdown) {
                    dropdown.classList.toggle('hidden');
                    if (arrow) {
                        arrow.classList.toggle('rotate-180');
                    }
                }
            });
        });
    }

    // Load components when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            loadComponent('navbar-placeholder', 'navbar');
            loadComponent('footer-placeholder', 'footer');
        });
    } else {
        loadComponent('navbar-placeholder', 'navbar');
        loadComponent('footer-placeholder', 'footer');
    }
})();
