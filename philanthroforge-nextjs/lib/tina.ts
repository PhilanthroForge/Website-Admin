import client from '@/tina/__generated__/client';

export interface Service {
    slug: string;
    title: string;
    excerpt?: string;
    icon?: string;
}

// Fetch all services for listing pages
export async function getAllServices(): Promise<Service[]> {
    try {
        const response = await client.queries.serviceConnection();
        const services = response.data.serviceConnection.edges?.map((edge) => ({
            slug: edge?.node?._sys.filename || '',
            title: edge?.node?.title || '',
            excerpt: edge?.node?.description || '',
            icon: edge?.node?.icon || '',
        })) || [];

        return services;
    } catch (error) {
        console.error('Error fetching services:', error);
        return [];
    }
}

// Fetch a single service by slug
export async function getServiceBySlug(slug: string) {
    try {
        const response = await client.queries.service({
            relativePath: `${slug}.mdx`,
        });

        return response.data;
    } catch (error) {
        console.error(`Error fetching service ${slug}:`, error);
        return null;
    }
}

// Fetch a single page by slug
export async function getPageBySlug(slug: string) {
    try {
        const response = await client.queries.page({
            relativePath: `${slug}.mdx`,
        });

        return response.data;
    } catch (error) {
        console.error(`Error fetching page ${slug}:`, error);
        return null;
    }
}

// Fetch all case studies
export async function getAllCaseStudies() {
    try {
        const response = await client.queries.caseStudyConnection();
        const caseStudies = response.data.caseStudyConnection.edges?.map((edge) => ({
            slug: edge?.node?._sys.filename || '',
            title: edge?.node?.title || '',
            excerpt: edge?.node?.excerpt || '',
            featuredImage: edge?.node?.featuredImage || '',
        })) || [];

        return caseStudies;
    } catch (error) {
        console.error('Error fetching case studies:', error);
        return [];
    }
}

// Fetch a single case study by slug
export async function getCaseStudyBySlug(slug: string) {
    try {
        const response = await client.queries.caseStudy({
            relativePath: `${slug}.mdx`,
        });

        return response.data;
    } catch (error) {
        console.error(`Error fetching case study ${slug}:`, error);
        return null;
    }
}
