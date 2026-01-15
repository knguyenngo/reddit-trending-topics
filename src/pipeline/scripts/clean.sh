#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$PROJECT_ROOT"

echo "Cleaning raw post data"
rm -f src/data/raw/*.json

echo "Cleaning raw comments data"
rm -f src/data/raw/post_comments/*

echo "Cleaning tokens"
rm -f src/data/clean/post_comments/*.json

