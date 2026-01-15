#!/bin/bash
set -e
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# scripts -> pipeline -> src -> Reddit_Scraper
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

cd "$PROJECT_ROOT"

POSTS_FILE=$(python src/pipeline/gather_posts.py -s MMA -f 72 -u 16 -l 1000 -h)

python src/pipeline/gather_comments.py --input "$POSTS_FILE"
#python src/pipeline/analyse_data.py

