#!/bin/bash
set -e

# Setup directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

# List of subreddits to scrape
SUBREDDITS=("popular")

# Start total timer
START_TOTAL=$(date +%s)

echo "-------------------------------------------"
echo "Starting batch scrape at $(date)"
echo "-------------------------------------------"

for SUB in "${SUBREDDITS[@]}"; do
    echo "Processing subreddit: /r/$SUB"
    
    # Track time for this specific subreddit
    START_SUB=$(date +%s)
    
    # Run the python script
    # -s: sub, -f: from, -u: until, -l: limit, -h: hot
    python src/pipeline/get_data.py -s "$SUB" -f 72 -u 4 -l 1000 -h
    
    END_SUB=$(date +%s)
    DIFF_SUB=$((END_SUB - START_SUB))
    echo "Finished /r/$SUB in $((DIFF_SUB / 60))m $((DIFF_SUB % 60))s"
    echo "-------------------------------------------"
done

# End total timer
END_TOTAL=$(date +%s)
DIFF_TOTAL=$((END_TOTAL - START_TOTAL))

echo "Batch processing complete!"
echo "Total elapsed time: $((DIFF_TOTAL / 60)) minutes and $((DIFF_TOTAL % 60)) seconds."
echo "-------------------------------------------"
