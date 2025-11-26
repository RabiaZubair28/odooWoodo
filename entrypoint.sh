#!/bin/bash

if [ ! -d "/app" ]; then
    echo "Error: /app directory does not exist" >&2
    exit 1
fi

cd /app/ || exit
python config/generate_config.py
if [ $? -ne 0 ]; then
    echo "Error: Configuration generation failed" >&2
    exit 1
fi

exec odoo-src/odoo-bin --conf config/odoo.conf "$@"