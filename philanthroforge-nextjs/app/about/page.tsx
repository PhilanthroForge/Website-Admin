import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function AboutPage() {
    return (
        <>
            <Navbar />
            <main className="min-h-screen bg-white">
                {/* Hero Section */}
                <section className="py-20 bg-navy text-white">
                    <div className="container mx-auto px-4 max-w-4xl text-center">
                        <h1 className="text-4xl md:text-5xl font-bold mb-6">About PhilanthroForge</h1>
                        <p className="text-xl text-gray-300">
                            Transforming non-profit fundraising through donor-centric digital strategies.
                        </p>
                    </div>
                </section>

                {/* Mission Section */}
                <section className="py-20">
                    <div className="container mx-auto px-4 max-w-4xl">
                        <h2 className="text-3xl font-bold mb-6">Our Mission</h2>
                        <p className="text-lg text-gray-700 mb-6 leading-relaxed">
                            We believe that every non-profit deserves access to world-class fundraising strategies and technology.
                            Our mission is to <strong>forge the next era of non-profit fundraising</strong> by helping organizations
                            build donor-centric digital systems that scale.
                        </p>

                        <h3 className="text-2xl font-bold mb-4 mt-12">What We Do</h3>
                        <p className="text-lg text-gray-700 mb-6 leading-relaxed">
                            PhilanthroForge partners with non-profits to optimize their digital fundraising ecosystem. From strategic
                            planning to technical implementation, we provide end-to-end solutions that drive sustainable revenue growth.
                        </p>

                        <div className="grid md:grid-cols-2 gap-8 mt-10">
                            <div className="bg-gray-50 p-6 rounded-lg">
                                <h4 className="font-bold text-lg mb-2">Donor-Centric Design</h4>
                                <p className="text-gray-700">We put donor experience at the heart of every strategy</p>
                            </div>
                            <div className="bg-gray-50 p-6 rounded-lg">
                                <h4 className="font-bold text-lg mb-2">Data-Driven Decisions</h4>
                                <p className="text-gray-700">Leveraging analytics to optimize performance</p>
                            </div>
                            <div className="bg-gray-50 p-6 rounded-lg">
                                <h4 className="font-bold text-lg mb-2">Sustainable Growth</h4>
                                <p className="text-gray-700">Building systems that scale with your organization</p>
                            </div>
                            <div className="bg-gray-50 p-6 rounded-lg">
                                <h4 className="font-bold text-lg mb-2">Continuous Innovation</h4>
                                <p className="text-gray-700">Staying ahead of industry trends and best practices</p>
                            </div>
                        </div>
                    </div>
                </section>

                {/* CTA Section */}
                <section className="py-20 bg-gray-50">
                    <div className="container mx-auto px-4 text-center">
                        <h3 className="text-3xl font-bold mb-6">Ready to Transform Your Fundraising?</h3>
                        <p className="text-lg text-gray-700 mb-8 max-w-2xl mx-auto">
                            Let's discuss how we can help your organization thrive.
                        </p>
                        <a
                            href="/lets-talk"
                            className="inline-block bg-accent text-primary font-bold uppercase py-4 px-10 rounded-sm hover:opacity-90 transition-opacity"
                        >
                            Get in Touch
                        </a>
                    </div>
                </section>
            </main>
            <Footer />
        </>
    );
}
