"use client";

import Link from "next/link";
import { useState } from "react";

export default function Navbar() {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [servicesDropdownOpen, setServicesDropdownOpen] = useState(false);
    return (
        <nav className="bg-white border-b border-gray-200">
            <div className="container mx-auto px-4">
                <div className="flex items-center justify-between h-20">
                    {/* Logo */}
                    <div className="flex items-center">
                        <a href="/" className="flex items-center space-x-2">
                            <div className="w-10 h-10 bg-accent rounded-full flex items-center justify-center">
                                <span className="text-primary font-bold text-xl">PF</span>
                            </div>
                            <span className="text-xl font-bold text-navy">PhilanthroForge</span>
                        </a>
                    </div>

                    {/* Desktop Navigation */}
                    <div className="hidden lg:flex items-center space-x-8">
                        <a href="/" className="text-gray-700 hover:text-navy transition-colors">Home</a>
                        <a href="/about" className="text-gray-700 hover:text-navy transition-colors">About</a>

                        {/* Services Dropdown */}
                        <div className="relative group">
                            <button className="text-gray-700 hover:text-navy transition-colors flex items-center">
                                Services
                                <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                </svg>
                            </button>
                            <div className="absolute left-0 mt-2 w-64 bg-white rounded-md shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                                <div className="py-2">
                                    <a href="/services/digital-fundraising-strategy" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Digital Fundraising Strategy</a>
                                    <a href="/services/consultancy-advisory" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Consultancy & Advisory</a>
                                    <a href="/services/donation-form-optimization" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Donation Form Optimization</a>
                                </div>
                            </div>
                        </div>

                        <a href="/case-studies" className="text-gray-700 hover:text-navy transition-colors">Case Studies</a>
                        <a
                            href="/lets-talk"
                            className="bg-accent text-primary font-bold uppercase py-2 px-6 rounded-sm hover:opacity-90 transition-opacity"
                        >
                            Let&#39;s Talk
                        </a>
                    </div>

                    {/* Mobile menu button */}
                    <div className="lg:hidden">
                        <button
                            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                            className="p-2 hover:bg-gray-100 rounded transition-colors"
                            aria-label="Toggle mobile menu"
                        >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                {mobileMenuOpen ? (
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                ) : (
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                                )}
                            </svg>
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            {mobileMenuOpen && (
                <div className="lg:hidden border-t border-gray-200">
                    <div className="container mx-auto px-4 py-4 space-y-2">
                        <Link
                            href="/"
                            className="block py-2 hover:text-accent transition-colors"
                            onClick={() => setMobileMenuOpen(false)}
                        >
                            Home
                        </Link>
                        <Link
                            href="/about"
                            className="block py-2 hover:text-accent transition-colors"
                            onClick={() => setMobileMenuOpen(false)}
                        >
                            About
                        </Link>

                        {/* Mobile Services Dropdown */}
                        <div>
                            <button
                                onClick={() => setServicesDropdownOpen(!servicesDropdownOpen)}
                                className="w-full text-left py-2 flex justify-between items-center hover:text-accent transition-colors"
                            >
                                Services
                                <svg
                                    className={`w-4 h-4 transition-transform ${servicesDropdownOpen ? 'rotate-180' : ''}`}
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                </svg>
                            </button>
                            {servicesDropdownOpen && (
                                <div className="pl-4 space-y-2 mt-2">
                                    <Link
                                        href="/services/digital-fundraising-strategy"
                                        className="block py-2 text-sm hover:text-accent transition-colors"
                                        onClick={() => setMobileMenuOpen(false)}
                                    >
                                        Digital Fundraising Strategy
                                    </Link>
                                    <Link
                                        href="/services/consultancy-advisory"
                                        className="block py-2 text-sm hover:text-accent transition-colors"
                                        onClick={() => setMobileMenuOpen(false)}
                                    >
                                        Consultancy & Advisory
                                    </Link>
                                    <Link
                                        href="/services/donation-form-optimization"
                                        className="block py-2 text-sm hover:text-accent transition-colors"
                                        onClick={() => setMobileMenuOpen(false)}
                                    >
                                        Donation Form Optimization
                                    </Link>
                                </div>
                            )}
                        </div>

                        <Link
                            href="/case-studies"
                            className="block py-2 hover:text-accent transition-colors"
                            onClick={() => setMobileMenuOpen(false)}
                        >
                            Case Studies
                        </Link>

                        <Link
                            href="/lets-talk"
                            className="block mt-4 bg-accent text-primary font-bold uppercase py-3 px-6 rounded-sm text-center hover:opacity-90 transition-opacity"
                            onClick={() => setMobileMenuOpen(false)}
                        >
                            Let's Talk
                        </Link>
                    </div>
                </div>
            )}
        </nav>
    );
}
