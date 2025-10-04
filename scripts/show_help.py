#!/usr/bin/env python3
"""
Help System - Shows available commands and usage information
"""

def show_help():
    """Display help information for the SAIL Lab website system"""

    print("🚀 SAIL Lab Website Management System")
    print("=" * 50)
    print()

    print("📰 NEWS MANAGEMENT")
    print("  npm run add-news         Add a new news item interactively")
    print("  npm run update-news      Generate news HTML from data/news.json")
    print()

    print("📚 PUBLICATIONS MANAGEMENT")
    print("  npm run update-publications    Full update: fetch + process HTML")
    print("  npm run fetch-publications     Fetch new publications from Google Scholar")
    print("  npm run process-publications   Generate HTML from publications.json")
    print()

    print("🛠️  UTILITIES")
    print("  npm run preview           Start local web server (http://localhost:8000)")
    print("  npm run backup            Create manual backup of all data")
    print("  npm run status            Check system status and statistics")
    print("  npm run validate          Validate all JSON data files")
    print("  npm run install-deps      Install Python dependencies")
    print("  npm run help              Show this help message")
    print()

    print("📖 DOCUMENTATION")
    print("  docs/NEWS_MANAGEMENT.md        How to manage news items")
    print("  docs/PUBLICATIONS_MANAGEMENT.md How to manage publications")
    print("  docs/SYSTEM_OVERVIEW.md        Technical system overview")
    print()

    print("🎯 QUICK START")
    print("  1. Add news:        npm run add-news")
    print("  2. Update pubs:     npm run update-publications")
    print("  3. Preview site:    npm run preview")
    print("  4. Check status:    npm run status")
    print()

    print("🆘 TROUBLESHOOTING")
    print("  • Check docs/ folder for detailed guides")
    print("  • Backups are automatically created in backups/")
    print("  • Run 'npm run validate' to check data integrity")
    print("  • Use 'npm run status' to see system health")
    print()

    print("📁 IMPORTANT FILES")
    print("  data/news.json           News items data")
    print("  data/publications.json   Publications database")
    print("  data/scholar_config.json Google Scholar settings")
    print("  index.html               Main website file")
    print()

if __name__ == "__main__":
    show_help()