'use client';

import { useRef, useEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

// Register plugin
if (typeof window !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
}

interface UseScrollAnimationOptions {
    trigger?: string;
    start?: string;
    end?: string;
    scrub?: boolean;
    markers?: boolean;
}

/**
 * Custom hook for scroll-triggered animations
 */
export function useScrollAnimation(
    animationFn: (element: HTMLElement) => gsap.core.Timeline | gsap.core.Tween,
    options?: UseScrollAnimationOptions
) {
    const elementRef = useRef<HTMLElement>(null);

    useEffect(() => {
        const element = elementRef.current;
        if (!element) return;

        const animation = animationFn(element);

        const scrollTrigger = ScrollTrigger.create({
            trigger: options?.trigger || element,
            start: options?.start || 'top 80%',
            end: options?.end || 'bottom 20%',
            scrub: options?.scrub || false,
            markers: options?.markers || false,
            animation,
            toggleActions: 'play none none none',
        });

        return () => {
            scrollTrigger.kill();
            if (animation instanceof gsap.core.Timeline || animation instanceof gsap.core.Tween) {
                animation.kill();
            }
        };
    }, [animationFn, options]);

    return elementRef;
}

/**
 * Hook for fade in up animation on scroll
 */
export function useFadeInUp(delay: number = 0) {
    return useScrollAnimation((element) => {
        return gsap.fromTo(
            element,
            { opacity: 0, y: 50 },
            {
                opacity: 1,
                y: 0,
                duration: 0.8,
                delay,
                ease: 'power3.out',
            }
        );
    });
}

/**
 * Hook for stagger animation
 */
export function useStaggerAnimation(childSelector: string = '.animate-item', stagger: number = 0.1) {
    const containerRef = useRef<HTMLElement>(null);

    useEffect(() => {
        const container = containerRef.current;
        if (!container) return;

        const children = container.querySelectorAll(childSelector);

        const animation = gsap.fromTo(
            children,
            { opacity: 0, y: 50 },
            {
                opacity: 1,
                y: 0,
                duration: 0.6,
                stagger,
                ease: 'power3.out',
            }
        );

        const scrollTrigger = ScrollTrigger.create({
            trigger: container,
            start: 'top 80%',
            toggleActions: 'play none none none',
            animation,
        });

        return () => {
            scrollTrigger.kill();
            animation.kill();
        };
    }, [childSelector, stagger]);

    return containerRef;
}

/**
 * Hook for scale in animation
 */
export function useScaleIn(delay: number = 0) {
    return useScrollAnimation((element) => {
        return gsap.fromTo(
            element,
            { opacity: 0, scale: 0.9 },
            {
                opacity: 1,
                scale: 1,
                duration: 0.8,
                delay,
                ease: 'power2.out',
            }
        );
    });
}

/**
 * Hook for slide animations
 */
export function useSlideIn(direction: 'left' | 'right' = 'left', delay: number = 0) {
    return useScrollAnimation((element) => {
        const xValue = direction === 'left' ? -100 : 100;
        return gsap.fromTo(
            element,
            { opacity: 0, x: xValue },
            {
                opacity: 1,
                x: 0,
                duration: 0.8,
                delay,
                ease: 'power3.out',
            }
        );
    });
}
