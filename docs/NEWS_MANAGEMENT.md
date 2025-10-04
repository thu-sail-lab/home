# 📰 News Management Guide

This guide explains how to add, edit, and manage news items for the SAIL lab website.

## 🎯 Quick Start

### Adding a New News Item

1. **Easy Way (Recommended)**:
   ```bash
   python scripts/add_news.py
   ```
   Follow the interactive prompts to add your news item.

2. **Manual Way**:
   - Edit `data/news.json` directly
   - Follow the structure shown below
   - Run `python scripts/generate_news_html.py` to update the website

3. **Update the Website**:
   ```bash
   python scripts/generate_news_html.py
   ```

## 📋 News Item Structure

Each news item in `data/news.json` has the following structure:

```json
{
  "id": "news-001",
  "date": "2025-01-15",
  "month": "Jan",
  "day": "15",
  "year": "2025",
  "icon": "fas fa-trophy",
  "category": "award",
  "title": "Your News Title",
  "description": "Brief description of the news.",
  "visible": true,
  "featured": true
}
```

### Field Descriptions

| Field | Description | Example | Required |
|-------|-------------|---------|----------|
| `id` | Unique identifier | `"news-001"` | ✅ |
| `date` | Full date in YYYY-MM-DD format | `"2025-01-15"` | ✅ |
| `month` | Three-letter month abbreviation | `"Jan"` | ✅ |
| `day` | Day of month | `"15"` | ✅ |
| `year` | Full year | `"2025"` | ✅ |
| `icon` | FontAwesome icon class | `"fas fa-trophy"` | ✅ |
| `category` | News category | `"award"` | ✅ |
| `title` | News headline | `"Best Paper Award"` | ✅ |
| `description` | Brief description | `"Our paper won..."` | ✅ |
| `visible` | Whether to show the item | `true` | ✅ |
| `featured` | Show in main section | `true` | ✅ |

## 🎨 Available Icons

Choose from these commonly used icons:

| Icon Class | Visual | Best For |
|------------|--------|----------|
| `fas fa-trophy` | 🏆 | Awards, achievements |
| `fas fa-graduation-cap` | 🎓 | New team members, graduations |
| `fas fa-microscope` | 🔬 | Research grants, new research |
| `fas fa-users` | 👥 | Collaborations, partnerships |
| `fas fa-book-open` | 📖 | Publications, papers |
| `fas fa-medal` | 🏅 | Student awards, honors |
| `fas fa-globe` | 🌍 | Presentations, conferences |
| `fas fa-laptop-code` | 💻 | Open source, software releases |
| `fas fa-lightbulb` | 💡 | General research news |
| `fas fa-newspaper` | 📰 | General announcements |

## 📂 Categories

Available categories for news items:

- `award` - Awards and honors
- `team` - Team updates (new members, etc.)
- `grant` - Research grants and funding
- `collaboration` - Industry partnerships
- `publication` - Research publications
- `presentation` - Conference presentations
- `opensource` - Open source releases
- `other` - General announcements

## 🎛️ Visibility Settings

### `featured` (true/false)
- `true`: Shows in the main "Recent News" section (always visible)
- `false`: Shows in the "Past Announcements" section (hidden by default)

### `visible` (true/false)
- `true`: News item appears on the website
- `false`: News item is hidden (useful for drafts or archived items)

## 📝 Examples

### Award Announcement
```json
{
  "id": "news-009",
  "date": "2025-01-15",
  "month": "Jan",
  "day": "15",
  "year": "2025",
  "icon": "fas fa-trophy",
  "category": "award",
  "title": "Best Paper Award at AAAI 2025",
  "description": "Our paper on multi-agent causal discovery received the Best Paper Award.",
  "visible": true,
  "featured": true
}
```

### New Team Member
```json
{
  "id": "news-010",
  "date": "2024-12-20",
  "month": "Dec",
  "day": "20",
  "year": "2024",
  "icon": "fas fa-graduation-cap",
  "category": "team",
  "title": "Welcome New PhD Student",
  "description": "Jane Doe joins our lab to work on deep learning for time series analysis.",
  "visible": true,
  "featured": true
}
```

### Grant Announcement
```json
{
  "id": "news-011",
  "date": "2024-11-28",
  "month": "Nov",
  "day": "28",
  "year": "2024",
  "icon": "fas fa-microscope",
  "category": "grant",
  "title": "NSF Grant Awarded",
  "description": "Received $2.5M NSF grant for explainable AI research.",
  "visible": true,
  "featured": true
}
```

## 🛠️ Advanced Management

### Managing Featured News
- Keep 5-7 items as `featured: true` for the main section
- Older items should be set to `featured: false` to move them to "Past Announcements"

### Archiving Old News
- Set `visible: false` for very old news items
- Keep them in the file for historical records
- They won't appear on the website

### Backup and Safety
- The system automatically creates backups before updates
- Backups are stored in the `backups/` folder
- Always test changes locally before committing

## 🚀 Automation (Future)

The news system is designed to support future automation:
- RSS feed generation
- Social media posting
- Email notifications
- Scheduled publication

## 🆘 Troubleshooting

### Common Issues

**News not appearing:**
- Check `visible: true` and run `generate_news_html.py`
- Verify JSON syntax is correct

**Wrong order:**
- News items are ordered by date automatically
- Ensure date format is correct (YYYY-MM-DD)

**Styling issues:**
- Don't modify the HTML structure in generated files
- All styling is preserved from the original design

**Script errors:**
- Ensure Python 3.6+ is installed
- Check that all files are in the correct locations

### Getting Help

1. Check the JSON syntax in `data/news.json`
2. Run `python scripts/add_news.py` for guided input
3. Review error messages carefully
4. Check the `backups/` folder if you need to restore

## 📁 File Structure

```
data/
  └── news.json              # News data storage
scripts/
  ├── add_news.py           # Interactive news addition
  └── generate_news_html.py # HTML generation
docs/
  └── NEWS_MANAGEMENT.md    # This guide
backups/
  └── [automatic backups]   # Safety backups
```

---

**Need help?** Check the examples above or run `python scripts/add_news.py` for an interactive guide.