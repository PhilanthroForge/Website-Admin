'use client';

import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

if (typeof window !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
}

interface AnimatedSectionProps {
    children: React.ReactNode;
    className?: string;
    animation?: 'fadeInUp' | 'stagger' | 'scaleIn';
    delay?: number;
}

export default function AnimatedSection({
    children,
    className = '',
    animation = 'fadeInUp',
    delay = 0,
}: AnimatedSectionProps) {
    const sectionRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const section = sectionRef.current;
        if (!section) return;

        let tween: gsap.core.Tween | gsap.core.Timeline;

        if (animation === 'fadeInUp') {
            tween = gsap.fromTo(
                section,
                { opacity: 0, y: 50 },
                {
                    opacity: 1,
                    y: 0,
                    duration: 0.8,
                    delay,
                    ease: 'power3.out',
                    scrollTrigger: {
                        trigger: section,
                        start: 'top 80%',
                        toggleActions: 'play none none none',
                    },
                }
            );
        } else if (animation === 'stagger') {
            const children = section.querySelectorAll('.animate-item');
            tween = gsap.fromTo(
                children,
                { opacity: 0, y: 30 },
                {
                    opacity: 1,
                    y: 0,
                    duration: 0.6,
                    stagger: 0.15,
                    ease: 'power3.out',
                    scrollTrigger: {
                        trigger: section,
                        start: 'top 75%',
                        toggleActions: 'play none none none',
                    },
                }
            );
        } else if (animation === 'scaleIn') {
            tween = gsap.fromTo(
                section,
                { opacity: 0, scale: 0.95 },
                {
                    opacity: 1,
                    scale: 1,
                    duration: 0.8,
                    delay,
                    ease: 'power2.out',
                    scrollTrigger: {
                        trigger: section,
                        start: 'top 80%',
                        toggleActions: 'play none none none',
                    },
                }
            );
        }

        return () => {
            if (tween) tween.kill();
        };
    }, [animation, delay]);

    return (
        <div ref={sectionRef} className={className}>
            {children}
        </div>
    );
}
