import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { getAllServices, getServiceBySlug } from '@/lib/tina';
import { TinaMarkdown } from 'tinacms/dist/rich-text';
import { notFound } from 'next/navigation';

export async function generateStaticParams() {
    const services = await getAllServices();
    return services.map((service) => ({
        slug: service.slug,
    }));
}

export default async function ServicePage({
    params,
}: {
    params: Promise<{ slug: string }>;
}) {
    const { slug } = await params;
    const serviceData = await getServiceBySlug(slug);

    if (!serviceData || !serviceData.service) {
        notFound();
    }

    const service = serviceData.service;

    return (
        <>
            <Navbar />
            <main className="min-h-screen bg-white">
                {/* Hero Section */}
                <section className="bg-gradient-to-br from-navy to-blue-900 text-white py-20">
                    <div className="max-w-6xl mx-auto px-6">
                        <h1 className="text-5xl font-bold mb-6">{service.title}</h1>
                        {service.description && (
                            <p className="text-xl opacity-90 max-w-3xl">{service.description}</p>
                        )}
                    </div>
                </section>

                {/* Content Section */}
                <section className="py-20">
                    <div className="max-w-4xl mx-auto px-6 prose prose-lg max-w-none prose-headings:text-navy prose-a:text-accent prose-strong:text-navy">
                        {service.body && <TinaMarkdown content={service.body} />}
                    </div>
                </section>

                {/* CTA Section */}
                <section className="bg-gray-50 py-16">
                    <div className="max-w-4xl mx-auto px-6 text-center">
                        <h2 className="text-3xl font-bold text-navy mb-4">Ready to Transform Your Fundraising?</h2>
                        <p className="text-xl text-gray-600 mb-8">
                            Let's discuss how we can help your organization achieve its goals.
                        </p>
                        <a
                            href="/lets-talk"
                            className="inline-block bg-accent text-navy px-10 py-4 rounded-md font-bold hover:bg-yellow-400 transition-colors"
                        >
                            LET'S TALK
                        </a>
                    </div>
                </section>
            </main>
            <Footer />
        </>
    );
}
