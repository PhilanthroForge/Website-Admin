import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import AnimatedSection from "@/components/AnimatedSection";
import ServiceCard from "@/components/ServiceCard";

export default function Home() {
  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-white">
        {/* Hero Section */}
        <AnimatedSection animation="scaleIn" className="py-24 text-center relative overflow-hidden">
          <div className="container mx-auto px-4 relative z-10 max-w-4xl">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-neutral-dark mb-8 leading-tight">
              Forging the <span className="text-navy">Next Era</span> of Non-Profit Fundraising.
            </h1>
            <p className="text-lg md:text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              We help non-profits build donor-centric digital fundraising systems that scale.
            </p>
            <a
              href="/lets-talk"
              className="inline-block bg-accent text-primary font-bold uppercase py-4 px-10 rounded-sm hover:opacity-90 transition-opacity"
            >
              Let&#39;s Talk
            </a>
          </div>
        </AnimatedSection>

        {/* Services Section */}
        <section className="py-20 bg-gray-50">
          <div className="container mx-auto px-4">
            <AnimatedSection animation="fadeInUp" className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">Our Services</h2>
              <p className="text-gray-600 max-w-2xl mx-auto">
                Expert guidance to transform your fundraising strategy and maximize impact.
              </p>
            </AnimatedSection>

            <AnimatedSection animation="stagger">
              <div className="grid md:grid-cols-3 gap-8">
                <ServiceCard
                  title="Digital Fundraising Strategy"
                  description="Strategic planning and execution for modern digital fundraising campaigns."
                  href="/services/digital-fundraising-strategy"
                />
                <ServiceCard
                  title="Consultancy & Advisory"
                  description="Expert guidance on fundraising optimization and donor engagement."
                  href="/services/consultancy-advisory"
                />
                <ServiceCard
                  title="Donation Form Optimization"
                  description="Increase conversion rates with optimized donation forms and user experiences."
                  href="/services/donation-form-optimization"
                />
              </div>
            </AnimatedSection>
          </div>
        </section>

        {/* Case Study CTA */}
        <section className="py-20">
          <div className="container mx-auto px-4">
            <AnimatedSection animation="fadeInUp">
              <div className="bg-navy text-white p-12 rounded-lg">
                <h4 className="text-accent font-bold uppercase tracking-wider mb-2">Case Study</h4>
                <h2 className="text-3xl md:text-4xl font-bold mb-6">Rewarding Generosity</h2>
                <p className="text-gray-300 text-lg mb-8 max-w-2xl">
                  Discover how we helped a leading non-profit unlock new giving potential by restructuring their donor recognition program.
                </p>
                <a
                  href="/case-studies/rewarding-generosity"
                  className="inline-block bg-accent text-primary font-bold uppercase py-3 px-8 rounded-sm hover:opacity-90 transition-opacity"
                >
                  Read Case Study
                </a>
              </div>
            </AnimatedSection>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
