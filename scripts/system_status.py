#!/usr/bin/env python3
"""
System Status - Shows current status of the website management system
"""

import json
import os
from datetime import datetime
from typing import Dict, Any

def load_json_safe(file_path: str) -> Dict[str, Any]:
    """Safely load JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def check_file_status(file_path: str) -> Dict[str, Any]:
    """Check file existence and modification time"""
    if os.path.exists(file_path):
        stat = os.stat(file_path)
        return {
            'exists': True,
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        return {'exists': False}

def get_backup_info() -> Dict[str, Any]:
    """Get information about backup files"""
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        return {'count': 0, 'latest': None}

    try:
        backup_files = [f for f in os.listdir(backup_dir) if f.endswith(('.json', '.html'))]
        backup_files.sort(key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)), reverse=True)

        latest_backup = None
        if backup_files:
            latest_file = backup_files[0]
            latest_backup = {
                'file': latest_file,
                'time': datetime.fromtimestamp(
                    os.path.getmtime(os.path.join(backup_dir, latest_file))
                ).strftime('%Y-%m-%d %H:%M:%S')
            }

        return {
            'count': len(backup_files),
            'latest': latest_backup
        }
    except Exception:
        return {'count': 0, 'latest': None}

def show_status():
    """Display comprehensive system status"""

    print("📊 SAIL Lab Website System Status")
    print("=" * 40)
    print(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Check main data files
    print("📁 DATA FILES")
    files_to_check = [
        ('News Data', 'data/news.json'),
        ('Publications', 'publications.json'),
        ('Scholar Config', 'data/scholar_config.json'),
        ('Main Website', 'index.html')
    ]

    for name, path in files_to_check:
        status = check_file_status(path)
        if status['exists']:
            size_kb = status['size'] / 1024
            print(f"  ✅ {name:<15} {size_kb:>6.1f}KB  Modified: {status['modified']}")
        else:
            print(f"  ❌ {name:<15} File not found")

    print()

    # News statistics
    print("📰 NEWS STATISTICS")
    news_data = load_json_safe('data/news.json')
    if news_data:
        total_news = len(news_data)
        featured_news = sum(1 for item in news_data if item.get('featured', False))
        visible_news = sum(1 for item in news_data if item.get('visible', True))
        categories = {}
        for item in news_data:
            cat = item.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1

        print(f"  Total news items: {total_news}")
        print(f"  Featured (visible): {featured_news}")
        print(f"  Public items: {visible_news}")
        print(f"  Categories: {', '.join(f'{k}({v})' for k, v in categories.items())}")
    else:
        print("  ❌ No news data found")

    print()

    # Publications statistics
    print("📚 PUBLICATIONS STATISTICS")
    pub_data = load_json_safe('publications.json')
    if pub_data:
        total_pubs = len(pub_data)
        total_citations = sum(pub.get('citations', 0) for pub in pub_data)
        years = {}
        venues = set()

        for pub in pub_data:
            year = pub.get('year', 'Unknown')
            years[year] = years.get(year, 0) + 1
            venue = pub.get('venue', '')
            if venue and venue != 'Unknown Venue':
                venues.add(venue)

        recent_years = {k: v for k, v in years.items() if isinstance(k, int) and k >= 2020}

        print(f"  Total publications: {total_pubs}")
        print(f"  Total citations: {total_citations}")
        print(f"  Unique venues: {len(venues)}")
        print(f"  Recent years: {', '.join(f'{k}({v})' for k, v in sorted(recent_years.items(), reverse=True))}")

        if total_pubs > 0:
            avg_citations = total_citations / total_pubs
            print(f"  Average citations: {avg_citations:.1f}")
    else:
        print("  ❌ No publications data found")

    print()

    # Google Scholar configuration
    print("🎓 GOOGLE SCHOLAR CONFIG")
    scholar_config = load_json_safe('data/scholar_config.json')
    if scholar_config:
        author = scholar_config.get('author_name', 'Not set')
        affiliation = scholar_config.get('affiliation', 'Not set')
        last_update = scholar_config.get('last_update', 'Never')

        print(f"  Author: {author}")
        print(f"  Affiliation: {affiliation}")
        print(f"  Last update: {last_update}")

        settings = scholar_config.get('settings', {})
        if settings:
            use_proxy = settings.get('use_proxy', False)
            delay = settings.get('delay_between_requests', 'Not set')
            print(f"  Proxy enabled: {'Yes' if use_proxy else 'No'}")
            print(f"  Request delay: {delay}s")
    else:
        print("  ❌ No configuration found")

    print()

    # Backup information
    print("💾 BACKUP STATUS")
    backup_info = get_backup_info()
    print(f"  Total backups: {backup_info['count']}")
    if backup_info['latest']:
        print(f"  Latest backup: {backup_info['latest']['file']}")
        print(f"  Created: {backup_info['latest']['time']}")
    else:
        print("  No backups found")

    print()

    # System health
    print("🏥 SYSTEM HEALTH")
    issues = []

    # Check for required files
    required_files = ['data/news.json', 'publications.json', 'index.html']
    for file in required_files:
        if not os.path.exists(file):
            issues.append(f"Missing required file: {file}")

    # Check JSON syntax
    for file, name in [('data/news.json', 'news'), ('publications.json', 'publications')]:
        try:
            with open(file, 'r') as f:
                json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            issues.append(f"Invalid JSON in {name} file")

    # Check if backups are recent (within 7 days)
    if backup_info['latest']:
        try:
            backup_time = datetime.strptime(backup_info['latest']['time'], '%Y-%m-%d %H:%M:%S')
            days_since_backup = (datetime.now() - backup_time).days
            if days_since_backup > 7:
                issues.append(f"Last backup is {days_since_backup} days old")
        except ValueError:
            pass

    if not issues:
        print("  ✅ All systems operational")
    else:
        for issue in issues:
            print(f"  ⚠️  {issue}")

    print()

    # Quick actions
    print("🔧 QUICK ACTIONS")
    print("  Add news:           npm run add-news")
    print("  Update publications: npm run update-publications")
    print("  Create backup:      npm run backup")
    print("  View help:          npm run help")

if __name__ == "__main__":
    show_status()