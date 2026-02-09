/* =====================================================
   PhilanthroForge - Premium Microinteractions
   Delightful UI moments that elevate the experience
   ===================================================== */

document.addEventListener('DOMContentLoaded', () => {

    // ==================
    // Button Ripple Effect
    // ==================
    const createRipple = (event) => {
        const button = event.currentTarget;

        // Create ripple element
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            left: ${x}px;
            top: ${y}px;
            transform: scale(0);
            pointer-events: none;
            animation: ripple 0.6s ease-out;
        `;

        // Add ripple animation CSS if not exists
        if (!document.querySelector('#ripple-animation')) {
            const style = document.createElement('style');
            style.id = 'ripple-animation';
            style.textContent = `
                @keyframes ripple {
                    to {
                        transform: scale(4);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);

        // Remove ripple after animation
        setTimeout(() => ripple.remove(), 600);
    };

    // Add ripple to all buttons
    document.querySelectorAll('.btn, button, [role="button"]').forEach(button => {
        button.addEventListener('click', createRipple);
    });

    // ==================
    // Card Tilt Effect (3D)
    // ==================
    const cards = document.querySelectorAll('.card, [data-tilt]');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
        });
    });

    // ==================
    // Magnetic Cursor Effect (Desktop only)
    // ==================
    if (window.innerWidth > 768) {
        const magneticElements = document.querySelectorAll('.btn-primary, [data-magnetic]');

        magneticElements.forEach(el => {
            el.addEventListener('mousemove', (e) => {
                const rect = el.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;

                el.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
            });

            el.addEventListener('mouseleave', () => {
                el.style.transform = 'translate(0, 0)';
            });
        });
    }

    // ==================
    // Form Input Focus Effects
    // ==================
    const inputs = document.querySelectorAll('input, textarea, select');

    inputs.forEach(input => {
        // Floating label effect
        const label = input.previousElementSibling;

        if (label && label.tagName === 'LABEL') {
            input.addEventListener('focus', () => {
                label.style.transform = 'translateY(-24px) scale(0.85)';
                label.style.color = 'var(--color-accent-primary)';
            });

            input.addEventListener('blur', () => {
                if (!input.value) {
                    label.style.transform = 'translateY(0) scale(1)';
                    label.style.color = 'var(--color-text-secondary)';
                }
            });
        }

        // Success checkmark animation
        input.addEventListener('blur', () => {
            if (input.validity.valid && input.value) {
                input.style.borderColor = 'var(--color-success)';

                // Add checkmark
                if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('checkmark')) {
                    const checkmark = document.createElement('span');
                    checkmark.className = 'checkmark';
                    checkmark.innerHTML = '✓';
                    checkmark.style.cssText = `
                        position: absolute;
                        right: 12px;
                        top: 50%;
                        transform: translateY(-50%) scale(0);
                        color: var(--color-success);
                        font-weight: bold;
                        animation: popIn 0.3s ease-out forwards;
                    `;
                    input.parentElement.style.position = 'relative';
                    input.parentElement.appendChild(checkmark);

                    // Add pop-in animation
                    if (!document.querySelector('#popIn-animation')) {
                        const style = document.createElement('style');
                        style.id = 'popIn-animation';
                        style.textContent = `
                            @keyframes popIn {
                                to {
                                    transform: translateY(-50%) scale(1);
                                }
                            }
                        `;
                        document.head.appendChild(style);
                    }
                }
            }
        });
    });

    // ==================
    // Navigation Link Underline Animation
    // ==================
    const navLinks = document.querySelectorAll('nav a, .nav-link');

    navLinks.forEach(link => {
        if (!link.querySelector('::after')) {
            link.classList.add('link-animated');
        }
    });

    // ==================
    // Icon Hover Animations
    // ==================
    const icons = document.querySelectorAll('.icon, [class*="icon-"], svg');

    icons.forEach(icon => {
        // Exclude SVGs inside the rotating graphic wrapper
        if (icon.closest('.sir-circle-wrapper')) {
            return;
        }

        icon.addEventListener('mouseenter', () => {
            icon.style.transform = 'rotate(360deg) scale(1.1)';
            icon.style.transition = 'transform 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
        });

        icon.addEventListener('mouseleave', () => {
            icon.style.transform = 'rotate(0deg) scale(1)';
        });
    });

    // ==================
    // Scroll-triggered Nav Bar Shrink
    // ==================
    const navbar = document.querySelector('nav, .navbar');
    let lastScroll = 0;

    if (navbar) {
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;

            if (currentScroll > 100) {
                navbar.classList.add('scrolled');
                navbar.style.transform = currentScroll > lastScroll ? 'translateY(-100%)' : 'translateY(0)';
            } else {
                navbar.classList.remove('scrolled');
                navbar.style.transform = 'translateY(0)';
            }

            lastScroll = currentScroll;
        });
    }

    // ==================
    // Mega Menu Hover Effects
    // ==================
    const megaMenuTriggers = document.querySelectorAll('[data-mega-menu-trigger], .group');

    megaMenuTriggers.forEach(trigger => {
        const menu = trigger.querySelector('.absolute, [class*="dropdown"]');

        if (menu) {
            trigger.addEventListener('mouseenter', () => {
                menu.style.animation = 'slideDown 0.3s cubic-bezier(0.22, 1, 0.36, 1) forwards';
            });

            // Add slideDown animation
            if (!document.querySelector('#slideDown-animation')) {
                const style = document.createElement('style');
                style.id = 'slideDown-animation';
                style.textContent = `
                    @keyframes slideDown {
                        from {
                            opacity: 0;
                            transform: translateY(-10px);
                        }
                        to {
                            opacity: 1;
                            transform: translateY(0);
                        }
                    }
                `;
                document.head.appendChild(style);
            }
        }
    });

    // ==================
    // Image Hover Zoom
    // ==================
    const hoverImages = document.querySelectorAll('.card img, [data-hover-zoom]');

    hoverImages.forEach(img => {
        img.style.transition = 'transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';

        img.parentElement.addEventListener('mouseenter', () => {
            img.style.transform = 'scale(1.08)';
        });

        img.parentElement.addEventListener('mouseleave', () => {
            img.style.transform = 'scale(1)';
        });
    });

    // ==================
    // Confetti on Success (Newsletter, Forms)
    // ==================
    window.triggerConfetti = (element) => {
        const colors = ['#ff9f1c', '#ff6b6b', '#4ecdc4', '#7a9b76'];
        const confettiCount = 40;

        for (let i = 0; i < confettiCount; i++) {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: fixed;
                width: 10px;
                height: 10px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                left: 50%;
                top: 50%;
                opacity: 1;
                pointer-events: none;
                animation: confettiFall ${1 + Math.random()}s ease-out forwards;
                transform: translate(${Math.random() * 200 - 100}px, ${Math.random() * 200 - 100}px) rotate(${Math.random() * 360}deg);
            `;
            document.body.appendChild(confetti);

            setTimeout(() => confetti.remove(), 2000);
        }

        // Add confetti animation
        if (!document.querySelector('#confetti-animation')) {
            const style = document.createElement('style');
            style.id = 'confetti-animation';
            style.textContent = `
                @keyframes confettiFall {
                    to {
                        transform: translateY(100vh) rotate(720deg);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    };

    // ==================
    // Smooth Number Increment (Visible counters)
    // ==================
    const observeCounters = () => {
        const counters = document.querySelectorAll('[data-count]');

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                    const target = parseInt(entry.target.dataset.count);
                    const duration = 2000;
                    const start = 0;
                    const increment = target / (duration / 16);
                    let current = start;

                    const timer = setInterval(() => {
                        current += increment;
                        if (current >= target) {
                            entry.target.textContent = target;
                            clearInterval(timer);
                            entry.target.classList.add('counted');
                        } else {
                            entry.target.textContent = Math.ceil(current);
                        }
                    }, 16);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(counter => observer.observe(counter));
    };

    observeCounters();

    // ==================
    // Toast Notifications
    // ==================
    window.showToast = (message, type = 'success') => {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 32px;
            right: 32px;
            padding: 16px 24px;
            background: ${type === 'success' ? 'var(--color-success)' : 'var(--color-error)'};
            color: white;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-xl);
            z-index: 10000;
            animation: slideInRight 0.3s ease-out;
        `;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }, 3000);

        // Add slide animations
        if (!document.querySelector('#toast-animations')) {
            const style = document.createElement('style');
            style.id = 'toast-animations';
            style.textContent = `
                @keyframes slideInRight {
                    from {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
                @keyframes slideOutRight {
                    to {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    };

    console.log('✨ Premium microinteractions loaded');
});
