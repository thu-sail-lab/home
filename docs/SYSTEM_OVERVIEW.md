# 🏗️ SAIL Lab Website Automation System

This document provides a technical overview of the automated content management system for the SAIL lab website.

## 🎯 System Goals

- **Preserve Design**: Maintain exact current website design and styling
- **Automate Content**: Eliminate manual HTML editing for publications and news
- **Ensure Reliability**: Provide backups, error handling, and rollback capabilities
- **Enable Scalability**: Support growing research output without maintenance overhead
- **Maintain Quality**: Automated categorization and validation

## 🏛️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   Processing    │    │   Website       │
│                 │    │                 │    │                 │
│ Google Scholar  │───▶│ Python Scripts │───▶│ Static HTML     │
│ Manual Input    │    │ JSON Data       │    │ CSS/JS          │
│ News Entries    │    │ HTML Generation │    │ GitHub Pages    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
                               ▼
                      ┌─────────────────┐
                      │   Backups &     │
                      │   Validation    │
                      └─────────────────┘
```

## 📁 File Structure

```
SAIL-Lab-Website/
├── data/
│   ├── news.json              # News items data
│   ├── publications.json      # Publications database
│   └── scholar_config.json    # Google Scholar settings
├── scripts/
│   ├── add_news.py           # Interactive news addition
│   ├── generate_news_html.py # News HTML generator
│   ├── fetch_scholar_publications.py  # Google Scholar fetcher
│   ├── auto_process_publications.py   # Publications processor
│   └── update_publications.py         # Master update script
├── docs/
│   ├── NEWS_MANAGEMENT.md     # News management guide
│   ├── PUBLICATIONS_MANAGEMENT.md  # Publications guide
│   └── SYSTEM_OVERVIEW.md     # This document
├── backups/
│   ├── index_backup_*.html    # HTML backups
│   ├── publications_backup_*.json  # Data backups
│   └── news_backup_*.json     # News backups
├── index.html                 # Main website file
├── process_publications_updated.py  # Original processor
└── [other website files]
```

## 🔧 Component Details

### Data Layer

#### `data/news.json`
- Structured storage for news items
- Supports categorization, visibility controls, and featured items
- JSON format for easy parsing and editing

#### `data/publications.json`
- Research publications database
- Fetched from Google Scholar and manually curated
- Includes titles, authors, venues, citations, abstracts

#### `data/scholar_config.json`
- Configuration for Google Scholar automation
- Author information, update frequency, proxy settings
- System preferences and filters

### Processing Layer

#### News Processing
- **add_news.py**: Interactive CLI for adding news items
- **generate_news_html.py**: Converts JSON to HTML matching current design
- Preserves exact styling and layout structure

#### Publications Processing
- **fetch_scholar_publications.py**: Google Scholar integration
- **auto_process_publications.py**: Enhanced HTML generation
- **update_publications.py**: Orchestrates complete update workflow
- Uses existing categorization logic from `process_publications_updated.py`

### Safety Layer

#### Automatic Backups
- HTML backups before any updates
- JSON data backups with timestamps
- Stored in `backups/` directory with date/time stamps

#### Validation
- JSON syntax validation
- Required field checking
- Error handling with rollback capability

## 🚀 Workflows

### News Management Workflow

```
1. Content Creation
   ├── Interactive: python scripts/add_news.py
   └── Manual: Edit data/news.json directly

2. HTML Generation
   └── python scripts/generate_news_html.py
       ├── Creates backup
       ├── Generates HTML matching current design
       └── Updates index.html

3. Verification
   ├── Review changes in index.html
   ├── Test website locally
   └── Commit to git
```

### Publications Update Workflow

```
1. Data Fetching
   └── python scripts/fetch_scholar_publications.py
       ├── Connects to Google Scholar
       ├── Fetches new publications
       ├── Merges with existing data
       └── Creates backup

2. HTML Processing
   └── python scripts/auto_process_publications.py
       ├── Categorizes publications by topic
       ├── Groups by year and venue type
       ├── Generates filter buttons
       └── Updates index.html with exact styling

3. Complete Automation
   └── python scripts/update_publications.py
       ├── Orchestrates full workflow
       ├── Provides options for partial updates
       └── Updates configuration timestamps
```

## 🔄 Automation Schedule

### Recommended Schedule

- **Daily**: Automated publication check (optional)
- **Weekly**: Full publication update from Google Scholar
- **As-needed**: News updates when announcements are made
- **Monthly**: Review and cleanup old backups

### Implementation Options

#### Cron Job (Linux/Mac)
```bash
# Weekly publication update (Sundays at 2 AM)
0 2 * * 0 cd /path/to/website && python scripts/update_publications.py
```

#### GitHub Actions
```yaml
# .github/workflows/update-publications.yml
name: Update Publications
on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday at 2 AM
  workflow_dispatch:     # Manual trigger
```

#### Manual Execution
```bash
# Run when needed
python scripts/update_publications.py
```

## 🛡️ Safety and Reliability

### Backup Strategy
- **Automatic**: Created before every update
- **Timestamped**: Easy to identify and restore
- **Comprehensive**: Includes both data and HTML files
- **Retention**: Configurable cleanup of old backups

### Error Handling
- **Graceful Degradation**: Continues processing despite individual failures
- **Detailed Logging**: Clear error messages for debugging
- **Rollback Capability**: Easy restoration from backups
- **Validation**: Input checking and format validation

### Quality Assurance
- **Design Preservation**: Generated HTML matches original exactly
- **Content Validation**: Required fields, proper formatting
- **Link Checking**: Validates publication URLs
- **Statistics Generation**: Monitors data quality

## 🔧 Customization Points

### Topic Categories
Edit `TOPICS` dictionary in `process_publications_updated.py`:
```python
TOPICS = {
    'your-topic': ['keyword1', 'keyword2', 'keyword3'],
    # ... other topics
}
```

### News Categories
Modify category options in `scripts/add_news.py`:
```python
CATEGORY_OPTIONS = {
    '1': 'your-category',
    # ... other categories
}
```

### HTML Templates
- News HTML structure in `generate_news_html.py`
- Publications HTML in `auto_process_publications.py`
- Both preserve current styling exactly

### Google Scholar Settings
Configure in `data/scholar_config.json`:
- Author identification
- Proxy settings
- Update frequency
- Content filters

## 📊 Monitoring and Analytics

### System Health
- Check `last_update` timestamp in `scholar_config.json`
- Monitor backup file creation
- Review error logs from script execution

### Content Quality
- Publication count trends
- Citation statistics
- Topic distribution
- Missing or incomplete data

### Performance Metrics
- Update success rate
- Processing time
- Error frequency
- Backup storage usage

## 🚨 Troubleshooting

### Common Issues

**Scripts not running:**
- Check Python version (3.6+ required)
- Install required packages: `pip install scholarly`
- Verify file permissions

**Google Scholar issues:**
- Enable proxy in configuration
- Increase delay between requests
- Check if profile is public

**HTML not updating:**
- Check backup creation
- Verify JSON syntax
- Review error messages

**Design changes:**
- Generated HTML should match original exactly
- If styling breaks, restore from backup
- Check for template modifications

### Recovery Procedures

**Data corruption:**
```bash
# Restore publications data
cp backups/publications_backup_LATEST.json publications.json

# Restore HTML
cp backups/index_backup_LATEST.html index.html
```

**System reset:**
```bash
# Clean restart
git checkout HEAD -- index.html publications.json
python scripts/auto_process_publications.py
```

## 🔮 Future Enhancements

### Planned Features
- RSS feed generation for news
- Social media integration
- Email notifications for updates
- Advanced analytics dashboard

### Extensibility
- Plugin architecture for new data sources
- Template system for different layouts
- API endpoints for external integrations
- Mobile app connectivity

### Scaling Considerations
- Database migration for larger datasets
- CDN integration for media files
- Caching strategies for better performance
- Multi-language support

---

**For support**: Review error messages, check backups, and refer to individual component documentation.