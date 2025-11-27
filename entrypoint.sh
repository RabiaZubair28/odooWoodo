#!/bin/bash

ODOO_BIN="odoo-src/odoo-bin"
CONFIG_FILE="config/odoo.conf"

# 1. Check if root directory exists

if [ ! -d "/app" ]; then
    echo "Error: /app directory does not exist" >&2
    exit 1
fi

cd /app/ || exit

# 2. Check if the configuration already exists
if [ -f "$CONFIG_FILE" ]; then
    echo "Odoo configuration already exists. Skipping initialization."
    python config/generate_config.py # Ensure config is up to date
    exec $ODOO_BIN --conf $CONFIG_FILE "$@"
    exit 0
fi

echo "Waiting for PostgreSQL..."
# Using parentheses creates a subshell to suppress errors cleanly
while ! (timeout 1 bash -c "</dev/tcp/$POSTGRES_HOST/$POSTGRES_PORT") >/dev/null 2>&1; do
    echo "  - Database not ready yet..."
    sleep 1
done
echo "PostgreSQL started"

# 3. Generate Configuration and Initialize Database
echo "Generate Odoo Configuration..."
python config/generate_config.py
if [ $? -ne 0 ]; then
    echo "Error: Configuration generation failed" >&2
    exit 1
fi

echo "Initializing Odoo Database..."
$ODOO_BIN -c $CONFIG_FILE -d $POSTGRES_DB -i base -i hrmis_registry --no-http --stop-after-init --db_user=$POSTGRES_USER --db_password=$POSTGRES_PASSWORD

if [ $? -ne 0 ]; then
    echo "Error: Database initialization failed." >&2
    exit 1
fi

# 5. Change the 'admin' Password
# We pipe a Python script into the Odoo shell to securely change the password
echo "Setting Odoo Admin Password..."
$ODOO_BIN shell -c $CONFIG_FILE -d $POSTGRES_DB <<EOF
# env is already available in the odoo shell context
admin_user = env['res.users'].search([('login', '=', 'admin')], limit=1)
if admin_user:
    admin_user.password = '$ODOO_PASSWORD'
    env.cr.commit()
    print("Admin password changed successfully.")
else:
    print("Error: Admin user not found!")
    exit(1)
EOF

# 6. Start Odoo Server

exec $ODOO_BIN --conf $CONFIG_FILE "$@"