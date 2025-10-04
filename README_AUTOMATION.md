# 🚀 SAIL Lab Website Automation System

An automated content management system for the SAIL research lab website that preserves your existing design while making content updates effortless.

## ✨ What's New

This system transforms your static website into a semi-automated platform where you can:

- **📰 Manage News**: Add news items via simple commands instead of editing HTML
- **📚 Auto-Update Publications**: Sync with Google Scholar automatically
- **🎨 Preserve Design**: Keep your exact current styling and layout
- **🔄 Easy Updates**: Simple commands for all operations
- **🛡️ Safety First**: Automatic backups and rollback capability

## 🎯 Quick Start

### Add a News Item
```bash
npm run add-news
```

### Update Publications from Google Scholar
```bash
npm run update-publications
```

### Check System Status
```bash
npm run status
```

### Get Help
```bash
npm run help
```

## 📦 Installation

1. **Install Python Dependencies**:
   ```bash
   npm run install-deps
   # or manually: pip install scholarly
   ```

2. **Configure Google Scholar** (Optional):
   - Edit `data/scholar_config.json`
   - Set your author name and affiliation

3. **Validate System**:
   ```bash
   npm run validate
   ```

## 🛠️ Available Commands

| Command | Description |
|---------|-------------|
| `npm run add-news` | Add a new news item interactively |
| `npm run update-news` | Generate news HTML from data |
| `npm run update-publications` | Full publication update (Scholar + HTML) |
| `npm run fetch-publications` | Fetch from Google Scholar only |
| `npm run process-publications` | Generate HTML from existing data |
| `npm run preview` | Start local web server |
| `npm run status` | Show system status and statistics |
| `npm run validate` | Validate all data files |
| `npm run backup` | Create manual backup |
| `npm run help` | Show detailed help |

## 📁 Project Structure

```
├── data/
│   ├── news.json              # News items data
│   ├── publications.json      # Publications database
│   └── scholar_config.json    # Google Scholar settings
├── scripts/
│   ├── add_news.py           # Interactive news addition
│   ├── generate_news_html.py # News HTML generator
│   ├── fetch_scholar_publications.py  # Google Scholar fetcher
│   ├── auto_process_publications.py   # Publications processor
│   ├── update_publications.py         # Master update script
│   └── [utility scripts]
├── docs/
│   ├── NEWS_MANAGEMENT.md     # How to manage news
│   ├── PUBLICATIONS_MANAGEMENT.md  # How to manage publications
│   └── SYSTEM_OVERVIEW.md     # Technical overview
├── backups/                   # Automatic backups
├── index.html                 # Your website (updated automatically)
└── package.json              # NPM commands
```

## 📰 News Management

### Quick Add
```bash
npm run add-news
```
Follow the interactive prompts to add news items.

### Manual Edit
1. Edit `data/news.json`
2. Run `npm run update-news`

### News Structure
```json
{
  "id": "news-001",
  "date": "2025-01-15",
  "title": "Best Paper Award at AAAI 2025",
  "description": "Our paper received the Best Paper Award.",
  "icon": "fas fa-trophy",
  "category": "award",
  "featured": true,
  "visible": true
}
```

## 📚 Publications Management

### Automated Updates
```bash
npm run update-publications
```

### Configuration
Edit `data/scholar_config.json`:
```json
{
  "author_name": "Your Name",
  "affiliation": "Your University",
  "settings": {
    "use_proxy": true,
    "delay_between_requests": 2
  }
}
```

### Manual Publications
1. Edit `publications.json` directly
2. Run `npm run process-publications`

## 🛡️ Safety Features

### Automatic Backups
- Created before every update
- Stored in `backups/` with timestamps
- Includes both data and HTML files

### Validation
```bash
npm run validate
```
Checks all data files for integrity.

### Rollback
```bash
# Restore from backup if needed
cp backups/index_backup_YYYYMMDD_HHMMSS.html index.html
```

## 📊 System Status

Check system health:
```bash
npm run status
```

Shows:
- Data file status
- Publication statistics
- News item counts
- Last update times
- Backup information

## 🎨 Design Preservation

The system **preserves your exact current design**:
- ✅ Same HTML structure
- ✅ Same CSS classes
- ✅ Same styling and layout
- ✅ Same JavaScript functionality

## 🔄 Automation Schedule

### Recommended Schedule
- **Weekly**: `npm run update-publications`
- **As-needed**: `npm run add-news`
- **Monthly**: Review and cleanup

### Advanced: Automated Scheduling
Set up cron jobs or GitHub Actions for hands-off operation.

## 📖 Documentation

Detailed guides available in `docs/`:

- **[News Management](docs/NEWS_MANAGEMENT.md)**: Complete news system guide
- **[Publications Management](docs/PUBLICATIONS_MANAGEMENT.md)**: Publications automation guide
- **[System Overview](docs/SYSTEM_OVERVIEW.md)**: Technical architecture details

## 🆘 Troubleshooting

### Common Issues

**Google Scholar Rate Limiting:**
- Enable proxy in `data/scholar_config.json`
- Increase delay between requests

**HTML Not Updating:**
- Run `npm run validate` to check data integrity
- Check error messages in terminal

**Missing Publications:**
- Verify author name in config
- Check Google Scholar profile is public

### Getting Help

1. Run `npm run status` to check system health
2. Run `npm run validate` to check data integrity
3. Check documentation in `docs/` folder
4. Review error messages for specific issues

## 🔮 Future Enhancements

Planned features:
- RSS feed generation
- Social media integration
- Email notifications
- Advanced analytics
- Multi-language support

## 📝 Contributing

To extend the system:
1. Follow existing code patterns
2. Update documentation
3. Add validation for new features
4. Maintain design preservation

## 📄 License

MIT License - Feel free to adapt for your research group.

---

## 🎉 Success!

Your SAIL Lab website now features:
- ✅ Automated Google Scholar publication sync
- ✅ Easy news management
- ✅ Preserved custom design
- ✅ Comprehensive documentation
- ✅ Safety and backup systems
- ✅ Simple command-line interface

**Next Steps:**
1. Run `npm run status` to see your current setup
2. Try `npm run add-news` to add a news item
3. Test `npm run update-publications` for publication sync
4. Explore the documentation in `docs/`

*Happy researching! 🔬🎓*