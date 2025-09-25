#!/bin/bash
POSTS_FILE=$(python ../scrape_main_page.py -s MMA -f 72 -u 16 -l 1000 -h)
python ../gather_comments.py --input "$POSTS_FILE"
python ../analyse_data.py
