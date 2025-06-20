#!/bin/bash
# Automated research publications update script
# This script can be run daily via cron to keep publications current

echo "🔬 Starting automated research update..."

# Change to the portfolio directory
cd "$(dirname "$0")"

# Update publications from Google Scholar
echo "📡 Fetching latest publications from Google Scholar..."
python3 scholar_manager.py update

# Check if update was successful
if [ $? -eq 0 ]; then
    echo "✅ Research publications updated successfully"
    echo "📊 Current publication count:"
    python3 scholar_manager.py list | tail -1
else
    echo "❌ Failed to update publications"
    echo "💾 Using cached data"
    python3 scholar_manager.py generate
fi

echo "🎯 Research update complete!"

# Optional: Add git commit if you want to automatically commit changes
# Uncomment the lines below if you want automatic commits
# if [ -n "$(git status --porcelain)" ]; then
#     git add research.html .scholar_cache.json scholar_config.json
#     git commit -m "🤖 Auto-update research publications $(date +%Y-%m-%d)"
#     echo "📝 Changes committed to git"
# fi