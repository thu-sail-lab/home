#!/usr/bin/env python3
"""
Data Validation - Validates JSON data files and system integrity
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

class DataValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate_json_file(self, file_path: str, required_fields: List[str] = None) -> bool:
        """Validate JSON file syntax and structure"""
        if not os.path.exists(file_path):
            self.errors.append(f"File not found: {file_path}")
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # For array files, check each item
            if isinstance(data, list):
                for i, item in enumerate(data):
                    if required_fields:
                        for field in required_fields:
                            if field not in item:
                                self.errors.append(f"{file_path}[{i}]: Missing required field '{field}'")

            print(f"✅ {file_path}: Valid JSON")
            return True

        except json.JSONDecodeError as e:
            self.errors.append(f"{file_path}: Invalid JSON - {e}")
            return False

    def validate_news_data(self) -> bool:
        """Validate news.json structure and content"""
        print("\n📰 Validating news data...")

        required_fields = ['id', 'date', 'month', 'day', 'year', 'icon', 'category', 'title', 'description', 'visible', 'featured']

        if not self.validate_json_file('data/news.json', required_fields):
            return False

        try:
            with open('data/news.json', 'r') as f:
                news_data = json.load(f)

            # Check for unique IDs
            ids = [item.get('id') for item in news_data]
            if len(ids) != len(set(ids)):
                self.errors.append("Duplicate news IDs found")

            # Check date formats
            for i, item in enumerate(news_data):
                try:
                    datetime.strptime(item.get('date', ''), '%Y-%m-%d')
                except ValueError:
                    self.errors.append(f"News item {i}: Invalid date format (should be YYYY-MM-DD)")

                # Check required boolean fields
                for field in ['visible', 'featured']:
                    if not isinstance(item.get(field), bool):
                        self.warnings.append(f"News item {i}: '{field}' should be true/false")

            print(f"📊 Found {len(news_data)} news items")
            return True

        except Exception as e:
            self.errors.append(f"Error validating news data: {e}")
            return False

    def validate_publications_data(self) -> bool:
        """Validate publications.json structure and content"""
        print("\n📚 Validating publications data...")

        required_fields = ['title', 'authors', 'venue', 'year']

        if not self.validate_json_file('publications.json', required_fields):
            return False

        try:
            with open('publications.json', 'r') as f:
                pub_data = json.load(f)

            # Check year values
            for i, pub in enumerate(pub_data):
                year = pub.get('year')
                if not isinstance(year, int) or year < 1990 or year > datetime.now().year + 2:
                    self.warnings.append(f"Publication {i}: Unusual year value: {year}")

                # Check for empty titles
                title = pub.get('title', '').strip()
                if not title:
                    self.errors.append(f"Publication {i}: Empty title")

                # Check citations
                citations = pub.get('citations', 0)
                if not isinstance(citations, int) or citations < 0:
                    self.warnings.append(f"Publication {i}: Invalid citations count: {citations}")

            print(f"📊 Found {len(pub_data)} publications")
            return True

        except Exception as e:
            self.errors.append(f"Error validating publications data: {e}")
            return False

    def validate_config_data(self) -> bool:
        """Validate scholar_config.json"""
        print("\n🎓 Validating Google Scholar configuration...")

        if not self.validate_json_file('data/scholar_config.json'):
            return False

        try:
            with open('data/scholar_config.json', 'r') as f:
                config = json.load(f)

            # Check required fields
            required_fields = ['author_name', 'affiliation']
            for field in required_fields:
                if not config.get(field):
                    self.warnings.append(f"Config: Missing or empty '{field}'")

            # Check settings
            settings = config.get('settings', {})
            delay = settings.get('delay_between_requests', 2)
            if not isinstance(delay, (int, float)) or delay < 1:
                self.warnings.append("Config: delay_between_requests should be >= 1 second")

            print("✅ Configuration file validated")
            return True

        except Exception as e:
            self.errors.append(f"Error validating config: {e}")
            return False

    def validate_html_integrity(self) -> bool:
        """Basic validation of main HTML file"""
        print("\n🌐 Validating HTML file...")

        if not os.path.exists('index.html'):
            self.errors.append("Main HTML file (index.html) not found")
            return False

        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for required sections
            required_sections = [
                '<!-- News Section -->',
                '<!-- Publication Categories -->',
                '<!-- Recent Publications -->'
            ]

            for section in required_sections:
                if section not in content:
                    self.warnings.append(f"HTML: Missing section marker: {section}")

            # Check file size (should be reasonable)
            size_kb = len(content.encode('utf-8')) / 1024
            if size_kb < 10:
                self.warnings.append(f"HTML file seems too small ({size_kb:.1f}KB)")
            elif size_kb > 1000:
                self.warnings.append(f"HTML file seems very large ({size_kb:.1f}KB)")

            print(f"📊 HTML file size: {size_kb:.1f}KB")
            return True

        except Exception as e:
            self.errors.append(f"Error validating HTML: {e}")
            return False

    def validate_system(self) -> bool:
        """Run complete system validation"""
        print("🔍 SAIL Lab Website Data Validation")
        print("=" * 40)

        # Validate all components
        news_ok = self.validate_news_data()
        pubs_ok = self.validate_publications_data()
        config_ok = self.validate_config_data()
        html_ok = self.validate_html_integrity()

        # Show results
        print("\n📊 VALIDATION RESULTS")
        print("-" * 25)

        if self.errors:
            print("❌ ERRORS FOUND:")
            for error in self.errors:
                print(f"   • {error}")

        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"   • {warning}")

        if not self.errors and not self.warnings:
            print("✅ All validations passed!")
            print("🎉 System is ready for operation")

        print(f"\nSummary: {len(self.errors)} errors, {len(self.warnings)} warnings")

        return len(self.errors) == 0

def main():
    """Main validation function"""
    validator = DataValidator()
    success = validator.validate_system()

    if not success:
        print("\n🔧 RECOMMENDED ACTIONS:")
        print("1. Fix any errors listed above")
        print("2. Review warnings for potential issues")
        print("3. Run validation again: npm run validate")
        print("4. Check documentation in docs/ folder")

    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)