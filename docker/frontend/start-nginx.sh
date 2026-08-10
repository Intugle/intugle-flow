#!/bin/sh
set -e

# Define writable directory for the final config
CONFIG_DIR="/tmp/nginx"
mkdir -p $CONFIG_DIR
RUNTIME_CONFIG_PATH="$CONFIG_DIR/runtime-config.js"

# Check and set environment variables
if [ -z "$BACKEND_URL" ]; then
  BACKEND_URL="$1"
fi
if [ -z "$FRONTEND_PORT" ]; then
  FRONTEND_PORT="$2"
fi
if [ -z "$FRONTEND_PORT" ]; then
  FRONTEND_PORT="80"
fi
if [ -z "$LANGFLOW_MAX_FILE_SIZE_UPLOAD" ]; then
  LANGFLOW_MAX_FILE_SIZE_UPLOAD="1"
fi
if [ -z "$LANGFLOW_UNAUTHORIZED_REDIRECT_URL" ]; then
  LANGFLOW_UNAUTHORIZED_REDIRECT_URL=""
fi
if [ -z "$BACKEND_URL" ]; then
  echo "BACKEND_URL must be set as an environment variable or as first parameter. (e.g. http://localhost:7860)"
  exit 1
fi

escaped_unauthorized_redirect_url=$(printf '%s' "$LANGFLOW_UNAUTHORIZED_REDIRECT_URL" | sed 's/\\/\\\\/g; s/"/\\"/g')

cat > "$RUNTIME_CONFIG_PATH" <<EOF
window.__LANGFLOW_RUNTIME_CONFIG__ = Object.freeze({
  LANGFLOW_UNAUTHORIZED_REDIRECT_URL: "$escaped_unauthorized_redirect_url"
});
EOF

# Export variables for envsubst
export BACKEND_URL FRONTEND_PORT LANGFLOW_MAX_FILE_SIZE_UPLOAD

# Use envsubst to substitute environment variables in the template
envsubst '${BACKEND_URL} ${FRONTEND_PORT} ${LANGFLOW_MAX_FILE_SIZE_UPLOAD}' < /etc/nginx/conf.d/default.conf.template > $CONFIG_DIR/default.conf

# Start nginx with the new configuration
exec nginx -c $CONFIG_DIR/default.conf -g 'daemon off;'
