#!/usr/bin/env python3
"""
Master Publications Update Script
Orchestrates the complete publication update process
"""

import sys
import subprocess
import json
from datetime import datetime

def run_command(command: list, description: str) -> bool:
    """Run a command and return success status"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def update_config_timestamp():
    """Update the last update timestamp in config"""
    try:
        with open('data/scholar_config.json', 'r') as f:
            config = json.load(f)

        config['last_update'] = datetime.now().isoformat()

        with open('data/scholar_config.json', 'w') as f:
            json.dump(config, f, indent=2)

        print("✓ Updated configuration timestamp")
    except Exception as e:
        print(f"Warning: Could not update config timestamp: {e}")

def main():
    """Main update orchestration"""
    print("SAIL Lab - Publications Update System")
    print("=" * 40)

    # Ask user what they want to do
    print("\nUpdate options:")
    print("1. Fetch new publications from Google Scholar + Update HTML")
    print("2. Update HTML only (using existing publications.json)")
    print("3. Fetch only (no HTML update)")

    choice = input("\nSelect option (1-3): ").strip()

    success = True

    if choice == "1":
        # Full update: fetch + process
        print("\n🚀 Starting full publication update...")

        # Step 1: Fetch from Google Scholar
        if run_command([sys.executable, 'scripts/fetch_scholar_publications.py'],
                      "Fetching publications from Google Scholar"):

            # Step 2: Process and update HTML
            if run_command([sys.executable, 'scripts/auto_process_publications.py'],
                          "Processing publications and updating HTML"):
                update_config_timestamp()
                print("\n🎉 Full update completed successfully!")
            else:
                success = False
        else:
            success = False

    elif choice == "2":
        # HTML update only
        print("\n🔄 Updating HTML only...")

        if run_command([sys.executable, 'scripts/auto_process_publications.py'],
                      "Processing publications and updating HTML"):
            print("\n✅ HTML update completed successfully!")
        else:
            success = False

    elif choice == "3":
        # Fetch only
        print("\n📥 Fetching publications only...")

        if run_command([sys.executable, 'scripts/fetch_scholar_publications.py'],
                      "Fetching publications from Google Scholar"):
            update_config_timestamp()
            print("\n✅ Publications fetched successfully!")
            print("Run option 2 to update the HTML when ready.")
        else:
            success = False

    else:
        print("Invalid option selected.")
        success = False

    if success:
        print("\n📋 Summary:")
        print("- Publications data updated")
        print("- HTML generated with current design")
        print("- Backups created automatically")
        print("\nNext steps:")
        print("1. Review changes in index.html")
        print("2. Test the website locally")
        print("3. Commit changes to git")
    else:
        print("\n❌ Update process failed. Check error messages above.")

if __name__ == "__main__":
    main()