#!/bin/bash
set -euo pipefail

SOCAT_PID=""
WARP_PID=""

cleanup() {
	local exit_code=$?

	if [[ -n "$SOCAT_PID" ]] && kill -0 "$SOCAT_PID" 2>/dev/null; then
		kill "$SOCAT_PID" 2>/dev/null || true
		wait "$SOCAT_PID" 2>/dev/null || true
	fi

	if [[ -n "$WARP_PID" ]] && kill -0 "$WARP_PID" 2>/dev/null; then
		kill "$WARP_PID" 2>/dev/null || true
		wait "$WARP_PID" 2>/dev/null || true
	fi

	exit "$exit_code"
}

trap cleanup SIGTERM SIGINT EXIT

socat TCP-LISTEN:4000,bind=0.0.0.0,fork,reuseaddr TCP:127.0.0.1:50000 &
SOCAT_PID=$!

warp-svc &
WARP_PID=$!

# Exit if either critical process exits; trap will clean up the other one.
wait -n "$WARP_PID" "$SOCAT_PID"