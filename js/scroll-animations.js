/* =====================================================
   PhilanthroForge - Scroll Animations (GSAP)
   Cinematic scrollytelling with rotating graphics
   ===================================================== */

// Wait for DOM and GSAP to load
document.addEventListener('DOMContentLoaded', () => {
    // Check if GSAP and ScrollTrigger are loaded
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
        console.warn('GSAP or ScrollTrigger not loaded. Scroll animations disabled.');
        return;
    }

    // Register ScrollTrigger plugin
    gsap.registerPlugin(ScrollTrigger);

    // ==================
    // Scroll Progress Indicator
    // ==================
    const createScrollProgress = () => {
        // Create progress bar if it doesn't exist
        if (!document.querySelector('.scroll-progress')) {
            const progressBar = document.createElement('div');
            progressBar.className = 'scroll-progress';
            progressBar.innerHTML = '<div class="scroll-progress-bar"></div>';
            document.body.prepend(progressBar);
        }

        const progressBar = document.querySelector('.scroll-progress-bar');

        gsap.to(progressBar, {
            scaleX: 1,
            ease: 'none',
            scrollTrigger: {
                trigger: document.body,
                start: 'top top',
                end: 'bottom bottom',
                scrub: 0.3
            }
        });
    };

    // ==================
    // Rotating Graphic Scroll Animation
    // ==================
    const animateRotatingGraphics = () => {
        const graphics = document.querySelectorAll('.rotating-animation, [class*="rotating"]');

        graphics.forEach((graphic, index) => {
            // Check if it's the hero graphic or section graphic
            const isHero = graphic.closest('.hero, header, nav');

            if (isHero) {
                // Hero section: Scale and rotate based on scroll
                gsap.to(graphic, {
                    scale: 1.3,
                    rotation: 180,
                    ease: 'none',
                    scrollTrigger: {
                        trigger: graphic.closest('section, header'),
                        start: 'top top',
                        end: 'bottom top',
                        scrub: 1,
                        onUpdate: (self) => {
                            // Optional: Change opacity based on scroll
                            const opacity = 1 - (self.progress * 0.3);
                            graphic.style.opacity = opacity;
                        }
                    }
                });
            } else {
                // Other sections: Pulse and rotate on scroll into view
                gsap.fromTo(graphic,
                    {
                        scale: 0.8,
                        rotation: 0,
                        opacity: 0.5
                    },
                    {
                        scale: 1,
                        rotation: 360,
                        opacity: 1,
                        duration: 2,
                        ease: 'power2.out',
                        scrollTrigger: {
                            trigger: graphic,
                            start: 'top 80%',
                            end: 'bottom 20%',
                            scrub: 1,
                            toggleActions: 'play none none reverse'
                        }
                    }
                );
            }
        });
    };

    // ==================
    // Section Reveal Animations
    // ==================
    const animateSections = () => {
        const sections = document.querySelectorAll('section, .section');

        sections.forEach((section, index) => {
            // Skip hero section
            if (section.classList.contains('hero') || index === 0) return;

            // Fade and slide up on scroll
            gsap.fromTo(section,
                {
                    y: 60,
                    opacity: 0
                },
                {
                    y: 0,
                    opacity: 1,
                    duration: 0.8,
                    ease: 'power3.out',
                    scrollTrigger: {
                        trigger: section,
                        start: 'top 85%',
                        end: 'top 50%',
                        toggleActions: 'play none none reverse'
                    }
                }
            );
        });
    };

    // ==================
    // Card Stagger Animations
    // ==================
    const animateCards = () => {
        const cardContainers = document.querySelectorAll('.grid, .services-grid, .case-studies-grid');

        cardContainers.forEach(container => {
            const cards = container.querySelectorAll('.card, [class*="card"]');

            if (cards.length > 0) {
                gsap.fromTo(cards,
                    {
                        y: 40,
                        opacity: 0,
                        scale: 0.95
                    },
                    {
                        y: 0,
                        opacity: 1,
                        scale: 1,
                        duration: 0.6,
                        stagger: 0.1,
                        ease: 'back.out(1.2)',
                        scrollTrigger: {
                            trigger: container,
                            start: 'top 80%',
                            toggleActions: 'play none none reverse'
                        }
                    }
                );
            }
        });
    };

    // ==================
    // Headline Split & Reveal
    // ==================
    const animateHeadlines = () => {
        const headlines = document.querySelectorAll('h1, .hero h2, .headline-animated');

        headlines.forEach(headline => {
            // Skip if already animated
            if (headline.dataset.animated) return;

            const text = headline.textContent;
            const words = text.split(' ');

            // Wrap each word in a span
            headline.innerHTML = words.map(word =>
                `<span class="word" style="display: inline-block; opacity: 0;">${word}</span>`
            ).join(' ');

            const wordSpans = headline.querySelectorAll('.word');

            gsap.to(wordSpans, {
                opacity: 1,
                y: 0,
                duration: 0.6,
                stagger: 0.08,
                ease: 'power2.out',
                scrollTrigger: {
                    trigger: headline,
                    start: 'top 90%',
                    toggleActions: 'play none none reverse'
                }
            });

            // Set initial state
            gsap.set(wordSpans, { y: 20, opacity: 0 });

            headline.dataset.animated = 'true';
        });
    };

    // ==================
    // Parallax Background Images
    // ==================
    const parallaxImages = () => {
        const images = document.querySelectorAll('[data-parallax], .parallax-image');

        images.forEach(image => {
            gsap.to(image, {
                y: () => image.offsetHeight * 0.3,
                ease: 'none',
                scrollTrigger: {
                    trigger: image.closest('section, .card, div'),
                    start: 'top bottom',
                    end: 'bottom top',
                    scrub: 1
                }
            });
        });
    };

    // ==================
    // Number Counter Animation
    // ==================
    const animateCounters = () => {
        const counters = document.querySelectorAll('[data-counter], .counter-number');

        counters.forEach(counter => {
            const target = parseInt(counter.dataset.counter || counter.textContent);

            if (!isNaN(target)) {
                gsap.fromTo(counter,
                    { textContent: 0 },
                    {
                        textContent: target,
                        duration: 2,
                        ease: 'power1.out',
                        snap: { textContent: 1 },
                        scrollTrigger: {
                            trigger: counter,
                            start: 'top 80%',
                            toggleActions: 'play none none reverse'
                        },
                        onUpdate: function () {
                            counter.textContent = Math.ceil(this.targets()[0].textContent);
                        }
                    }
                );
            }
        });
    };

    // ==================
    // CTA Button Entrance
    // ==================
    const animateCTAs = () => {
        const ctas = document.querySelectorAll('.btn-primary, .cta-button, [data-cta]');

        ctas.forEach(cta => {
            gsap.fromTo(cta,
                {
                    scale: 0.9,
                    opacity: 0
                },
                {
                    scale: 1,
                    opacity: 1,
                    duration: 0.5,
                    ease: 'back.out(1.5)',
                    scrollTrigger: {
                        trigger: cta,
                        start: 'top 90%',
                        toggleActions: 'play none none reverse'
                    }
                }
            );
        });
    };

    // ==================
    // Hero Scroll Indicator
    // ==================
    const animateScrollIndicator = () => {
        const indicator = document.querySelector('.scroll-indicator, [data-scroll-indicator]');

        if (indicator) {
            // Pulse animation
            gsap.to(indicator, {
                y: 10,
                opacity: 0.6,
                duration: 1,
                repeat: -1,
                yoyo: true,
                ease: 'power1.inOut'
            });

            // Hide on scroll
            ScrollTrigger.create({
                start: 'top top',
                end: '100 top',
                onUpdate: (self) => {
                    gsap.to(indicator, {
                        opacity: 1 - self.progress,
                        duration: 0.3
                    });
                }
            });
        }
    };

    // ==================
    // Smooth Scroll for Anchor Links
    // ==================
    const initSmoothScroll = () => {
        const links = document.querySelectorAll('a[href^="#"]');

        links.forEach(link => {
            link.addEventListener('click', (e) => {
                const targetId = link.getAttribute('href');
                if (targetId === '#') return;

                const target = document.querySelector(targetId);
                if (target) {
                    e.preventDefault();
                    gsap.to(window, {
                        scrollTo: {
                            y: target,
                            offsetY: 80 // Account for sticky nav
                        },
                        duration: 1,
                        ease: 'power2.inOut'
                    });
                }
            });
        });
    };

    // ==================
    // Initialize All Animations
    // ==================
    const init = () => {
        // Check for reduced motion preference
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (prefersReducedMotion) {
            console.log('Reduced motion preferred. Disabling scroll animations.');
            return;
        }

        // Initialize animations
        createScrollProgress();
        animateRotatingGraphics();
        animateSections();
        animateCards();
        animateHeadlines();
        parallaxImages();
        animateCounters();
        animateCTAs();
        animateScrollIndicator();
        initSmoothScroll();

        // Refresh ScrollTrigger after all animations are set
        ScrollTrigger.refresh();
    };

    // Run initialization
    init();

    // Refresh on window resize (debounced)
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            ScrollTrigger.refresh();
        }, 250);
    });
});

// ==================
// Export for manual refresh if needed
// ==================
window.refreshScrollAnimations = () => {
    if (typeof ScrollTrigger !== 'undefined') {
        ScrollTrigger.refresh();
    }
};
