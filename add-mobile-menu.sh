#!/bin/bash
# Script to add mobile menu to remaining pages

# List of files that need mobile menu added
files=(
    "lets-talk.html"
    "privacy-policy.html"
    "terms-and-conditions.html"
)

mobile_menu_html='
        <!-- Mobile Menu Overlay -->
        <div id="mobile-menu-overlay"
            class="fixed inset-0 bg-black/50 z-40 hidden lg:hidden backdrop-blur-sm opacity-0 transition-opacity duration-300">
        </div>

        <!-- Mobile Menu Panel -->
        <div id="mobile-menu-panel"
            class="fixed top-0 right-0 h-full w-[85%] max-w-sm bg-primary z-50 transform translate-x-full transition-transform duration-300 shadow-2xl overflow-y-auto lg:hidden">
            <div class="p-6">
                <div class="flex justify-between items-center mb-8">
                    <img src="assets/Folder/Philanthro%20logo.png" alt="Logo" class="h-8 w-auto">
                    <button id="close-mobile-menu" class="text-white hover:text-accent transition-colors focus:outline-none focus:ring-2 focus:ring-accent rounded" aria-label="Close menu">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <nav class="space-y-6" aria-label="Mobile navigation">
                    <a href="index.html"
                        class="block text-lg font-medium text-white hover:text-accent transition-colors border-b border-white/10 pb-3">Home</a>
                    <a href="about.html"
                        class="block text-lg font-medium text-white hover:text-accent transition-colors border-b border-white/10 pb-3">About</a>

                    <!-- Mobile Services -->
                    <div class="border-b border-white/10 pb-3">
                        <button
                            class="flex items-center justify-between w-full text-lg font-medium text-white hover:text-accent transition-colors focus:outline-none"
                            data-dropdown-toggle="mobile-services-dropdown"
                            aria-expanded="false"
                            aria-controls="mobile-services-dropdown">
                            Services
                            <svg data-dropdown-arrow class="w-4 h-4 transition-transform duration-300" fill="none"
                                stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                            </svg>
                        </button>
                        <div id="mobile-services-dropdown" class="hidden mt-4 pl-4 space-y-3">
                            <a href="services/digital-fundraising-strategy.html"
                                class="block text-sm text-gray-300 hover:text-white transition-colors">Digital Fundraising Strategy</a>
                            <a href="services/consultancy-advisory.html"
                                class="block text-sm text-gray-300 hover:text-white transition-colors">Consultancy & Advisory</a>
                            <a href="services/website-donation-optimization.html"
                                class="block text-sm text-gray-300 hover:text-white transition-colors">Website & Donation Optimization</a>
                            <a href="services/donation-form-optimization.html"
                                class="block text-sm text-gray-300 hover:text-white transition-colors">Donation Form Optimization</a>
                            <a href="services/fundraising-campaign-journey-design.html"
                                class="block text-sm text-gray-300 hover:text-white transition-colors">Campaign Design</a>
                            <a href="services/donor-behaviour-analysis-revenue-growth.html"
                                class="block text-sm text-gray-300 hover:text-white transition-colors">Donor Behaviour Analysis</a>
                            <a href="services/csr-major-donor-support.html"
                                class="block text-sm text-gray-300 hover:text-white transition-colors">CSR & Major Donor Support</a>
                            <a href="services/brand-identity-impact-communication.html"
                                class="block text-sm text-gray-300 hover:text-white transition-colors">Brand Identity</a>
                        </div>
                    </div>

                    <!-- Mobile Case Studies -->
                    <div class="border-b border-white/10 pb-3">
                        <button
                            class="flex items-center justify-between w-full text-lg font-medium text-white hover:text-accent transition-colors focus:outline-none"
                            data-dropdown-toggle="mobile-casestudies-dropdown"
                            aria-expanded="false"
                            aria-controls="mobile-casestudies-dropdown">
                            Case Studies
                            <svg data-dropdown-arrow class="w-4 h-4 transition-transform duration-300" fill="none"
                                stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                            </svg>
                        </button>
                        <div id="mobile-casestudies-dropdown" class="hidden mt-4 pl-4 space-y-3">
                            <a href="case-studies/rewarding-generosity.html"
                                class="block text-sm text-gray-300 hover:text-white transition-colors">Rewarding Generosity</a>
                            <a href="case-studies/turning-supporters-into-fundraisers.html"
                                class="block text-sm text-gray-300 hover:text-white transition-colors">Turning Supporters Into Champions</a>
                            <a href="case-studies/integrated-ecosystems.html"
                                class="block text-sm text-gray-300 hover:text-white transition-colors">Integrated Ecosystems</a>
                        </div>
                    </div>

                    <a href="lets-talk.html"
                        class="block w-full text-center bg-accent text-primary font-bold uppercase py-3 px-6 rounded-md hover:bg-white transition-all shadow-md">Let'"'"'s Talk</a>
                </nav>
            </div>
        </div>
    </nav>'

echo "Mobile menu HTML template ready"
echo "Files to update: ${files[@]}"
