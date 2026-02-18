# PRINTMAXX Makefile
# Quick commands for development, builds, validation, and operations

.PHONY: dev build validate content apps test-app lint clean status help

# Default: show help
.DEFAULT_GOAL := help

# ---------------------------
# Development
# ---------------------------

dev: ## Start Next.js dev server
	cd LANDING/printmaxx-site && npm run dev

build: ## Production build
	cd LANDING/printmaxx-site && npm run build

lint: ## Run linter
	cd LANDING/printmaxx-site && npm run lint

clean: ## Clean build artifacts
	rm -rf LANDING/printmaxx-site/.next
	rm -rf LANDING/printmaxx-site/node_modules/.cache
	@echo "Cleaned build artifacts"

# ---------------------------
# Validation
# ---------------------------

validate: ## Run all validators (CSV, markdown, copy-style)
	python3 scripts/validate.py

validate-csv: ## Validate CSV files only
	python3 scripts/validate.py --csv-only

validate-copy: ## Validate copy style only
	python3 scripts/validate.py --copy-only

validate-links: ## Validate internal links only
	python3 scripts/validate.py --links-only

# ---------------------------
# Content Operations
# ---------------------------

content: ## Generate N content pieces (default N=10)
	python3 scripts/content_queue.py --generate $(or $(N),10)

queue: ## Show next items to post
	python3 scripts/content_queue.py --show-queue

post: ## Mark items as posted
	python3 scripts/content_queue.py --mark-posted $(ID)

schedule: ## Show posting schedule
	@cat LEDGER/POSTING_SCHEDULE.md

# ---------------------------
# App Factory
# ---------------------------

apps: ## List app build status
	@echo "=== APP BUILD STATUS ==="
	@echo ""
	@if [ -d "MONEY_METHODS/APP_FACTORY/builds" ]; then \
		for dir in MONEY_METHODS/APP_FACTORY/builds/*/; do \
			app=$$(basename "$$dir"); \
			if [ -f "$$dir/README.md" ]; then \
				status="BUILT"; \
			else \
				status="IN PROGRESS"; \
			fi; \
			echo "  $$app: $$status"; \
		done; \
	else \
		echo "  No builds directory found"; \
	fi
	@echo ""
	@echo "=== APP CLONE OPPORTUNITIES ==="
	@if [ -f "LEDGER/APP_CLONE_OPPORTUNITIES.csv" ]; then \
		head -5 LEDGER/APP_CLONE_OPPORTUNITIES.csv; \
	fi

test-app: ## Test specific app (APP=appname)
ifndef APP
	@echo "Usage: make test-app APP=prayerlock"
	@echo "Available apps:"
	@ls -1 MONEY_METHODS/APP_FACTORY/builds/ 2>/dev/null || echo "  No apps built yet"
else
	@echo "Testing $(APP)..."
	@if [ -d "MONEY_METHODS/APP_FACTORY/builds/$(APP)" ]; then \
		cd MONEY_METHODS/APP_FACTORY/builds/$(APP) && \
		if [ -f "package.json" ]; then \
			npm test 2>/dev/null || echo "No tests configured"; \
		else \
			echo "Not a Node.js app"; \
		fi; \
	else \
		echo "App '$(APP)' not found in builds/"; \
	fi
endif

# ---------------------------
# Status & Monitoring
# ---------------------------

status: ## Show current project status
	@echo "=== PRINTMAXX STATUS ==="
	@echo ""
	@echo "--- Content Queue ---"
	@if [ -f "LEDGER/CONTENT_PIPELINE.csv" ]; then \
		queued=$$(grep -c "QUEUED" LEDGER/CONTENT_PIPELINE.csv 2>/dev/null || echo "0"); \
		posted=$$(grep -c "POSTED" LEDGER/CONTENT_PIPELINE.csv 2>/dev/null || echo "0"); \
		echo "  Queued: $$queued | Posted: $$posted"; \
	fi
	@echo ""
	@echo "--- Accounts ---"
	@if [ -f "LEDGER/ACCOUNTS.csv" ]; then \
		total=$$(tail -n +2 LEDGER/ACCOUNTS.csv | wc -l | tr -d ' '); \
		active=$$(grep -c "ACTIVE" LEDGER/ACCOUNTS.csv 2>/dev/null || echo "0"); \
		echo "  Total: $$total | Active: $$active"; \
	fi
	@echo ""
	@echo "--- Apps ---"
	@if [ -d "MONEY_METHODS/APP_FACTORY/builds" ]; then \
		count=$$(ls -1 MONEY_METHODS/APP_FACTORY/builds/ 2>/dev/null | wc -l | tr -d ' '); \
		echo "  Built: $$count"; \
	else \
		echo "  Built: 0"; \
	fi
	@echo ""
	@echo "--- Leads ---"
	@if [ -f "LEDGER/leads.csv" ]; then \
		leads=$$(tail -n +2 LEDGER/leads.csv 2>/dev/null | wc -l | tr -d ' '); \
		echo "  Total: $$leads"; \
	else \
		echo "  Total: 0"; \
	fi
	@echo ""
	@echo "--- LEDGER Files ---"
	@ls -1 LEDGER/*.csv 2>/dev/null | wc -l | tr -d ' ' | xargs -I {} echo "  CSV files: {}"
	@echo ""
	@echo "Run 'make help' for available commands"

health: ## Check account health
	@if [ -f "AUTOMATIONS/scripts/health_checker.py" ]; then \
		python3 AUTOMATIONS/scripts/health_checker.py; \
	else \
		echo "Health checker not found. Run validation scripts."; \
	fi

# ---------------------------
# Ralph Loops
# ---------------------------

ralph: ## Run a Ralph loop iteration
	@echo "Starting Ralph loop..."
	@if [ -f "ralph_task.md" ]; then \
		claude "Read ralph_task.md and .ralph/guardrails.md. Complete the next unchecked item. Update .ralph/progress.md when done."; \
	else \
		echo "No ralph_task.md found. Create one first."; \
	fi

ralph-status: ## Show Ralph progress
	@if [ -f ".ralph/progress.md" ]; then \
		head -100 .ralph/progress.md; \
	else \
		echo "No Ralph progress file found"; \
	fi

# ---------------------------
# Deployment
# ---------------------------

deploy-check: ## Pre-flight deployment checklist
	@echo "=== DEPLOY CHECKLIST ==="
	@echo ""
	@echo "[1] Build check..."
	@cd LANDING/printmaxx-site && npm run build 2>/dev/null && echo "  OK: Build passes" || echo "  FAIL: Build errors"
	@echo ""
	@echo "[2] Lint check..."
	@cd LANDING/printmaxx-site && npm run lint 2>/dev/null && echo "  OK: Lint passes" || echo "  WARN: Lint issues"
	@echo ""
	@echo "[3] Env check..."
	@if [ -f "LANDING/printmaxx-site/.env.local" ]; then \
		echo "  OK: .env.local exists"; \
	else \
		echo "  WARN: No .env.local file"; \
	fi
	@echo ""
	@echo "[4] Content check..."
	@if [ -d "CONTENT/truth_pages" ]; then \
		count=$$(ls -1 CONTENT/truth_pages/*.md 2>/dev/null | wc -l | tr -d ' '); \
		echo "  Truth pages: $$count"; \
	fi

# ---------------------------
# Help
# ---------------------------

help: ## Show this help
	@echo "PRINTMAXX Makefile Commands"
	@echo ""
	@echo "Usage: make [command]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Examples:"
	@echo "  make dev              Start development server"
	@echo "  make validate         Run all validators"
	@echo "  make content N=25     Generate 25 content pieces"
	@echo "  make test-app APP=prayerlock  Test specific app"
	@echo "  make status           Show project status"
