#!/bin/bash

set -e

# Variables
INFLUX_ORG="my-org"
INFLUX_BUCKET="cpu-load"
INFLUX_USER="admin"
INFLUX_PASSWORD="password"
TELEGRAF_CONF="./Telegraf/telegraf.conf"
ENV_FILE=".env"

# Wait for InfluxDB to initialize
echo "Waiting for InfluxDB to initialize..."
sleep 5

# Step 2: Set up InfluxDB
echo "Setting up InfluxDB..."
docker exec -it pxl_influxdb influx setup --org "$INFLUX_ORG" --bucket "$INFLUX_BUCKET" --username "$INFLUX_USER" --password "$INFLUX_PASSWORD" --force

# Generate an InfluxDB token
INFLUX_TOKEN=$(docker exec -it pxl_influxdb influx auth list --json | jq -r '.[0].token')
if [ -z "$INFLUX_TOKEN" ]; then
  echo "Failed to retrieve InfluxDB token. Exiting..."
  exit 1
fi
echo "InfluxDB token retrieved: $INFLUX_TOKEN"

# Step 3: Update the .env file
echo "Updating .env file with new credentials..."
cat <<EOF > $ENV_FILE
INFLUX_BUCKET=$INFLUX_BUCKET
INFLUX_TOKEN=$INFLUX_TOKEN
INFLUX_ORG=$INFLUX_ORG
EOF

# Step 4: Create or Update Telegraf configuration file
echo "Creating or updating Telegraf configuration file..."
mkdir -p "$(dirname $TELEGRAF_CONF)"
cat <<EOF > $TELEGRAF_CONF
[[outputs.influxdb_v2]]
  urls = ["http://pxl_influxdb:8086"]
  bucket = "$INFLUX_BUCKET"
  token = "$INFLUX_TOKEN"
  organization = "$INFLUX_ORG"

[[inputs.system]]
  interval = "1s"
  name_override = "cpu_metrics"

[[inputs.prometheus]]
  urls = ["http://pxl_influxdb:8086/metrics"]
  metric_version = 1
EOF

# Step 5: Restart the entire environment
echo "Restarting the environment with Telegraf..."
docker-compose up -d telegraf

echo "Setup complete! Telegraf is now monitoring metrics."