#!/usr/bin/env bash
# Usage: jitter_run.sh <seconds_max> <command...>
# Adds random delay up to $1 seconds before running the rest
# Prevents all agents from hitting APIs at the same wall-clock second
JITTER=$(( RANDOM % ${1:-180} ))
sleep $JITTER
shift
exec "$@"
