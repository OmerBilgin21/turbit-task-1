#!/bin/sh

# credits to: https://github.com/vishnubob for the wait-for-it script
/app/wait-for-it.sh mongodb:27017 --timeout=60 --strict -- echo "MongoDB is up"

python3 src/utils/fetch_data.py

exec python3 main.py
