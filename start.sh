#!/bin/bash

# 1. Convert JSON to Markdown
for json_file in inputs/*.json; do
    if [ -f "$json_file" ]; then
        python3 -m src.json2md --input "$json_file"
    fi
done

# 2. Build Markdown to HTML static site
python3 src/static_generator/md2html.py

# 3. Docker commands
docker compose down && docker compose up -d
