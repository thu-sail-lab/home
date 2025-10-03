#!/usr/bin/env python3
"""
Publication Processing Script - Updated with LLM Topic
Converts publications.json to HTML format with topic categorization including LLMs
"""

import json
import re
from typing import Dict, List, Set, Tuple

# Topics dictionary for categorization - UPDATED with LLMs
TOPICS = {
    'deep-learning': [
        'deep learning', 'neural network', 'CNN', 'RNN', 'LSTM', 'transformer',
        'attention', 'GNN', 'graph neural', 'convolution', 'deep', 'learning model'
    ],
    'machine-learning': [
        'machine learning', 'classification', 'clustering', 'regression',
        'supervised', 'unsupervised', 'ensemble', 'random forest', 'SVM'
    ],
    'reinforcement-learning': [
        'reinforcement learning', 'Q-learning', 'policy', 'reward', 'agent',
        'multi-armed bandit', 'thompson sampling', 'DRL', 'deep reinforcement'
    ],
    'time-series': [
        'time series', 'temporal', 'forecasting', 'prediction', 'sequential',
        'ARIMA', 'spatiotemporal', 'passenger flow', 'traffic'
    ],
    'anomaly-detection': [
        'anomaly detection', 'change detection', 'outlier', 'monitoring',
        'fault detection', 'defect', 'quality control'
    ],
    'causal-inference': [
        'causal', 'causality', 'DAG', 'directed acyclic', 'causal discovery',
        'causal graph', 'intervention'
    ],
    'bayesian-methods': [
        'bayesian', 'prior', 'posterior', 'MCMC', 'bayesian network',
        'probabilistic', 'belief network'
    ],
    'tensor-methods': [
        'tensor', 'tensor decomposition', 'tucker', 'CP decomposition',
        'tensor completion', 'tensor factorization'
    ],
    'functional-data': [
        'functional data', 'functional', 'profile', 'curve', 'FDA',
        'functional principal component'
    ],
    'graph-learning': [
        'graph', 'network', 'community detection', 'graph learning',
        'relational', 'node', 'edge', 'connectivity'
    ],
    'statistical-modeling': [
        'statistical', 'regression', 'hypothesis', 'significance',
        'inference', 'estimation', 'ANOVA', 'GLM'
    ],
    'optimization': [
        'optimization', 'bilevel', 'constraint', 'objective function',
        'linear programming', 'convex', 'optimization problem'
    ],
    'transportation': [
        'metro', 'subway', 'transportation', 'traffic', 'urban',
        'passenger', 'mobility', 'transit'
    ],
    'manufacturing': [
        'manufacturing', 'production', 'industrial', 'semiconductor',
        'assembly', 'supply chain', 'remanufacturing'
    ],
    'medical-ai': [
        'medical', 'clinical', 'diagnosis', 'patient', 'healthcare',
        'disease', 'immunofixation', 'glaucoma'
    ],
    'llms': [
        'large language model', 'large language models', 'LLM', 'LLMs',
        'language model', 'GPT', 'BERT',
        'natural language', 'NLP', 'text generation', 'language understanding'
    ]
}

def categorize_publication(pub: dict) -> Tuple[Set[str], str, str]:
    """
    Categorize a publication based on its title and abstract.
    Returns: (topic_categories, venue_category, combined_categories)
    """
    # Combine title and abstract for topic matching
    text = (pub.get('title', '') + ' ' + pub.get('abstract', '')).lower()

    # Find matching topics
    matching_topics = set()
    for topic, keywords in TOPICS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                matching_topics.add(topic)
                break

    # Determine venue category based on venue name
    venue = pub.get('venue', '').lower()
    venue_category = 'journals'  # default

    if 'ieee' in venue:
        venue_category = 'ieee'
    elif any(conf in venue for conf in ['conference', 'proceedings', 'aaai', 'ijcai', 'kdd', 'ecml']):
        venue_category = 'conferences'
    elif any(journal in venue for journal in ['journal', 'transactions', 'technometrics']):
        venue_category = 'journals'
    elif 'arxiv' in venue or 'preprint' in venue:
        venue_category = 'conferences'

    # Combine all categories
    all_categories = list(matching_topics) + [venue_category]
    combined_categories = ' '.join(all_categories)

    return matching_topics, venue_category, combined_categories

def format_authors(authors_str: str) -> str:
    """Format author names for display"""
    # Handle common author string formats
    authors_str = authors_str.replace(' and ', ', ')
    # Clean up any double commas
    authors_str = re.sub(r',\s*,', ',', authors_str)
    return authors_str.strip()

def format_venue(venue: str, year: int) -> str:
    """Format venue with year"""
    if venue == "Unknown Venue":
        return f"{year} Conference Proceedings"
    return f"{year} {venue}"

def get_pdf_url(pub: dict) -> str:
    """Get the best available PDF URL"""
    url = pub.get('url', '')
    eprint_url = pub.get('eprint_url', '')

    # Prefer eprint_url if available, otherwise use url
    return eprint_url if eprint_url else url

def generate_publication_html(pub: dict) -> str:
    """Generate HTML for a single publication"""
    topics, venue_cat, all_cats = categorize_publication(pub)

    # Format data
    title = pub.get('title', 'Untitled')
    authors = format_authors(pub.get('authors', ''))
    venue = format_venue(pub.get('venue', 'Unknown Venue'), pub.get('year', 2020))
    year = pub.get('year', 2020)
    pdf_url = get_pdf_url(pub)

    # Create data attributes for filtering
    data_attrs = f'data-year="{year}" data-category="{venue_cat}"'
    if topics:
        topic_attrs = ' '.join(f'data-{topic}="true"' for topic in topics)
        data_attrs += f' {topic_attrs}'

    # Generate HTML
    html = f'''                        <div class="publication-item {all_cats}" {data_attrs}>
                            <div class="publication-vertical-content">
                                <div class="publication-title">{title}</div>
                                <div class="publication-authors">{authors}</div>
                                <div class="publication-venue">{venue}</div>
                                <div class="publication-meta-row">
                                    <span class="publication-links">'''

    if pdf_url:
        html += f'''
                                        <a href="{pdf_url}" class="btn btn-small" target="_blank"><i class="fas fa-file-pdf"></i> PDF</a>'''
    else:
        html += f'''
                                        <a href="#" class="btn btn-small"><i class="fas fa-file-pdf"></i> PDF</a>'''

    html += f'''
                                        <a href="#" class="btn btn-small btn-secondary"><i class="fas fa-code"></i> Code</a>
                                    </span>
                                </div>
                            </div>
                        </div>'''

    return html

def process_publications():
    """Process all publications and generate HTML"""
    # Load publications
    with open('publications.json', 'r', encoding='utf-8') as f:
        publications = json.load(f)

    # Sort by year (newest first)
    publications.sort(key=lambda x: x.get('year', 0), reverse=True)

    # Group by year
    years = {}
    for pub in publications:
        year = pub.get('year', 2020)
        if year not in years:
            years[year] = []
        years[year].append(pub)

    # Generate HTML for each year
    html_sections = []

    for year in sorted(years.keys(), reverse=True):
        pubs_html = []
        for pub in years[year]:
            pubs_html.append(generate_publication_html(pub))

        section_html = f'''
                <!-- {year} Publications -->
                <div style="margin-bottom: 4rem;">
                    <h3 style="font-size: 2rem; margin-bottom: 2rem; color: #1e293b; position: relative; display: inline-block;">
                        {year} Publications
                        <span style="position: absolute; bottom: -8px; left: 0; width: 60px; height: 4px; background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); border-radius: 2px;"></span>
                    </h3>

                    <div class="publications-list">
{chr(10).join(pubs_html)}
                    </div>
                </div>'''

        html_sections.append(section_html)

    # Generate topic filter buttons - UPDATED with LLMs
    topic_filters = []
    for topic_key, keywords in TOPICS.items():
        # Create a readable topic name
        if topic_key == 'llms':
            topic_name = 'LLMs'
        else:
            topic_name = topic_key.replace('-', ' ').title()
        topic_filters.append(f'                        <button class="publication-filter btn btn-secondary" data-category="{topic_key}">{topic_name}</button>')

    # Generate complete HTML
    complete_html = f'''                <!-- Publication Categories -->
                <div style="margin-bottom: 4rem;">
                    <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 2rem;">
                        <button class="publication-filter btn btn-primary active" data-category="all">All Publications</button>
                        <button class="publication-filter btn btn-secondary" data-category="ieee">IEEE Transactions</button>
                        <button class="publication-filter btn btn-secondary" data-category="journals">Journals</button>
                        <button class="publication-filter btn btn-secondary" data-category="conferences">Conferences</button>
                    </div>

                    <!-- Topic Filters -->
                    <div style="display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap; margin-bottom: 1rem;">
                        <h4 style="width: 100%; text-align: center; margin-bottom: 0.5rem; color: #64748b; font-size: 1rem;">Filter by Research Topics:</h4>
{chr(10).join(topic_filters)}
                    </div>
                </div>

{chr(10).join(html_sections)}'''

    # Save to file
    with open('generated_publications_with_llm.html', 'w', encoding='utf-8') as f:
        f.write(complete_html)

    print(f"Processed {len(publications)} publications")
    print(f"Generated HTML saved to generated_publications_with_llm.html")

    # Print statistics
    topic_stats = {}
    for pub in publications:
        topics, _, _ = categorize_publication(pub)
        for topic in topics:
            topic_stats[topic] = topic_stats.get(topic, 0) + 1

    print("\nTopic distribution:")
    for topic, count in sorted(topic_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {topic}: {count} publications")

if __name__ == "__main__":
    process_publications()
