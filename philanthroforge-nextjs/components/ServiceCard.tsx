'use client';

import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';

interface ServiceCardProps {
    title: string;
    description: string;
    href: string;
}

export default function ServiceCard({ title, description, href }: ServiceCardProps) {
    const cardRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const card = cardRef.current;
        if (!card) return;

        const handleMouseEnter = () => {
            gsap.to(card, {
                y: -8,
                boxShadow: '0 20px 40px rgba(0, 0, 0, 0.1)',
                duration: 0.3,
                ease: 'power2.out',
            });
        };

        const handleMouseLeave = () => {
            gsap.to(card, {
                y: 0,
                boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
                duration: 0.3,
                ease: 'power2.out',
            });
        };

        card.addEventListener('mouseenter', handleMouseEnter);
        card.addEventListener('mouseleave', handleMouseLeave);

        return () => {
            card.removeEventListener('mouseenter', handleMouseEnter);
            card.removeEventListener('mouseleave', handleMouseLeave);
        };
    }, []);

    return (
        <div ref={cardRef} className="bg-white p-8 rounded-lg shadow-sm transition-shadow animate-item">
            <h3 className="text-xl font-bold mb-4 text-navy">{title}</h3>
            <p className="text-gray-600 mb-6">{description}</p>
            <a href={href} className="text-accent font-semibold hover:underline">
                Learn More →
            </a>
        </div>
    );
}
