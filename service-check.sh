#!/usr/bin/env bash

set -u

SERVICE="${1:-}"
URL="${2:-}"

if [[ -z "$SERVICE" || -z "$URL" ]]; then
    echo "Usage: $0 <service-name> <health-url>"
    exit 2
fi

echo "Checking service: $SERVICE"

if ! systemctl is-active --quiet "$SERVICE"; then
    echo "FAILED: $SERVICE is not running"
    exit 1
fi

echo "PASSED: $SERVICE is running"
echo "Checking URL: $URL"

if curl --fail --silent --show-error --max-time 5 "$URL" > /dev/null; then
    echo "PASSED: $URL returned a successful response"
    exit 0
else
    echo "FAILED: $URL did not return a successful response"
    exit 1
fi
