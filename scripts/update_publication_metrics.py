#!/usr/bin/env python3
"""
Publication Metrics Updater
Automatically calculates and updates the Publication Impact section with real data
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Tuple
from collections import Counter

class PublicationMetricsCalculator:
    def __init__(self, publications_file: str = 'publications.json'):
        self.publications_file = publications_file
        self.publications = []

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

    def calculate_metrics(self) -> Dict[str, any]:
        """Calculate comprehensive publication metrics"""
        if not self.publications:
            return {}

        metrics = {}

        # Basic counts
        metrics['total_publications'] = len(self.publications)
        metrics['total_citations'] = sum(pub.get('citations', 0) for pub in self.publications)

        # IEEE Transactions count
        ieee_count = 0
        ieee_venues = []
        for pub in self.publications:
            venue = pub.get('venue', '').lower()
            if 'ieee' in venue and 'transaction' in venue:
                ieee_count += 1
                ieee_venues.append(pub.get('venue', ''))

        metrics['ieee_transactions'] = ieee_count

        # Top venues analysis
        venues = [pub.get('venue', '') for pub in self.publications if pub.get('venue', '') != 'Unknown Venue']
        venue_counts = Counter(venues)
        metrics['top_venues'] = venue_counts.most_common(10)

        # Journal vs Conference classification
        journal_count = 0
        conference_count = 0
        for pub in self.publications:
            venue = pub.get('venue', '').lower()
            if any(keyword in venue for keyword in ['journal', 'transactions', 'technometrics']):
                journal_count += 1
            elif any(keyword in venue for keyword in ['conference', 'proceedings', 'aaai', 'ijcai']):
                conference_count += 1

        metrics['journal_publications'] = journal_count
        metrics['conference_publications'] = conference_count

        # Recent years analysis (last 5 years)
        current_year = datetime.now().year
        recent_years = list(range(current_year - 4, current_year + 1))
        recent_pubs = [pub for pub in self.publications if pub.get('year', 0) in recent_years]
        metrics['recent_publications'] = len(recent_pubs)
        metrics['recent_citations'] = sum(pub.get('citations', 0) for pub in recent_pubs)

        # High-impact publications (>= 50 citations)
        high_impact = [pub for pub in self.publications if pub.get('citations', 0) >= 50]
        metrics['high_impact_publications'] = len(high_impact)

        # H-index calculation (simplified)
        citations_sorted = sorted([pub.get('citations', 0) for pub in self.publications], reverse=True)
        h_index = 0
        for i, citations in enumerate(citations_sorted, 1):
            if citations >= i:
                h_index = i
            else:
                break
        metrics['h_index'] = h_index

        # Average citations per paper
        if metrics['total_publications'] > 0:
            metrics['avg_citations'] = metrics['total_citations'] / metrics['total_publications']
        else:
            metrics['avg_citations'] = 0

        # First author papers (assuming first author is Chen Zhang)
        first_author_count = 0
        for pub in self.publications:
            authors = pub.get('authors', '')
            if authors.lower().startswith('chen zhang'):
                first_author_count += 1
        metrics['first_author_papers'] = first_author_count

        return metrics

    def extract_key_venues(self, metrics: Dict) -> Dict[str, List[str]]:
        """Extract and categorize key publication venues"""
        venues = {}

        # IEEE Transactions
        ieee_venues = set()
        top_journals = set()
        conferences = set()

        for pub in self.publications:
            venue = pub.get('venue', '').strip()
            if not venue or venue == 'Unknown Venue':
                continue

            venue_lower = venue.lower()

            if 'ieee' in venue_lower:
                if 'transaction' in venue_lower:
                    # Extract the specific IEEE transaction name
                    ieee_name = venue.replace('IEEE Transactions on', '').replace('IEEE Transaction on', '').strip()
                    if len(ieee_name) > 5:  # Valid length
                        ieee_venues.add(ieee_name)
                else:
                    ieee_venues.add(venue)

            elif any(keyword in venue_lower for keyword in ['journal', 'technometrics']):
                # Extract journal name
                journal_name = venue
                if 'journal of' in venue_lower:
                    journal_name = venue
                elif len(venue) < 50:  # Reasonable length
                    journal_name = venue
                if journal_name:
                    top_journals.add(journal_name)

            elif any(keyword in venue_lower for keyword in ['conference', 'proceedings', 'aaai', 'ijcai', 'icml', 'nips']):
                # Extract conference name
                conf_name = venue
                if 'proceedings of' in venue_lower:
                    conf_name = venue.replace('Proceedings of the', '').replace('Proceedings of', '').strip()
                if len(conf_name) < 60:  # Reasonable length
                    conferences.add(conf_name)

        venues['ieee_transactions'] = sorted(list(ieee_venues))[:5]  # Top 5
        venues['top_journals'] = sorted(list(top_journals))[:5]      # Top 5
        venues['conferences'] = sorted(list(conferences))[:5]        # Top 5

        return venues

    def generate_main_stats_section_html(self, metrics: Dict) -> str:
        """Generate the main Statistics section HTML with real metrics (HOME PAGE ONLY)"""
        # Estimate active researchers from recent publications (last 2 years)
        current_year = datetime.now().year
        recent_years = [current_year, current_year - 1]
        recent_authors = set()

        for pub in self.publications:
            if pub.get('year', 0) in recent_years:
                authors = pub.get('authors', '')
                # Split authors and add to set (simplified estimation)
                author_list = [a.strip() for a in authors.split(',') if a.strip()]
                recent_authors.update(author_list[:3])  # Take first 3 authors per paper

        active_researchers = min(len(recent_authors), 15)  # Cap at reasonable number

        # Elite industry partners (estimated from venue diversity and collaboration indicators)
        industry_indicators = 0
        for pub in self.publications:
            title_abstract = (pub.get('title', '') + ' ' + pub.get('abstract', '')).lower()
            if any(keyword in title_abstract for keyword in ['industrial', 'manufacturing', 'tesla', 'industry', 'commercial']):
                industry_indicators += 1

        elite_partners = min(industry_indicators // 3, 12)  # Estimate based on industry-related publications

        stats_html = f'''        <!-- Statistics -->
        <section class="section">
            <div class="container">
                <div class="stats-section">
                    <div class="stats-grid">
                        <div class="stat-item">
                            <h3 class="stat-number">{active_researchers}</h3>
                            <p>Active Researchers</p>
                        </div>
                        <div class="stat-item">
                            <h3 class="stat-number">{metrics['total_publications']}</h3>
                            <p>Top-Tier Publications</p>
                        </div>
                        <div class="stat-item">
                            <h3 class="stat-number">{elite_partners}</h3>
                            <p>Elite Industry Partners</p>
                        </div>
                        <div class="stat-item">
                            <h3 class="stat-number">{metrics['total_citations']:,}</h3>
                            <p>Total Citations</p>
                        </div>
                        <div class="stat-item">
                            <h3>AI-First</h3>
                            <p>Research Philosophy</p>
                        </div>
                    </div>
                </div>
                <!-- Partners Collaboration Section -->
                <div style="margin-top: 5rem;">
                    <div style="text-align: center; margin-bottom: 3rem;">
                        <h3 style="color: var(--text-primary); font-size: 2rem; margin-bottom: 1rem;">Trusted by Leading Organizations</h3>
                        <p style="color: var(--text-secondary); font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
                            Collaborating with world-class institutions and industry leaders to drive AI innovation forward
                        </p>
                    </div>

                    <div class="partners-slider-container">
                        <div class="partners-slider">
                            <!-- First set of partners -->
                            <div class="partners-slide">
                                <div class="partner-logo-item">
                                    <img src="logo/huawei_logo.png" alt="Huawei Logo" style="width: 104px; height: auto;"
                                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                    <div style="display: none; align-items: center; justify-content: center; width: 100%; height: 100%; background: #FF0000; border-radius: 8px; color: white; font-weight: 700; font-size: 1.1rem;">
                                        HUAWEI
                                    </div>
                                </div>
                                <div class="partner-logo-item">
                                    <img src="logo/meituan.svg" alt="Meituan Logo" style="width: 104px; height: auto;"
                                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                    <div style="display: none; align-items: center; justify-content: center; width: 100%; height: 100%; background: #FFBE00; border-radius: 8px; color: white; font-weight: 700; font-size: 1rem; flex-direction: column;">
                                        <div style="font-size: 0.9rem;">美团</div>
                                        <div style="font-size: 0.8rem;">MEITUAN</div>
                                    </div>
                                </div>
                                <div class="partner-logo-item">
                                    <img src="logo/tecent_logo.png" alt="Tencent Logo" style="width: 104px; height: auto;"
                                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                    <div style="display: none; align-items: center; justify-content: center; width: 100%; height: 100%; background: #00A0E6; border-radius: 8px; color: white; font-weight: 700; font-size: 1.1rem;">
                                        Tencent
                                    </div>
                                </div>
                                <div class="partner-logo-item">
                                    <img src="logo/Alibaba-Logo.png" alt="Alibaba Logo" style="width: 104px; height: auto;"
                                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                    <div style="display: none; align-items: center; justify-content: center; width: 100%; height: 100%; background: #FF6A00; border-radius: 8px; color: white; font-weight: 700; font-size: 1.1rem;">
                                        Alibaba
                                    </div>
                                </div>
                                <div class="partner-logo-item">
                                    <img src="logo/Baidu.svg.png" alt="Baidu Logo" style="width: 104px; height: auto;"
                                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                    <div style="display: none; align-items: center; justify-content: center; width: 100%; height: 100%; background: #2932E1; border-radius: 8px; color: white; font-weight: 700; font-size: 1rem; flex-direction: column;">
                                        <div style="font-size: 0.9rem;">百度</div>
                                        <div style="font-size: 0.8rem;">BAIDU</div>
                                    </div>
                                </div>
                                <div class="partner-logo-item">
                                    <img src="logo/ByteDance_logo.svg" alt="ByteDance Logo" style="width: 104px; height: auto;"
                                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                    <div style="display: none; align-items: center; justify-content: center; width: 100%; height: 100%; background: #161823; border-radius: 8px; color: white; font-weight: 700; font-size: 1rem;">
                                        ByteDance
                                    </div>
                                </div>
                            </div>
                            <!-- Duplicate set for seamless loop -->
                            <div class="partners-slide">
                                <div class="partner-logo-item">
                                    <img src="logo/huawei_logo.png" alt="Huawei Logo" style="width: 104px; height: auto;"
                                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                    <div style="display: none; align-items: center; justify-content: center; width: 100%; height: 100%; background: #FF0000; border-radius: 8px; color: white; font-weight: 700; font-size: 1.1rem;">
                                        HUAWEI
                                    </div>
                                </div>
                                <div class="partner-logo-item">
                                    <img src="logo/meituan.svg" alt="Meituan Logo" style="width: 104px; height: auto;"
                                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                    <div style="display: none; align-items: center; justify-content: center; width: 100%; height: 100%; background: #FFBE00; border-radius: 8px; color: white; font-weight: 700; font-size: 1rem; flex-direction: column;">
                                        <div style="font-size: 0.9rem;">美团</div>
                                        <div style="font-size: 0.8rem;">MEITUAN</div>
                                    </div>
                                </div>
                                <div class="partner-logo-item">
                                    <img src="logo/tecent_logo.png" alt="Tencent Logo" style="width: 104px; height: auto;"
                                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                    <div style="display: none; align-items: center; justify-content: center; width: 100%; height: 100%; background: #00A0E6; border-radius: 8px; color: white; font-weight: 700; font-size: 1.1rem;">
                                        Tencent
                                    </div>
                                </div>
                                <div class="partner-logo-item">
                                    <img src="logo/Alibaba-Logo.png" alt="Alibaba Logo" style="width: 104px; height: auto;"
                                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                    <div style="display: none; align-items: center; justify-content: center; width: 100%; height: 100%; background: #FF6A00; border-radius: 8px; color: white; font-weight: 700; font-size: 1.1rem;">
                                        Alibaba
                                    </div>
                                </div>
                                <div class="partner-logo-item">
                                    <img src="logo/Baidu.svg.png" alt="Baidu Logo" style="width: 104px; height: auto;"
                                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                    <div style="display: none; align-items: center; justify-content: center; width: 100%; height: 100%; background: #2932E1; border-radius: 8px; color: white; font-weight: 700; font-size: 1rem; flex-direction: column;">
                                        <div style="font-size: 0.9rem;">百度</div>
                                        <div style="font-size: 0.8rem;">BAIDU</div>
                                    </div>
                                </div>
                                <div class="partner-logo-item">
                                    <img src="logo/ByteDance_logo.svg" alt="ByteDance Logo" style="width: 104px; height: auto;"
                                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                    <div style="display: none; align-items: center; justify-content: center; width: 100%; height: 100%; background: #161823; border-radius: 8px; color: white; font-weight: 700; font-size: 1rem;">
                                        ByteDance
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Call to Action Section -->
                <div style="margin-top: 5rem;">
                    <div style="text-align: center; margin-bottom: 3rem;">
                        <h3 style="color: var(--text-primary); font-size: 2rem; margin-bottom: 1rem;">Ready to Collaborate?</h3>
                        <p style="color: var(--text-secondary); font-size: 1.2rem; max-width: 600px; margin: 0 auto;">
                            Join our mission to advance superintelligence through cutting-edge AI research and industrial applications.
                        </p>
                    </div>

                    <div class="cta-cards-container">
                        <div class="cta-card">
                            <i class="fas fa-graduation-cap" style="font-size: 3rem; color: var(--accent-blue); margin-bottom: 1rem;"></i>
                            <h4 style="color: var(--text-primary); margin-bottom: 1rem;">Join Our Team</h4>
                            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">Explore PhD, postdoc, and research opportunities</p>
                            <a href="#" class="btn btn-primary" data-page="contact">
                                <i class="fas fa-envelope"></i>
                                Apply Now
                            </a>
                        </div>

                        <div class="cta-card">
                            <i class="fas fa-lightbulb" style="font-size: 3rem; color: var(--accent-blue); margin-bottom: 1rem;"></i>
                            <h4 style="color: var(--text-primary); margin-bottom: 1rem;">Latest Research</h4>
                            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">Discover our recent publications and breakthroughs</p>
                            <a href="#" class="btn btn-primary" data-page="publications">
                                <i class="fas fa-book"></i>
                                Read Papers
                            </a>
                        </div>

                        <div class="cta-card">
                            <i class="fab fa-github" style="font-size: 3rem; color: var(--accent-blue); margin-bottom: 1rem;"></i>
                            <h4 style="color: var(--text-primary); margin-bottom: 1rem;">Open Source Code</h4>
                            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">Explore our research implementations and contribute to our projects</p>
                            <a href="#" class="btn btn-primary" data-page="opensource">
                                <i class="fab fa-github"></i>
                                View Code
                            </a>
                        </div>
                    </div>

                    <!-- Quick Links -->
                    <div style="text-align: center;">
                        <h4 style="color: var(--text-primary); margin-bottom: 1.5rem;">Quick Navigation</h4>
                        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                            <a href="#" data-page="research" class="quick-nav-link">
                                <i class="fas fa-flask"></i> Research Areas
                            </a>
                            <a href="#" data-page="publications" class="quick-nav-link">
                                <i class="fas fa-file-alt"></i> Publications
                            </a>
                            <a href="#" data-page="team" class="quick-nav-link">
                                <i class="fas fa-users"></i> Meet the Team
                            </a>
                            <a href="#" data-page="partners" class="quick-nav-link">
                                <i class="fas fa-handshake"></i> Partners
                            </a>
                            <a href="#" data-page="opensource" class="quick-nav-link">
                                <i class="fab fa-github"></i> Open Source
                            </a>
                            <a href="#" data-page="contact" class="quick-nav-link">
                                <i class="fas fa-envelope"></i> Contact Us
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </section>'''

        return stats_html

    def generate_impact_section_html(self, metrics: Dict, venues: Dict) -> str:
        """Generate the Publication Impact section HTML with real metrics"""

        # Format numbers nicely
        total_pubs = metrics['total_publications']
        ieee_count = metrics['ieee_transactions']
        total_citations = metrics['total_citations']
        h_index = metrics['h_index']

        impact_html = f'''                <div style="margin-top: 5rem;">
                    <div class="section-header">
                        <h2>Publication Impact</h2>
                        <p>Research metrics and achievements</p>
                    </div>
                    <div class="stats-grid">
                        <div class="stat-item">
                            <h3 class="stat-number">{total_pubs}</h3>
                            <p>Total Publications</p>
                        </div>
                        <div class="stat-item">
                            <h3 class="stat-number">{ieee_count}</h3>
                            <p>IEEE Transactions</p>
                        </div>
                        <div class="stat-item">
                            <h3 class="stat-number">{h_index}</h3>
                            <p>H-Index</p>
                        </div>
                        <div class="stat-item">
                            <h3 class="stat-number">{total_citations:,}</h3>
                            <p>Total Citations</p>
                        </div>
                    </div>
                </div>

                <!-- Key Venues -->
                <div class="key-venues-section">
                    <h3 style="font-size: 1.8rem; color: var(--text-primary); margin-bottom: 1.5rem; font-weight: 700;">
                        <i class="fas fa-university" style="color: #0ea5e9; margin-right: 0.5rem;"></i>
                        Key Publication Venues
                    </h3>
                    <div class="venue-grid">
                        <div class="venue-card">
                            <h4 style="color: var(--accent-blue); margin-bottom: 0.5rem;">IEEE Transactions</h4>
                            <ul style="color: #64748b; margin: 0; padding-left: 1rem;">'''

        # Add IEEE venues
        for venue in venues.get('ieee_transactions', [])[:4]:
            impact_html += f'\n                                <li>{venue}</li>'

        impact_html += f'''
                            </ul>
                        </div>
                        <div class="venue-card">
                            <h4 style="color: var(--accent-blue); margin-bottom: 0.5rem;">Top Journals</h4>
                            <ul style="color: #64748b; margin: 0; padding-left: 1rem;">'''

        # Add top journals
        for venue in venues.get('top_journals', [])[:4]:
            impact_html += f'\n                                <li>{venue}</li>'

        impact_html += f'''
                            </ul>
                        </div>
                        <div class="venue-card">
                            <h4 style="color: var(--accent-blue); margin-bottom: 0.5rem;">Top Conferences</h4>
                            <ul style="color: #64748b; margin: 0; padding-left: 1rem;">'''

        # Add conferences
        for venue in venues.get('conferences', [])[:4]:
            impact_html += f'\n                                <li>{venue}</li>'

        impact_html += '''
                            </ul>
                        </div>
                    </div>
                </div>'''

        return impact_html

    def update_main_stats_section(self, stats_html: str) -> bool:
        """Update the main Statistics section in index.html"""
        try:
            # Read current index.html
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()

            # Find the main Statistics section
            start_marker = '        <!-- Statistics -->'
            start_pos = content.find(start_marker)

            if start_pos == -1:
                print("Warning: Could not find main Statistics section")
                return False

            # Find the end of the section
            search_start = start_pos + len(start_marker)
            end_marker = '        </section>'
            end_pos = content.find(end_marker, search_start)

            if end_pos == -1:
                print("Warning: Could not find Statistics section end")
                return False

            # Include the closing tag
            end_pos += len(end_marker)

            # Replace the section
            content = content[:start_pos] + stats_html + content[end_pos:]

            # Write back to temporary variable for next update
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(content)

            print("✓ Successfully updated main Statistics section")
            return True

        except Exception as e:
            print(f"Warning: Error updating main statistics: {e}")
            return False

    def update_html_metrics(self, impact_html: str) -> bool:
        """Update the Publication Impact section in index.html"""
        try:
            # Read current index.html
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()

            # Find the Publication Impact section
            start_marker = '                <div style="margin-top: 5rem;">'
            start_pos = content.find(start_marker)

            if start_pos == -1:
                print("Error: Could not find Publication Impact section start")
                return False

            # Find the end of the section (looking for the next major section)
            # Search for the closing div of the key venues section
            search_start = start_pos + len(start_marker)

            # Try multiple possible end markers
            possible_end_markers = [
                '                </div>\n\n            </div>',
                '                </div>\n            </div>',
                '            </div>\n        </section>',
                '        </section>'
            ]

            end_pos = -1
            for marker in possible_end_markers:
                pos = content.find(marker, search_start)
                if pos != -1:
                    end_pos = pos + len(marker)
                    break

            if end_pos == -1:
                print("Error: Could not find Publication Impact section end")
                return False

            # Replace the section
            new_content = content[:start_pos] + impact_html + content[end_pos:]

            # Write updated content
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(new_content)

            print("✓ Successfully updated Publication Impact section")
            return True

        except Exception as e:
            print(f"Error updating HTML: {e}")
            return False

    def process_metrics_update(self) -> bool:
        """Main function to calculate and update publication metrics"""
        print("📊 Publication Metrics Updater")
        print("=" * 35)

        # Load publications
        if not self.load_publications():
            return False

        # Calculate metrics
        print("Calculating publication metrics...")
        metrics = self.calculate_metrics()

        if not metrics:
            print("Error: Could not calculate metrics")
            return False

        # Extract key venues
        venues = self.extract_key_venues(metrics)

        # Create backup first
        from datetime import datetime
        import os
        os.makedirs('backups', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backups/index_metrics_backup_{timestamp}.html'

        try:
            with open('index.html', 'r', encoding='utf-8') as src:
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            print(f"✓ Backup created: {backup_file}")
        except Exception as e:
            print(f"Warning: Could not create backup: {e}")

        # Generate HTML sections
        print("Generating HTML sections...")
        main_stats_html = self.generate_main_stats_section_html(metrics)
        impact_html = self.generate_impact_section_html(metrics, venues)

        # Update both sections
        success_count = 0

        # Update main statistics section
        if self.update_main_stats_section(main_stats_html):
            success_count += 1

        # Update publication impact section
        if self.update_html_metrics(impact_html):
            success_count += 1

        if success_count > 0:
            print(f"\n📈 Metrics Updated Successfully!")
            print(f"  Sections updated: {success_count}/2")
            print(f"  Total Publications: {metrics['total_publications']}")
            print(f"  IEEE Transactions: {metrics['ieee_transactions']}")
            print(f"  Total Citations: {metrics['total_citations']:,}")
            print(f"  H-Index: {metrics['h_index']}")
            print(f"  Average Citations: {metrics['avg_citations']:.1f}")
            print(f"  High Impact Papers (50+ cites): {metrics['high_impact_publications']}")

            print(f"\n🏛️  Key Venues Found:")
            print(f"  IEEE Transactions: {len(venues['ieee_transactions'])}")
            print(f"  Top Journals: {len(venues['top_journals'])}")
            print(f"  Conferences: {len(venues['conferences'])}")

            return True
        else:
            print("❌ Failed to update any metrics sections")
            return False

def main():
    """Main function"""
    calculator = PublicationMetricsCalculator()
    success = calculator.process_metrics_update()

    if success:
        print("\nNext steps:")
        print("1. Review the updated Publication Impact section")
        print("2. Verify metrics accuracy")
        print("3. Commit changes to git")
    else:
        print("\nMetrics update failed. Check error messages above.")

if __name__ == "__main__":
    main()