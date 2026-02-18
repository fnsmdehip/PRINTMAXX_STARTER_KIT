# Security Rules

## Credentials & Secrets

**NEVER:**
- Commit API keys, passwords, or tokens to git
- Hardcode credentials in source code
- Log sensitive information
- Expose credentials in URLs or error messages

**ALWAYS:**
- Use environment variables for secrets
- Add `.env` to `.gitignore`
- Use secure key management (1Password, env vars)
- Rotate credentials if exposed

## Input Validation

**Server-side validation required for:**
- All user input
- File uploads
- API parameters
- Database queries

**Protection against:**
- SQL injection (use parameterized queries)
- XSS (sanitize HTML, escape output)
- CSRF (use tokens for state-changing operations)
- Path traversal (validate file paths)

## Authentication & Authorization

**Requirements:**
- Use established auth libraries (NextAuth, Auth0)
- Implement proper session management
- Use HTTPS only for auth endpoints
- Rate limit login attempts
- Implement secure password reset

**Never:**
- Roll your own crypto
- Store passwords in plain text
- Use weak session IDs
- Trust client-side validation alone

## Data Protection

**Sensitive data:**
- Email addresses → hash where possible
- Payment info → never store, use Stripe tokens
- User data → encrypt at rest if required
- Analytics → anonymize IP addresses

## Third-Party Dependencies

**Before adding dependencies:**
- Check for known vulnerabilities (npm audit)
- Review package maintainer reputation
- Check last update date (avoid abandoned packages)
- Review license compatibility

**Regularly:**
- Run `npm audit fix`
- Update dependencies
- Monitor security advisories

## File Upload Security

**If allowing uploads:**
- Validate file types (whitelist, not blacklist)
- Limit file sizes
- Scan for malware
- Store outside web root
- Generate random filenames
- Never execute uploaded files

## API Security

**For all API endpoints:**
- Require authentication where needed
- Implement rate limiting
- Validate all inputs
- Use proper HTTP methods (GET=read, POST=create, etc.)
- Return appropriate status codes
- Don't expose stack traces in production

## Compliance Requirements

**GDPR (if applicable):**
- User consent for data collection
- Right to deletion
- Data portability
- Clear privacy policy

**FTC (required):**
- Affiliate link disclosures
- Testimonial substantiation
- Clear terms of service

## Incident Response

**If security issue discovered:**
1. Document immediately in OPS/logs/SECURITY_INCIDENT.md
2. Assess severity and impact
3. Patch vulnerability
4. Rotate compromised credentials
5. Notify affected users if required
6. Post-mortem analysis

## Security Checklist for New Features

- [ ] Input validation implemented
- [ ] Authentication/authorization checked
- [ ] No hardcoded secrets
- [ ] Dependencies scanned for vulnerabilities
- [ ] Error messages don't leak sensitive info
- [ ] Rate limiting considered
- [ ] HTTPS enforced
- [ ] Security headers configured
