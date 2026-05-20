#!/bin/bash
# ==============================================
# Facebook Post Crawler - Quick Start Script
# ==============================================
# Usage:
#   ./run_crawler.sh <email> <password> <profile_url> [max_posts] [headless]
#
# Example:
#   ./run_crawler.sh "user@email.com" "password123" "https://www.facebook.com/username" 20 false
# ==============================================

set -e

# Check arguments
if [ $# -lt 3 ]; then
    echo "Usage: $0 <email> <password> <profile_url> [max_posts] [headless]"
    echo ""
    echo "Arguments:"
    echo "  email        - Facebook email/phone"
    echo "  password     - Facebook password"
    echo "  profile_url  - Facebook profile URL to crawl"
    echo "  max_posts    - Maximum posts to crawl (default: 20)"
    echo "  headless     - Run headless mode (default: false)"
    echo ""
    echo "Example:"
    echo "  $0 \"user@email.com\" \"pass123\" \"https://www.facebook.com/zuck\" 10 true"
    exit 1
fi

EMAIL="$1"
PASSWORD="$2"
PROFILE_URL="$3"
MAX_POSTS="${4:-20}"
HEADLESS="${5:-false}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "============================================"
echo "Facebook Post Crawler"
echo "============================================"
echo "Profile URL: $PROFILE_URL"
echo "Max Posts:   $MAX_POSTS"
echo "Headless:    $HEADLESS"
echo "============================================"

# Run the crawler
cd "$SCRIPT_DIR"
robot \
    --variable EMAIL:"$EMAIL" \
    --variable PASSWORD:"$PASSWORD" \
    --variable PROFILE_URL:"$PROFILE_URL" \
    --variable MAX_POSTS:"$MAX_POSTS" \
    --variable HEADLESS:"$HEADLESS" \
    --outputdir output \
    --loglevel INFO \
    tasks/crawl_facebook_posts.robot

echo ""
echo "============================================"
echo "Crawling complete!"
echo "Check the 'output' directory for results."
echo "============================================"
