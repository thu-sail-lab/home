#!/usr/bin/env python3
"""
News HTML Generator
Generates news section HTML from news.json data while preserving exact design and layout
"""

import json
from datetime import datetime
from typing import List, Dict

def load_news_data(file_path: str = 'data/news.json') -> List[Dict]:
    """Load news data from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing {file_path}: {e}")
        return []

def generate_news_item_html(news_item: Dict) -> str:
    """Generate HTML for a single news item matching current design"""
    html = f'''                        <!-- News Item -->
                        <div class="news-item">
                            <div class="news-date">
                                <span class="news-month">{news_item['month']}</span>
                                <span class="news-day">{news_item['day']}</span>
                                <span class="news-year">{news_item['year']}</span>
                            </div>
                            <div class="news-content">
                                <div class="news-icon">
                                    <i class="{news_item['icon']}"></i>
                                </div>
                                <div class="news-text">
                                    <h4>{news_item['title']}</h4>
                                    <p>{news_item['description']}</p>
                                </div>
                            </div>
                        </div>'''
    return html

def generate_news_section_html(news_data: List[Dict]) -> str:
    """Generate complete news section HTML matching current design exactly"""

    # Separate featured (recent) and past news
    featured_news = [item for item in news_data if item.get('featured', False) and item.get('visible', True)]
    past_news = [item for item in news_data if not item.get('featured', False) and item.get('visible', True)]

    # Limit featured news to 5 items (matching current design)
    featured_news = featured_news[:5]

    # Generate featured news items HTML
    featured_html = '\n'.join([generate_news_item_html(item) for item in featured_news])

    # Generate past news items HTML
    past_html = '\n'.join([generate_news_item_html(item) for item in past_news])

    # Complete news section HTML (matching current structure exactly)
    news_section_html = f'''        <!-- News Section -->
        <section class="section">
            <div class="container">
                <div class="section-header">
                    <h2><i class="fas fa-newspaper"></i> Lab News</h2>
                    <p>Latest announcements and updates from our research lab</p>
                </div>

                <!-- Recent News (Always Visible) -->
                <div class="news-container">
                    <div class="news-recent">
{featured_html}
                    </div>

                    <!-- Toggle Button -->
                    <div class="news-toggle-container">
                        <button id="news-toggle-btn" class="btn btn-secondary news-toggle-btn">
                            <i class="fas fa-chevron-down"></i>
                            Show Past Announcements
                        </button>
                    </div>

                    <!-- Past News (Initially Hidden) -->
                    <div id="news-past" class="news-past" style="display: none;">
{past_html}
                    </div>
                </div>
            </div>
        </section>'''

    return news_section_html

def update_index_html_with_news(news_html: str, backup: bool = True) -> bool:
    """Update index.html with new news section while preserving everything else"""
    try:
        # Read current index.html
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()

        # Create backup if requested
        if backup:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f'index_backup_{timestamp}.html'
            with open(f'backups/{backup_filename}', 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Backup created: {backup_filename}")

        # Find news section boundaries
        news_start = content.find('        <!-- News Section -->')
        if news_start == -1:
            print("Error: Could not find news section start marker")
            return False

        # Find end of news section (next section or known boundary)
        news_end = content.find('        <!-- Recent Publications -->', news_start)
        if news_end == -1:
            print("Error: Could not find news section end marker")
            return False

        # Replace news section
        new_content = content[:news_start] + news_html + '\n\n' + content[news_end:]

        # Write updated content
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_content)

        print("Successfully updated news section in index.html")
        return True

    except Exception as e:
        print(f"Error updating index.html: {e}")
        return False

def main():
    """Main function to generate and update news section"""
    print("Generating news section HTML...")

    # Load news data
    news_data = load_news_data()
    if not news_data:
        print("No news data loaded. Exiting.")
        return

    print(f"Loaded {len(news_data)} news items")

    # Generate news section HTML
    news_html = generate_news_section_html(news_data)

    # Create backups directory if it doesn't exist
    import os
    os.makedirs('backups', exist_ok=True)

    # Update index.html
    if update_index_html_with_news(news_html):
        print("News section updated successfully!")

        # Show summary
        featured_count = len([item for item in news_data if item.get('featured', False) and item.get('visible', True)])
        past_count = len([item for item in news_data if not item.get('featured', False) and item.get('visible', True)])
        print(f"  - Featured news items: {featured_count}")
        print(f"  - Past news items: {past_count}")
    else:
        print("Failed to update news section")

if __name__ == "__main__":
    main()