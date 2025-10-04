#!/usr/bin/env python3
"""
Automated Publications Processing
Enhanced version of the existing process_publications_updated.py with automation features
"""

import json
import re
import sys
import os
from typing import Dict, List, Set, Tuple
from datetime import datetime

# Import the existing processing logic
sys.path.append('.')
try:
    from process_publications_updated import (
        TOPICS, categorize_publication, format_authors,
        format_venue, get_pdf_url, generate_publication_html
    )
except ImportError:
    print("Error: Could not import from process_publications_updated.py")
    print("Make sure the file exists in the current directory")
    exit(1)

class AutoPublicationProcessor:
    def __init__(self, publications_file: str = 'publications.json'):
        self.publications_file = publications_file
        self.publications = []
        self.backup_dir = 'backups'

    def load_publications(self) -> bool:
        """Load publications from JSON file"""
        try:
            with open(self.publications_file, 'r', encoding='utf-8') as f:
                self.publications = json.load(f)
            print(f"✓ Loaded {len(self.publications)} publications")
            return True
        except FileNotFoundError:
            print(f"Error: {self.publications_file} not found")
            return False
        except json.JSONDecodeError as e:
            print(f"Error parsing {self.publications_file}: {e}")
            return False

    def create_backup(self) -> str:
        """Create backup of current index.html"""
        os.makedirs(self.backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(self.backup_dir, f'index_backup_{timestamp}.html')

        try:
            if os.path.exists('index.html'):
                with open('index.html', 'r', encoding='utf-8') as src:
                    with open(backup_file, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
                print(f"✓ Backup created: {backup_file}")
                return backup_file
        except Exception as e:
            print(f"Warning: Could not create backup: {e}")

        return ""

    def generate_publications_html(self) -> str:
        """Generate complete publications HTML section"""
        if not self.publications:
            return ""

        # Sort publications by year (newest first)
        sorted_pubs = sorted(self.publications, key=lambda x: x.get('year', 0), reverse=True)

        # Group by year
        years = {}
        for pub in sorted_pubs:
            year = pub.get('year', 2020)
            if year not in years:
                years[year] = []
            years[year].append(pub)

        # Generate HTML sections for each year
        html_sections = []

        for year in sorted(years.keys(), reverse=True):
            pubs_html = []
            for pub in years[year]:
                pubs_html.append(generate_publication_html(pub))

            section_html = f'''
                <!-- {year} Publications -->
                <div style="margin-bottom: 4rem;">
                    <h3 style="font-size: 2rem; margin-bottom: 2rem; color: var(--text-primary); position: relative; display: inline-block;">
                        {year} Publications
                        <span style="position: absolute; bottom: -8px; left: 0; width: 60px; height: 4px; background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); border-radius: 2px;"></span>
                    </h3>

                    <div class="publications-list">
{chr(10).join(pubs_html)}
                    </div>
                </div>'''

            html_sections.append(section_html)

        # Generate topic filter buttons
        topic_filters = []
        for topic_key, keywords in TOPICS.items():
            if topic_key == 'llms':
                topic_name = 'LLMs'
                icon = '<i class="fas fa-robot"></i>'
            elif topic_key == 'deep-learning':
                topic_name = 'Deep Learning'
                icon = '<i class="fas fa-brain"></i>'
            elif topic_key == 'machine-learning':
                topic_name = 'Machine Learning'
                icon = '<i class="fas fa-cogs"></i>'
            elif topic_key == 'reinforcement-learning':
                topic_name = 'Reinforcement Learning'
                icon = '<i class="fas fa-sync-alt"></i>'
            elif topic_key == 'time-series':
                topic_name = 'Time Series'
                icon = '<i class="fas fa-chart-line"></i>'
            elif topic_key == 'anomaly-detection':
                topic_name = 'Anomaly Detection'
                icon = '<i class="fas fa-search"></i>'
            elif topic_key == 'causal-inference':
                topic_name = 'Causal Inference'
                icon = '<i class="fas fa-project-diagram"></i>'
            elif topic_key == 'bayesian-methods':
                topic_name = 'Bayesian Methods'
                icon = '<i class="fas fa-calculator"></i>'
            elif topic_key == 'tensor-methods':
                topic_name = 'Tensor Methods'
                icon = '<i class="fas fa-cube"></i>'
            elif topic_key == 'functional-data':
                topic_name = 'Functional Data'
                icon = '<i class="fas fa-wave-square"></i>'
            elif topic_key == 'graph-learning':
                topic_name = 'Graph Learning'
                icon = '<i class="fas fa-share-alt"></i>'
            elif topic_key == 'statistical-modeling':
                topic_name = 'Statistical Modeling'
                icon = '<i class="fas fa-chart-bar"></i>'
            elif topic_key == 'optimization':
                topic_name = 'Optimization'
                icon = '<i class="fas fa-bullseye"></i>'
            elif topic_key == 'transportation':
                topic_name = 'Transportation'
                icon = '<i class="fas fa-car"></i>'
            elif topic_key == 'manufacturing':
                topic_name = 'Manufacturing'
                icon = '<i class="fas fa-industry"></i>'
            elif topic_key == 'medical-ai':
                topic_name = 'Medical AI'
                icon = '<i class="fas fa-heartbeat"></i>'
            else:
                topic_name = topic_key.replace('-', ' ').title()
                icon = '<i class="fas fa-tag"></i>'

            topic_filters.append(f'                        <button class="publication-filter btn btn-secondary" data-category="{topic_key}">{icon} {topic_name}</button>')

        # Generate complete publications section HTML
        complete_html = f'''                <!-- Publication Categories -->
                <div style="margin-bottom: 4rem;">
                    <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 2rem;">
                        <button class="publication-filter btn btn-primary active" data-category="all"><i class="fas fa-list-ul"></i> All Publications</button>
                        <button class="publication-filter btn btn-secondary" data-category="ieee"><i class="fas fa-graduation-cap"></i> IEEE Transactions</button>
                        <button class="publication-filter btn btn-secondary" data-category="journals"><i class="fas fa-book-open"></i> Journals</button>
                        <button class="publication-filter btn btn-secondary" data-category="conferences"><i class="fas fa-users"></i> Conferences</button>
                    </div>

                    <!-- Topic Filters -->
                    <div style="display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap; margin-bottom: 1rem;">
                        <h4 style="width: 100%; text-align: center; margin-bottom: 0.5rem; color: var(--text-secondary); font-size: 1rem;">Filter by Research Topics:</h4>
{chr(10).join(topic_filters)}
                    </div>
                </div>

{chr(10).join(html_sections)}'''

        return complete_html

    def update_index_html(self, publications_html: str) -> bool:
        """Update index.html with new publications section"""
        try:
            # Read current index.html
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()

            # Find publications section boundaries
            # Look for the publications filter section start
            start_marker = '                <!-- Publication Categories -->'
            start_pos = content.find(start_marker)

            if start_pos == -1:
                print("Error: Could not find publications section start marker")
                return False

            # Find the end of publications section (before publication stats or next major section)
            # Look for the publication impact section or stats section
            end_markers = [
                '                <!-- Publication Stats -->',
                '                <!-- Publication Impact -->',
                '       ',  # Multiple spaces indicating end of section
            ]

            end_pos = -1
            for marker in end_markers:
                pos = content.find(marker, start_pos + len(start_marker))
                if pos != -1:
                    end_pos = pos
                    break

            if end_pos == -1:
                print("Error: Could not find publications section end marker")
                return False

            # Replace publications section
            new_content = content[:start_pos] + publications_html + '\n\n' + content[end_pos:]

            # Write updated content
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(new_content)

            print("✓ Successfully updated publications section in index.html")
            return True

        except Exception as e:
            print(f"Error updating index.html: {e}")
            return False

    def generate_statistics(self) -> Dict:
        """Generate publication statistics"""
        if not self.publications:
            return {}

        total_pubs = len(self.publications)
        total_citations = sum(pub.get('citations', 0) for pub in self.publications)

        # Count by venue type
        ieee_count = sum(1 for pub in self.publications if 'ieee' in pub.get('venue', '').lower())

        # Count by topic
        topic_stats = {}
        for pub in self.publications:
            topics, _, _ = categorize_publication(pub)
            for topic in topics:
                topic_stats[topic] = topic_stats.get(topic, 0) + 1

        # Count by year
        year_stats = {}
        for pub in self.publications:
            year = pub.get('year', 'Unknown')
            year_stats[year] = year_stats.get(year, 0) + 1

        return {
            'total_publications': total_pubs,
            'total_citations': total_citations,
            'ieee_transactions': ieee_count,
            'topics': topic_stats,
            'years': year_stats
        }

    def process(self) -> bool:
        """Main processing function"""
        print("Auto Publications Processor")
        print("=" * 30)

        # Load publications
        if not self.load_publications():
            return False

        # Create backup
        backup_file = self.create_backup()

        # Generate publications HTML
        print("Generating publications HTML...")
        publications_html = self.generate_publications_html()

        if not publications_html:
            print("Error: No publications HTML generated")
            return False

        # Update index.html
        if self.update_index_html(publications_html):
            # Generate and display statistics
            stats = self.generate_statistics()
            print(f"\n📊 Publication Statistics:")
            print(f"  Total publications: {stats['total_publications']}")
            print(f"  Total citations: {stats['total_citations']}")
            print(f"  IEEE Transactions: {stats['ieee_transactions']}")

            print(f"\n🏷️  Top topics:")
            for topic, count in sorted(stats['topics'].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"    {topic}: {count} publications")

            print(f"\n🎉 Publications section updated successfully!")

            # Also update metrics sections
            print("\n📈 Updating publication metrics sections...")
            try:
                from update_publication_metrics import PublicationMetricsCalculator
                metrics_calc = PublicationMetricsCalculator()
                metrics_calc.publications = self.publications  # Reuse loaded publications

                # Calculate metrics
                metrics = metrics_calc.calculate_metrics()
                venues = metrics_calc.extract_key_venues(metrics)

                # Generate and update metrics sections
                main_stats_html = metrics_calc.generate_main_stats_section_html(metrics)
                impact_html = metrics_calc.generate_impact_section_html(metrics, venues)

                success_count = 0
                if metrics_calc.update_main_stats_section(main_stats_html):
                    success_count += 1
                if metrics_calc.update_html_metrics(impact_html):
                    success_count += 1

                if success_count > 0:
                    print(f"✓ Updated {success_count}/2 metrics sections")
                else:
                    print("⚠ Could not update metrics sections")

            except Exception as e:
                print(f"⚠ Could not update metrics: {e}")

            return True
        else:
            print("❌ Failed to update publications section")
            if backup_file:
                print(f"Backup available at: {backup_file}")
            return False

def main():
    """Main function"""
    processor = AutoPublicationProcessor()
    success = processor.process()

    if success:
        print("\nNext steps:")
        print("1. Review the updated index.html")
        print("2. Test the publication filters")
        print("3. Commit changes to git")
    else:
        print("\nProcessing failed. Check error messages above.")

if __name__ == "__main__":
    main()