import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

// Register GSAP plugins
if (typeof window !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
}

/**
 * Fade in and slide up animation
 */
export const fadeInUp = (element: HTMLElement | null, delay: number = 0) => {
    if (!element) return null;

    return gsap.fromTo(
        element,
        {
            opacity: 0,
            y: 50,
        },
        {
            opacity: 1,
            y: 0,
            duration: 0.8,
            delay,
            ease: 'power3.out',
        }
    );
};

/**
 * Stagger animation for multiple elements (like cards or list items)
 */
export const staggerAnimation = (
    container: HTMLElement | null,
    childSelector: string = '.animate-item'
) => {
    if (!container) return null;

    const children = container.querySelectorAll(childSelector);

    return gsap.fromTo(
        children,
        {
            opacity: 0,
            y: 50,
        },
        {
            opacity: 1,
            y: 0,
            duration: 0.6,
            stagger: 0.1,
            ease: 'power3.out',
            scrollTrigger: {
                trigger: container,
                start: 'top 80%',
                toggleActions: 'play none none none',
            },
        }
    );
};

/**
 * Scale in animation
 */
export const scaleIn = (element: HTMLElement | null, delay: number = 0) => {
    if (!element) return null;

    return gsap.fromTo(
        element,
        {
            opacity: 0,
            scale: 0.9,
        },
        {
            opacity: 1,
            scale: 1,
            duration: 0.8,
            delay,
            ease: 'power2.out',
        }
    );
};

/**
 * Slide in from left
 */
export const slideInLeft = (element: HTMLElement | null, delay: number = 0) => {
    if (!element) return null;

    return gsap.fromTo(
        element,
        {
            opacity: 0,
            x: -100,
        },
        {
            opacity: 1,
            x: 0,
            duration: 0.8,
            delay,
            ease: 'power3.out',
        }
    );
};

/**
 * Slide in from right
 */
export const slideInRight = (element: HTMLElement | null, delay: number = 0) => {
    if (!element) return null;

    return gsap.fromTo(
        element,
        {
            opacity: 0,
            x: 100,
        },
        {
            opacity: 1,
            x: 0,
            duration: 0.8,
            delay,
            ease: 'power3.out',
        }
    );
};

/**
 * Create scroll-triggered fade in animation
 */
export const scrollFadeIn = (
    element: HTMLElement | null,
    options?: ScrollTrigger.Vars
) => {
    if (!element) return null;

    return gsap.fromTo(
        element,
        {
            opacity: 0,
            y: 50,
        },
        {
            opacity: 1,
            y: 0,
            duration: 1,
            ease: 'power3.out',
            scrollTrigger: {
                trigger: element,
                start: 'top 85%',
                end: 'bottom 20%',
                toggleActions: 'play none none none',
                ...options,
            },
        }
    );
};

/**
 * Button hover animation
 */
export const buttonHover = (button: HTMLElement) => {
    const tl = gsap.timeline({ paused: true });

    tl.to(button, {
        scale: 1.05,
        duration: 0.2,
        ease: 'power2.out',
    });

    return {
        play: () => tl.play(),
        reverse: () => tl.reverse(),
    };
};

/**
 * Card hover animation
 */
export const cardHover = (card: HTMLElement) => {
    const tl = gsap.timeline({ paused: true });

    tl.to(card, {
        y: -8,
        boxShadow: '0 20px 40px rgba(0, 0, 0, 0.15)',
        duration: 0.3,
        ease: 'power2.out',
    });

    return {
        play: () => tl.play(),
        reverse: () => tl.reverse(),
    };
};

/**
 * Cleanup all ScrollTrigger instances
 */
export const cleanupScrollTriggers = () => {
    ScrollTrigger.getAll().forEach((trigger) => trigger.kill());
};

/**
 * Refresh ScrollTrigger (useful after dynamic content loads)
 */
export const refreshScrollTrigger = () => {
    ScrollTrigger.refresh();
};
