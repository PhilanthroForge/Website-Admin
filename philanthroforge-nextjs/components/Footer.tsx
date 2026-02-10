export default function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="bg-navy text-white py-12">
            <div className="container mx-auto px-4">
                <div className="grid md:grid-cols-4 gap-8">
                    {/* Company Info */}
                    <div>
                        <div className="flex items-center space-x-2 mb-4">
                            <div className="w-8 h-8 bg-accent rounded-full flex items-center justify-center">
                                <span className="text-primary font-bold">PF</span>
                            </div>
                            <span className="font-bold text-lg">PhilanthroForge</span>
                        </div>
                        <p className="text-gray-300 text-sm">
                            Forging the next era of non-profit fundraising.
                        </p>
                    </div>

                    {/* Services */}
                    <div>
                        <h3 className="font-bold mb-4">Services</h3>
                        <ul className="space-y-2 text-sm">
                            <li><a href="/services/digital-fundraising-strategy" className="text-gray-300 hover:text-accent transition-colors">Digital Fundraising</a></li>
                            <li><a href="/services/consultancy-advisory" className="text-gray-300 hover:text-accent transition-colors">Consultancy</a></li>
                            <li><a href="/services/donation-form-optimization" className="text-gray-300 hover:text-accent transition-colors">Form Optimization</a></li>
                        </ul>
                    </div>

                    {/* Company */}
                    <div>
                        <h3 className="font-bold mb-4">Company</h3>
                        <ul className="space-y-2 text-sm">
                            <li><a href="/about" className="text-gray-300 hover:text-accent transition-colors">About Us</a></li>
                            <li><a href="/case-studies" className="text-gray-300 hover:text-accent transition-colors">Case Studies</a></li>
                            <li><a href="/lets-talk" className="text-gray-300 hover:text-accent transition-colors">Contact</a></li>
                        </ul>
                    </div>

                    {/* Legal */}
                    <div>
                        <h3 className="font-bold mb-4">Legal</h3>
                        <ul className="space-y-2 text-sm">
                            <li><a href="/privacy-policy" className="text-gray-300 hover:text-accent transition-colors">Privacy Policy</a></li>
                            <li><a href="/terms-and-conditions" className="text-gray-300 hover:text-accent transition-colors">Terms & Conditions</a></li>
                        </ul>
                    </div>
                </div>

                {/* Copyright */}
                <div className="mt-8 pt-8 border-t border-gray-700 text-center text-sm text-gray-400">
                    <p>&copy; {currentYear} PhilanthroForge. All rights reserved.</p>
                </div>
            </div>
        </footer>
    );
}
