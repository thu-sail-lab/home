#!/usr/bin/env python3
"""
Add News Item Script
Interactive script to add new news items to news.json
"""

import json
import datetime
from typing import Dict, List

ICON_OPTIONS = {
    '1': 'fas fa-trophy',           # Awards
    '2': 'fas fa-graduation-cap',   # Team/Students
    '3': 'fas fa-microscope',       # Grants/Research
    '4': 'fas fa-users',            # Collaborations
    '5': 'fas fa-book-open',        # Publications
    '6': 'fas fa-medal',            # Student awards
    '7': 'fas fa-globe',            # Presentations
    '8': 'fas fa-laptop-code',      # Open source
    '9': 'fas fa-lightbulb',        # General research
    '10': 'fas fa-newspaper'        # General news
}

CATEGORY_OPTIONS = {
    '1': 'award',
    '2': 'team',
    '3': 'grant',
    '4': 'collaboration',
    '5': 'publication',
    '6': 'presentation',
    '7': 'opensource',
    '8': 'other'
}

def load_news_data(file_path: str = 'data/news.json') -> List[Dict]:
    """Load existing news data"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_news_data(news_data: List[Dict], file_path: str = 'data/news.json') -> bool:
    """Save news data to JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving news data: {e}")
        return False

def get_next_news_id(news_data: List[Dict]) -> str:
    """Generate next news ID"""
    if not news_data:
        return "news-001"

    # Extract numbers from existing IDs
    numbers = []
    for item in news_data:
        news_id = item.get('id', '')
        if news_id.startswith('news-'):
            try:
                num = int(news_id.split('-')[1])
                numbers.append(num)
            except (ValueError, IndexError):
                continue

    if numbers:
        next_num = max(numbers) + 1
    else:
        next_num = 1

    return f"news-{next_num:03d}"

def get_user_input():
    """Get news item details from user"""
    print("\n=== Add New News Item ===\n")

    # Get title
    title = input("Enter news title: ").strip()
    if not title:
        print("Title is required!")
        return None

    # Get description
    description = input("Enter news description: ").strip()
    if not description:
        print("Description is required!")
        return None

    # Get date
    print("\nDate (leave empty for today):")
    date_input = input("Enter date (YYYY-MM-DD): ").strip()
    if not date_input:
        date_obj = datetime.date.today()
    else:
        try:
            date_obj = datetime.datetime.strptime(date_input, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format! Using today's date.")
            date_obj = datetime.date.today()

    # Get icon
    print("\nChoose an icon:")
    for key, icon in ICON_OPTIONS.items():
        icon_name = icon.split()[-1]  # Get the last part (e.g., 'trophy' from 'fas fa-trophy')
        print(f"  {key}. {icon_name}")

    icon_choice = input("Select icon (1-10): ").strip()
    icon = ICON_OPTIONS.get(icon_choice, 'fas fa-newspaper')

    # Get category
    print("\nChoose a category:")
    for key, category in CATEGORY_OPTIONS.items():
        print(f"  {key}. {category}")

    category_choice = input("Select category (1-8): ").strip()
    category = CATEGORY_OPTIONS.get(category_choice, 'other')

    # Get visibility settings
    print("\nVisibility settings:")
    featured_input = input("Make this a featured news item? (y/n): ").strip().lower()
    featured = featured_input in ['y', 'yes', '1', 'true']

    visible_input = input("Make this news item visible? (y/n, default: y): ").strip().lower()
    visible = visible_input not in ['n', 'no', '0', 'false'] if visible_input else True

    # Create news item
    news_item = {
        "id": "",  # Will be set later
        "date": date_obj.strftime('%Y-%m-%d'),
        "month": date_obj.strftime('%b'),
        "day": str(date_obj.day),
        "year": str(date_obj.year),
        "icon": icon,
        "category": category,
        "title": title,
        "description": description,
        "visible": visible,
        "featured": featured
    }

    return news_item

def preview_news_item(news_item: Dict):
    """Preview the news item"""
    print("\n=== Preview ===")
    print(f"Title: {news_item['title']}")
    print(f"Description: {news_item['description']}")
    print(f"Date: {news_item['month']} {news_item['day']}, {news_item['year']}")
    print(f"Icon: {news_item['icon']}")
    print(f"Category: {news_item['category']}")
    print(f"Featured: {'Yes' if news_item['featured'] else 'No'}")
    print(f"Visible: {'Yes' if news_item['visible'] else 'No'}")

def main():
    """Main function"""
    print("SAIL Lab News Management System")
    print("================================")

    # Load existing news
    news_data = load_news_data()
    print(f"Loaded {len(news_data)} existing news items")

    # Get new news item details
    news_item = get_user_input()
    if not news_item:
        print("Failed to get news item details. Exiting.")
        return

    # Set ID
    news_item['id'] = get_next_news_id(news_data)

    # Preview
    preview_news_item(news_item)

    # Confirm
    confirm = input("\nAdd this news item? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes', '1']:
        print("News item not added.")
        return

    # Add to news data (at the beginning for chronological order)
    news_data.insert(0, news_item)

    # Save
    if save_news_data(news_data):
        print(f"\n✓ News item added successfully! (ID: {news_item['id']})")
        print(f"✓ Total news items: {len(news_data)}")
        print("\nNext steps:")
        print("1. Run: python scripts/generate_news_html.py")
        print("2. Review the updated index.html")
        print("3. Commit changes to git")
    else:
        print("✗ Failed to save news item")

if __name__ == "__main__":
    main()