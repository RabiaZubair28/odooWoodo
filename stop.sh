#!/bin/bash

if [ "$1" == "--clean" ]; then
    echo "🛑 Stopping containers and removing volumes..."
    docker compose down -v --remove-orphans

    echo "🧹 Cleaning up local volumes and config..."
    cd volumes || exit
    rm -rf *
    cd ..
    cd config || exit
    rm -f odoo.conf
    cd ..
    echo "✅ Sindh HRMIS has been stopped and fully cleaned up."
else
    echo "🛑 Stopping and removing containers..."
    docker compose down --remove-orphans
    echo "✅ Sindh HRMIS has been stopped."
fi