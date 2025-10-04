#!/usr/bin/env python3
"""
Google Scholar Publications Fetcher
Automatically fetches publications from Google Scholar and updates publications.json
"""

import json
import time
import re
from typing import Dict, List, Optional
from datetime import datetime

try:
    from scholarly import scholarly, ProxyGenerator
except ImportError:
    print("Error: scholarly library not installed.")
    print("Install with: pip install scholarly")
    exit(1)

class ScholarFetcher:
    def __init__(self, author_name: str = "Chen Zhang", affiliation: str = "Tsinghua University"):
        self.author_name = author_name
        self.affiliation = affiliation
        self.publications = []

    def setup_proxy(self) -> bool:
        """Setup proxy for Google Scholar access (optional but recommended)"""
        try:
            pg = ProxyGenerator()
            # Use free proxies (you may want to use premium proxies for better reliability)
            success = pg.FreeProxies()
            if success:
                scholarly.use_proxy(pg)
                print("✓ Proxy setup successful")
                return True
        except Exception as e:
            print(f"⚠ Proxy setup failed: {e}")
            print("Continuing without proxy (may be rate-limited)")
        return False

    def find_author(self) -> Optional[Dict]:
        """Find the author profile on Google Scholar"""
        print(f"Searching for author: {self.author_name}")

        try:
            # Search for the author
            search_query = scholarly.search_author(f'{self.author_name} {self.affiliation}')

            # Get the first result (most relevant)
            author = next(search_query)

            # Fill in additional details
            author = scholarly.fill(author)

            print(f"✓ Found author: {author.get('name', 'Unknown')}")
            print(f"  Affiliation: {author.get('affiliation', 'Unknown')}")
            print(f"  Citations: {author.get('citedby', 'Unknown')}")
            print(f"  H-index: {author.get('hindex', 'Unknown')}")

            return author

        except StopIteration:
            print(f"✗ Author '{self.author_name}' not found")
            return None
        except Exception as e:
            print(f"✗ Error finding author: {e}")
            return None

    def extract_publication_year(self, pub_info: Dict) -> int:
        """Extract publication year from various sources"""
        # Try bib year first
        if 'bib' in pub_info and 'pub_year' in pub_info['bib']:
            try:
                return int(pub_info['bib']['pub_year'])
            except (ValueError, TypeError):
                pass

        # Try parsing from venue string
        if 'bib' in pub_info and 'citation' in pub_info['bib']:
            citation = pub_info['bib']['citation']
            year_match = re.search(r'\b(19|20)\d{2}\b', citation)
            if year_match:
                return int(year_match.group())

        # Default to current year
        return datetime.now().year

    def clean_text(self, text: str) -> str:
        """Clean text by removing HTML tags and extra whitespace"""
        if not text:
            return ""

        # Remove HTML tags
        clean = re.sub('<.*?>', '', str(text))

        # Clean up whitespace
        clean = re.sub(r'\s+', ' ', clean).strip()

        return clean

    def fetch_publications(self) -> List[Dict]:
        """Fetch all publications for the author"""
        author = self.find_author()
        if not author:
            return []

        publications = []
        print(f"\nFetching publications...")

        try:
            # Get publications from the author profile
            pubs = author.get('publications', [])
            total_pubs = len(pubs)
            print(f"Found {total_pubs} publications")

            for i, pub in enumerate(pubs, 1):
                try:
                    print(f"Processing publication {i}/{total_pubs}...", end=' ')

                    # Fill in publication details (this may take time)
                    pub_filled = scholarly.fill(pub)

                    # Extract information
                    bib = pub_filled.get('bib', {})

                    publication = {
                        'title': self.clean_text(bib.get('title', 'Untitled')),
                        'authors': self.clean_text(bib.get('author', 'Unknown')),
                        'venue': self.clean_text(bib.get('venue', 'Unknown Venue')),
                        'year': self.extract_publication_year(pub_filled),
                        'citations': pub_filled.get('num_citations', 0),
                        'url': pub_filled.get('pub_url', ''),
                        'eprint_url': pub_filled.get('eprint_url', ''),
                        'abstract': self.clean_text(bib.get('abstract', ''))
                    }

                    publications.append(publication)
                    print("✓")

                    # Add delay to avoid rate limiting
                    time.sleep(2)

                except Exception as e:
                    print(f"✗ Error: {e}")
                    continue

        except Exception as e:
            print(f"✗ Error fetching publications: {e}")

        print(f"\n✓ Successfully fetched {len(publications)} publications")
        return publications

    def load_existing_publications(self, file_path: str = 'publications.json') -> List[Dict]:
        """Load existing publications from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"No existing publications file found at {file_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing existing publications: {e}")
            return []

    def merge_publications(self, new_pubs: List[Dict], existing_pubs: List[Dict]) -> List[Dict]:
        """Merge new publications with existing ones, avoiding duplicates"""
        print("Merging publications...")

        # Create a set of existing publication titles for quick lookup
        existing_titles = {pub.get('title', '').lower().strip() for pub in existing_pubs}

        merged = existing_pubs.copy()
        new_count = 0

        for pub in new_pubs:
            title = pub.get('title', '').lower().strip()

            # Check if this publication already exists
            if title and title not in existing_titles:
                merged.append(pub)
                existing_titles.add(title)
                new_count += 1

        print(f"✓ Added {new_count} new publications")
        print(f"✓ Total publications: {len(merged)}")

        # Sort by year (newest first)
        merged.sort(key=lambda x: x.get('year', 0), reverse=True)

        return merged

    def save_publications(self, publications: List[Dict], file_path: str = 'publications.json') -> bool:
        """Save publications to JSON file"""
        try:
            # Create backup of existing file
            import os
            if os.path.exists(file_path):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = f'backups/publications_backup_{timestamp}.json'
                os.makedirs('backups', exist_ok=True)

                with open(file_path, 'r', encoding='utf-8') as src:
                    with open(backup_path, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
                print(f"✓ Backup created: {backup_path}")

            # Save new publications
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(publications, f, indent=2, ensure_ascii=False)

            print(f"✓ Publications saved to {file_path}")
            return True

        except Exception as e:
            print(f"✗ Error saving publications: {e}")
            return False

def main():
    """Main function"""
    print("SAIL Lab - Google Scholar Publications Fetcher")
    print("=" * 50)

    # Configuration (you can modify these)
    AUTHOR_NAME = "Chen Zhang"
    AFFILIATION = "Tsinghua University"

    # Initialize fetcher
    fetcher = ScholarFetcher(AUTHOR_NAME, AFFILIATION)

    # Setup proxy (optional but recommended)
    fetcher.setup_proxy()

    # Fetch new publications
    print(f"\nStarting publication fetch...")
    new_publications = fetcher.fetch_publications()

    if not new_publications:
        print("No publications fetched. Exiting.")
        return

    # Load existing publications
    existing_publications = fetcher.load_existing_publications()

    # Merge publications
    merged_publications = fetcher.merge_publications(new_publications, existing_publications)

    # Save merged publications
    if fetcher.save_publications(merged_publications):
        print("\n🎉 Publication update completed successfully!")
        print("\nNext steps:")
        print("1. Review the updated publications.json")
        print("2. Run: python process_publications_updated.py")
        print("3. Check the generated HTML")
        print("4. Commit changes to git")
    else:
        print("\n❌ Failed to save publications")

if __name__ == "__main__":
    main()