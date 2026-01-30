#!/bin/bash
set -e

# Setup directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

# List of subreddits to analyze
SUBREDDITS=("popular")

# Start total timer
START_TOTAL=$(date +%s)

echo "-------------------------------------------"
echo "Starting batch analysis at $(date)"
echo "-------------------------------------------"

for SUB in "${SUBREDDITS[@]}"; do
    echo "Analyzing subreddit: /r/$SUB"
    
    # Track time for this specific subreddit
    START_SUB=$(date +%s)
    
    # Run analysis pipeline
    echo "  → Running NLP analysis..."
    python src/pipeline/analyze_subreddit.py "$SUB"
    
    # Generate insights
    echo "  → Generating insights..."
    python src/pipeline/generate_insights.py "$SUB"
    
    END_SUB=$(date +%s)
    DIFF_SUB=$((END_SUB - START_SUB))
    echo "Finished /r/$SUB in $((DIFF_SUB / 60))m $((DIFF_SUB % 60))s"
    echo "-------------------------------------------"
done

# End total timer
END_TOTAL=$(date +%s)
DIFF_TOTAL=$((END_TOTAL - START_TOTAL))

echo "Batch analysis complete!"
echo "Total elapsed time: $((DIFF_TOTAL / 60)) minutes and $((DIFF_TOTAL % 60)) seconds."
echo "-------------------------------------------"
