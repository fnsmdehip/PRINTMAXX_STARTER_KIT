#!/bin/bash
# PRINTMAXX Agent Daemon Wrapper
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
exec python3 -u AUTOMATIONS/printmaxx_agent.py >> AUTOMATIONS/agent/daemon.log 2>> AUTOMATIONS/agent/daemon_error.log
