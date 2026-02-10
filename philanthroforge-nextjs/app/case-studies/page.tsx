import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import Link from 'next/link';
import { getAllCaseStudies } from '@/lib/tina';

export default async function CaseStudiesPage() {
    const caseStudies = await getAllCaseStudies();

    return (
        <>
            <Navbar />
            <main className="min-h-screen bg-white">
                {/* Hero Section */}
                <section className="bg-gradient-to-br from-navy to-blue-900 text-white py-20">
                    <div className="max-w-6xl mx-auto px-6 text-center">
                        <h1 className="text-5xl font-bold mb-6">Case Studies</h1>
                        <p className="text-xl opacity-90 max-w-3xl mx-auto">
                            Real results from our partnerships with non-profits.
                        </p>
                    </div>
                </section>

                {/* Case Studies Grid */}
                <section className="py-20">
                    <div className="max-w-6xl mx-auto px-6">
                        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                            {caseStudies.map((study) => (
                                <Link
                                    key={study.slug}
                                    href={`/case-studies/${study.slug}`}
                                    className="block bg-white border border-gray-200 rounded-lg overflow-hidden hover:shadow-xl transition-shadow"
                                >
                                    <div className="p-8">
                                        <p className="text-accent font-bold mb-2 uppercase text-sm tracking-wider">
                                            CASE STUDY
                                        </p>
                                        <h3 className="text-2xl font-bold text-navy mb-4">
                                            {study.title}
                                        </h3>
                                        {study.excerpt && (
                                            <p className="text-gray-600 mb-6 line-clamp-3">
                                                {study.excerpt}
                                            </p>
                                        )}
                                        <span className="text-accent font-bold hover:underline">
                                            Read Full Case Study →
                                        </span>
                                    </div>
                                </Link>
                            ))}
                        </div>
                    </div>
                </section>

                {/* CTA Section */}
                <section className="bg-gray-50 py-16">
                    <div className="max-w-4xl mx-auto px-6 text-center">
                        <h2 className="text-3xl font-bold text-navy mb-4">Ready to Write Your Success Story?</h2>
                        <p className="text-xl text-gray-600 mb-8">
                            Let's discuss how we can help your organization achieve similar results.
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
