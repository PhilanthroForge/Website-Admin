import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { getAllCaseStudies, getCaseStudyBySlug } from '@/lib/tina';
import { TinaMarkdown } from 'tinacms/dist/rich-text';
import { notFound } from 'next/navigation';

export async function generateStaticParams() {
    const caseStudies = await getAllCaseStudies();
    return caseStudies.map((study) => ({
        slug: study.slug,
    }));
}

export default async function CaseStudyPage({
    params,
}: {
    params: Promise<{ slug: string }>;
}) {
    const { slug } = await params;
    const caseStudyData = await getCaseStudyBySlug(slug);

    if (!caseStudyData || !caseStudyData.caseStudy) {
        notFound();
    }

    const caseStudy = caseStudyData.caseStudy;

    return (
        <>
            <Navbar />
            <main className="min-h-screen bg-white">
                {/* Hero Section */}
                <section className="bg-gradient-to-br from-navy to-blue-900 text-white py-20">
                    <div className="max-w-6xl mx-auto px-6">
                        <p className="text-accent font-bold mb-4 uppercase tracking-wider">Case Study</p>
                        <h1 className="text-5xl font-bold mb-6">{caseStudy.title}</h1>
                        {caseStudy.excerpt && (
                            <p className="text-xl opacity-90 max-w-3xl">{caseStudy.excerpt}</p>
                        )}
                    </div>
                </section>

                {/* Content Section */}
                <section className="py-20">
                    <div className="max-w-4xl mx-auto px-6 prose prose-lg max-w-none prose-headings:text-navy prose-a:text-accent prose-strong:text-navy">
                        {caseStudy.body && <TinaMarkdown content={caseStudy.body} />}
                    </div>
                </section>

                {/* CTA Section */}
                <section className="bg-gray-50 py-16">
                    <div className="max-w-4xl mx-auto px-6 text-center">
                        <h2 className="text-3xl font-bold text-navy mb-4">Want Similar Results?</h2>
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
