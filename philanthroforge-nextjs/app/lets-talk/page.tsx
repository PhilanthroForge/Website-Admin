import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function LetsTalkPage() {
    return (
        <>
            <Navbar />
            <main className="min-h-screen bg-white">
                {/* Hero */}
                <section className="py-20 bg-navy text-white">
                    <div className="container mx-auto px-4 max-w-4xl text-center">
                        <h1 className="text-4xl md:text-5xl font-bold mb-6">Let's Talk</h1>
                        <p className="text-xl text-gray-300">
                            Ready to transform your fundraising? Get in touch with our team.
                        </p>
                    </div>
                </section>

                {/* Contact Form */}
                <section className="py-20">
                    <div className="container mx-auto px-4 max-w-2xl">
                        <form className="space-y-6">
                            <div className="grid md:grid-cols-2 gap-6">
                                <div>
                                    <label htmlFor="name" className="block text-sm font-bold mb-2">Name *</label>
                                    <input
                                        type="text"
                                        id="name"
                                        name="name"
                                        required
                                        className="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:border-accent"
                                    />
                                </div>
                                <div>
                                    <label htmlFor="email" className="block text-sm font-bold mb-2">Email *</label>
                                    <input
                                        type="email"
                                        id="email"
                                        name="email"
                                        required
                                        className="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:border-accent"
                                    />
                                </div>
                            </div>

                            <div>
                                <label htmlFor="organization" className="block text-sm font-bold mb-2">Organization</label>
                                <input
                                    type="text"
                                    id="organization"
                                    name="organization"
                                    className="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:border-accent"
                                />
                            </div>

                            <div>
                                <label htmlFor="service" className="block text-sm font-bold mb-2">Service of Interest</label>
                                <select
                                    id="service"
                                    name="service"
                                    className="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:border-accent"
                                >
                                    <option value="">Select a service...</option>
                                    <option value="digital-fundraising">Digital Fundraising Strategy</option>
                                    <option value="consultancy">Consultancy & Advisory</option>
                                    <option value="donation-forms">Donation Form Optimization</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>

                            <div>
                                <label htmlFor="message" className="block text-sm font-bold mb-2">Message *</label>
                                <textarea
                                    id="message"
                                    name="message"
                                    rows={6}
                                    required
                                    className="w-full px-4 py-3 border border-gray-300 rounded-sm focus:outline-none focus:border-accent"
                                ></textarea>
                            </div>

                            <button
                                type="submit"
                                className="w-full bg-accent text-primary font-bold uppercase py-4 px-10 rounded-sm hover:opacity-90 transition-opacity"
                            >
                                Send Message
                            </button>
                        </form>

                        <p className="text-sm text-gray-600 mt-6 text-center">
                            We typically respond within 24 hours.
                        </p>
                    </div>
                </section>
            </main>
            <Footer />
        </>
    );
}
