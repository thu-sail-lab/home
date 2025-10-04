#!/usr/bin/env python3
"""
Manual Backup Creation - Creates backups of all important files
"""

import os
import shutil
from datetime import datetime

def create_backup():
    """Create manual backup of all important files"""
    print("💾 Creating manual backup...")

    # Create backup directory
    backup_dir = 'backups'
    os.makedirs(backup_dir, exist_ok=True)

    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    files_to_backup = [
        ('index.html', f'index_manual_{timestamp}.html'),
        ('publications.json', f'publications_manual_{timestamp}.json'),
        ('data/news.json', f'news_manual_{timestamp}.json'),
        ('data/scholar_config.json', f'scholar_config_manual_{timestamp}.json')
    ]

    backed_up = []
    errors = []

    for source, backup_name in files_to_backup:
        if os.path.exists(source):
            try:
                backup_path = os.path.join(backup_dir, backup_name)
                shutil.copy2(source, backup_path)
                size_kb = os.path.getsize(backup_path) / 1024
                backed_up.append((backup_name, size_kb))
                print(f"  ✅ {source} → {backup_name} ({size_kb:.1f}KB)")
            except Exception as e:
                errors.append(f"Failed to backup {source}: {e}")
                print(f"  ❌ {source}: {e}")
        else:
            errors.append(f"File not found: {source}")
            print(f"  ⚠️  {source}: File not found")

    print(f"\n📊 Backup Summary:")
    print(f"  ✅ Successfully backed up: {len(backed_up)} files")
    print(f"  ❌ Errors: {len(errors)}")

    if backed_up:
        total_size = sum(size for _, size in backed_up)
        print(f"  💾 Total backup size: {total_size:.1f}KB")
        print(f"  📁 Backup location: {backup_dir}/")

    if errors:
        print(f"\n⚠️  Issues encountered:")
        for error in errors:
            print(f"    • {error}")

    return len(errors) == 0

def main():
    """Main backup function"""
    print("🔧 SAIL Lab Website Manual Backup")
    print("=" * 35)

    success = create_backup()

    if success:
        print("\n🎉 Backup completed successfully!")
        print("\nNext steps:")
        print("• Backups are stored in the backups/ folder")
        print("• Use these files to restore if needed")
        print("• Consider committing to git for version control")
    else:
        print("\n❌ Backup completed with errors")
        print("• Check error messages above")
        print("• Ensure all files exist and are accessible")

if __name__ == "__main__":
    main()