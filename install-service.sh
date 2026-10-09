#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_FILE="$SCRIPT_DIR/proteus-ui.service"

if [ ! -f "$SERVICE_FILE" ]; then
  echo "Error: proteus-ui.service not found in $SCRIPT_DIR"
  exit 1
fi

echo "Installing Proteus UI service..."
echo "Make sure you've edited proteus-ui.service with your username and paths first!"
echo ""

sudo cp "$SERVICE_FILE" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable proteus-ui
sudo systemctl start proteus-ui
sudo systemctl status proteus-ui
