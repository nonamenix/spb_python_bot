#!/usr/bin/env bash
set -euo pipefail

# Usage: ./deploy.sh [user@host]
# Defaults to DEPLOY_HOST env var if no argument given.

HOST="${1:-${DEPLOY_HOST:?Set DEPLOY_HOST or pass host as argument}}"
REMOTE_DIR="${DEPLOY_DIR:-/srv/spb_python_bot}"

echo "==> Deploying to $HOST:$REMOTE_DIR"

# Copy required files to the server
ssh "$HOST" "mkdir -p $REMOTE_DIR"
scp "$(dirname "$0")/docker-compose.yml" "$HOST:$REMOTE_DIR/docker-compose.yml"

# Pull latest image and restart
ssh "$HOST" bash -s << EOF
  cd $REMOTE_DIR
  docker compose pull
  docker compose up -d --remove-orphans
  docker compose ps
EOF

echo "==> Done"
