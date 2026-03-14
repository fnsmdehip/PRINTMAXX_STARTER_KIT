# Security

## Rules

- Keep control services loopback-bound unless they are behind a private transport.
- Prefer tailnet-only publishing over public exposure.
- Rotate bootstrap or pairing tokens after first use.
- Keep state files private if they contain real hostnames, IDs, or URLs.
- Do not mix business logic and control-plane code in the same public repo.

## Publishing checklist

Before open-sourcing, remove or replace:
- real hostnames
- account emails
- auth URLs
- device IDs
- passwords or tokens
- business-specific service names
