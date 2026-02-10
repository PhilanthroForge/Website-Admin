#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Configuration
const SOURCE_DIR = '..';
const CONTENT_DIRS = {
    services: 'content/services',
    'case-studies': 'content/case-studies',
    pages: 'content/pages'
};

// Helper function to clean text content
function cleanText(text) {
    if (!text) return '';
    return text
        .replace(/\\n\\n/g, '\n\n')
        .replace(/\\u2019/g, "'")
        .replace(/\\u2013/g, '–')
        .replace(/\\u2014/g, '—')
        .replace(/\\u2011/g, '-')
        .trim();
}

// Convert JSON to MDX
function convertJsonToMdx(jsonPath) {
    const fileName = path.basename(jsonPath, '.json');
    const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
    const { metadata, content_blocks } = data;

    console.log(`Converting: ${fileName}`);

    // Determine output directory and file name
    let outputDir, outputFileName;

    if (fileName.startsWith('services_')) {
        outputDir = CONTENT_DIRS.services;
        outputFileName = fileName.replace('services_', '') + '.mdx';
    } else if (fileName.startsWith('case-studies_')) {
        outputDir = CONTENT_DIRS['case-studies'];
        outputFileName = fileName.replace('case-studies_', '') + '.mdx';
    } else if (fileName === 'index') {
        outputDir = CONTENT_DIRS.pages;
        outputFileName = 'home.mdx';
    } else {
        outputDir = CONTENT_DIRS.pages;
        outputFileName = fileName + '.mdx';
    }

    // Create MDX frontmatter
    let mdx = `---
title: "${metadata.title || fileName}"
slug: "${metadata.slug || fileName}"
description: ""
---

`;

    // Convert content blocks to MDX
    content_blocks.forEach((block, index) => {
        // Skip intro blocks with navigation noise
        if (block.type === 'intro' && block.text && block.text.includes('HomeAboutServices')) {
            // Only add images from intro
            if (block.images && block.images.length > 0) {
                block.images.forEach(img => {
                    const imgPath = img.src.replace('assets/', '/images/');
                    if (img.alt) {
                        mdx += `![${img.alt}](${imgPath})\n\n`;
                    }
                });
            }
            return;
        }

        // Add heading
        if (block.heading && block.heading.trim()) {
            const headingText = cleanText(block.heading);

            // Determine heading level from tag
            let headingLevel = '##';
            if (block.tag === 'h1') headingLevel = '#';
            else if (block.tag === 'h2') headingLevel = '##';
            else if (block.tag === 'h3') headingLevel = '###';

            mdx += `${headingLevel} ${headingText}\n\n`;
        }

        // Add text content
        if (block.text && block.text.trim()) {
            const cleanedText = cleanText(block.text);

            // Split into bullet points if the text has clear list structure
            const lines = cleanedText.split('\n\n');
            lines.forEach(line => {
                if (line.trim()) {
                    mdx += `${line}\n\n`;
                }
            });
        }

        // Add images
        if (block.images && block.images.length > 0) {
            block.images.forEach(img => {
                const imgPath = img.src.replace('assets/', '/images/');
                const altText = img.alt || '';
                mdx += `![${altText}](${imgPath})\n\n`;
            });
        }
    });

    // Write MDX file
    const outputPath = path.join(outputDir, outputFileName);
    fs.writeFileSync(outputPath, mdx);
    console.log(`  ✓ Created: ${outputPath}`);

    return outputFileName;
}

// Main execution
console.log('Starting JSON to MDX conversion...\n');

// Get all JSON files from parent directory
const jsonFiles = fs.readdirSync(SOURCE_DIR)
    .filter(f => f.endsWith('.json') && !f.includes('package'));

console.log(`Found ${jsonFiles.length} JSON files to convert\n`);

// Convert each file
const converted = [];
jsonFiles.forEach(file => {
    try {
        const outputFile = convertJsonToMdx(path.join(SOURCE_DIR, file));
        converted.push(outputFile);
    } catch (error) {
        console.error(`  ✗ Error converting ${file}:`, error.message);
    }
});

console.log(`\n✓ Conversion complete! Converted ${converted.length} files.`);
console.log('\nNext steps:');
console.log('1. Review the generated MDX files in content/ directories');
console.log('2. Update TinaCMS schema in tina/config.ts');
console.log('3. Update page components to fetch from TinaCMS');
