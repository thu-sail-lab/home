# 📚 Publications Management Guide

This guide explains how to manage and automate publications for the SAIL lab website.

## 🎯 Quick Start

### Automated Update (Recommended)
```bash
python scripts/update_publications.py
```
Choose option 1 for a complete update (fetch from Google Scholar + update HTML).

### Manual Update
```bash
# Option 1: Full automation
python scripts/fetch_scholar_publications.py  # Fetch from Google Scholar
python scripts/auto_process_publications.py   # Generate HTML

# Option 2: Update HTML only (if publications.json already updated)
python scripts/auto_process_publications.py
```

## 🤖 Automation Features

### Google Scholar Integration
- Automatically fetches publications from professor's Google Scholar profile
- Merges with existing publications (no duplicates)
- Enriches data with abstracts, citations, and venue information
- Preserves manual edits and custom categorizations

### Smart Processing
- Automatic topic categorization (LLMs, Deep Learning, Time Series, etc.)
- Venue type detection (IEEE, Journals, Conferences)
- Publication year grouping
- Citation count tracking

### Safety Features
- Automatic backups before any changes
- Rollback capability
- Validation and error checking
- Preserves exact website design and styling

## 📁 File Structure

```
data/
  ├── scholar_config.json    # Google Scholar settings
  └── publications.json      # Publications database
scripts/
  ├── fetch_scholar_publications.py  # Google Scholar fetcher
  ├── auto_process_publications.py   # HTML generator
  └── update_publications.py         # Master orchestrator
backups/
  ├── publications_backup_*.json     # Data backups
  └── index_backup_*.html           # HTML backups
```

## ⚙️ Configuration

### Google Scholar Settings (`data/scholar_config.json`)

```json
{
  "author_name": "Chen Zhang",
  "affiliation": "Tsinghua University",
  "google_scholar_id": "",
  "backup_enabled": true,
  "max_publications": 100,
  "update_frequency": "weekly",
  "settings": {
    "use_proxy": true,
    "delay_between_requests": 2,
    "retry_attempts": 3,
    "include_citations": true,
    "include_abstracts": true
  }
}
```

#### Key Settings:
- **author_name**: Full name as it appears on Google Scholar
- **affiliation**: University/organization name
- **use_proxy**: Recommended to avoid rate limiting
- **delay_between_requests**: Seconds between requests (2-5 recommended)

## 📊 Publication Data Structure

Each publication in `publications.json` follows this structure:

```json
{
  "title": "Paper Title",
  "authors": "Author1, Author2, Author3",
  "venue": "Conference/Journal Name",
  "year": 2024,
  "citations": 42,
  "url": "https://paper-url.com",
  "eprint_url": "https://arxiv.org/...",
  "abstract": "Paper abstract text..."
}
```

## 🏷️ Topic Categorization

The system automatically categorizes publications into topics:

### Research Areas
- **LLMs**: Large Language Models, GPT, BERT, NLP
- **Deep Learning**: Neural networks, CNN, RNN, Transformers
- **Machine Learning**: Classification, clustering, supervised learning
- **Reinforcement Learning**: Q-learning, multi-armed bandits
- **Time Series**: Forecasting, temporal analysis, sequential data
- **Anomaly Detection**: Outlier detection, monitoring, fault detection
- **Causal Inference**: DAG, causal discovery, interventions
- **Bayesian Methods**: Probabilistic models, MCMC
- **Tensor Methods**: Tensor decomposition, factorization
- **Functional Data**: Profile analysis, FDA

### Application Areas
- **Transportation**: Metro, traffic, urban mobility
- **Manufacturing**: Industrial systems, quality control
- **Medical AI**: Healthcare, diagnosis, clinical applications

### Methods
- **Statistical Modeling**: Regression, hypothesis testing
- **Optimization**: Bilevel optimization, constraints
- **Graph Learning**: Networks, community detection

## 🛠️ Manual Management

### Adding Publications Manually

1. **Edit publications.json directly**:
   ```json
   {
     "title": "Your Paper Title",
     "authors": "Your Name, Co-author Name",
     "venue": "Conference Name",
     "year": 2024,
     "citations": 0,
     "url": "https://paper-url.com",
     "eprint_url": "",
     "abstract": "Your abstract here..."
   }
   ```

2. **Update the website**:
   ```bash
   python scripts/auto_process_publications.py
   ```

### Editing Existing Publications

1. Find the publication in `publications.json`
2. Edit the relevant fields
3. Run the processing script to update HTML
4. Manual edits will be preserved during automatic updates

### Managing Categories

Categories are assigned automatically based on title and abstract content. To override:

1. The categorization happens in `process_publications_updated.py`
2. Edit the `TOPICS` dictionary to modify keyword mappings
3. Categories include venue type (ieee, journals, conferences) and research topics

## 🔄 Update Workflows

### Daily/Weekly Automated Updates

Set up a scheduled task to run:
```bash
python scripts/update_publications.py
```

This will:
1. Check Google Scholar for new publications
2. Merge with existing database
3. Update HTML with new publications
4. Create backups automatically

### Before Important Deadlines

Manually run a full update:
```bash
python scripts/fetch_scholar_publications.py
python scripts/auto_process_publications.py
```

### After Manual Edits

Just update the HTML:
```bash
python scripts/auto_process_publications.py
```

## 🚨 Troubleshooting

### Common Issues

**Google Scholar Rate Limiting:**
- Enable proxy in config: `"use_proxy": true`
- Increase delay: `"delay_between_requests": 5`
- Run during off-peak hours

**Missing Publications:**
- Check author name and affiliation in config
- Verify Google Scholar profile is public
- Some very recent publications may not appear immediately

**Categorization Issues:**
- Edit `TOPICS` dictionary in `process_publications_updated.py`
- Add specific keywords for your research areas
- Categories are based on title and abstract content

**HTML Generation Errors:**
- Check `publications.json` syntax
- Ensure all required fields are present
- Look for special characters that need escaping

### Error Recovery

**If automation fails:**
1. Check error messages for specific issues
2. Restore from backup if needed:
   ```bash
   cp backups/publications_backup_YYYYMMDD_HHMMSS.json publications.json
   ```
3. Run manual processing to verify

**If HTML is corrupted:**
1. Restore from HTML backup:
   ```bash
   cp backups/index_backup_YYYYMMDD_HHMMSS.html index.html
   ```
2. Re-run the processing script

## 🔮 Advanced Features

### Custom Filters

Add new publication filters by:
1. Adding data attributes in `generate_publication_html()`
2. Creating filter buttons in the HTML template
3. Adding JavaScript handlers (if needed)

### Integration with Other Systems

The JSON-based approach allows easy integration with:
- Academic database APIs
- Institutional repositories
- Citation management systems
- Social media automation

### Bulk Operations

For large-scale updates:
```python
# Example: Update all citations
import json

with open('publications.json', 'r') as f:
    pubs = json.load(f)

# Process publications...

with open('publications.json', 'w') as f:
    json.dump(pubs, f, indent=2)
```

## 📈 Analytics and Monitoring

### Publication Statistics

The system automatically generates:
- Total publication count
- Total citation count
- Publications by venue type (IEEE, journals, conferences)
- Publications by research topic
- Publications by year

### Performance Monitoring

Track automation success:
- Check `data/scholar_config.json` for `last_update` timestamp
- Monitor backup files for system health
- Review generated statistics for data quality

## 🔄 Maintenance Schedule

### Weekly
- Run automated update to catch new publications
- Review generated statistics
- Check for any categorization issues

### Monthly
- Review and clean up old backup files
- Update Google Scholar configuration if needed
- Verify all publication links are working

### Quarterly
- Review topic categorization accuracy
- Update keyword mappings in `TOPICS` dictionary
- Audit for any missing publications

---

**Need help?** Check the error messages, review backups, or run the scripts step-by-step to identify issues.