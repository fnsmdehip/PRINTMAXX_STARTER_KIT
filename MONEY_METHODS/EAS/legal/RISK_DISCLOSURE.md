> **TEMPLATE — Review with qualified legal counsel before use.**
> This document is a starting template and does not constitute legal advice.

---

# AUTOMATION RISK DISCLOSURE AND ACKNOWLEDGMENT

**Addendum to Master Services Agreement MSA-[NUMBER]**

**Date:** [DATE]

---

## PARTIES

**Client:** [CLIENT_NAME] ("Client")

**Service Provider:** Enterprise Automation Solutions, a trade name of [LLC_NAME] LLC ("EAS")

---

## PREAMBLE

This Risk Disclosure Addendum ("Addendum") supplements the Master Services Agreement ("MSA") between Client and EAS dated [MSA_DATE]. This Addendum is incorporated into and forms part of the MSA. Client acknowledges and agrees that it has been informed of the following inherent risks associated with AI and automation systems, and that Client enters into the engagement with full knowledge of these risks.

---

## SECTION A: STANDARD RISKS — ALL ENGAGEMENTS

The following risks are inherent to all AI and automation implementations. These risks exist regardless of the quality of implementation and cannot be fully eliminated.

### 1. AI Detection

AI-powered phone systems, chatbots, and voice agents may be detected as artificial by callers, customers, or other parties. Detection rates vary based on the voice model used, caller demographics, call complexity, ambient noise, and individual caller sensitivity. Detection may negatively impact caller experience or trust. Client should consider disclosure requirements under applicable state and federal laws regarding AI-generated communications.

### 2. Automation Accuracy

Automation workflows may produce incorrect, incomplete, or unexpected outputs that require human review and correction. No automation system achieves 100% accuracy across all conditions. Output quality depends on input data quality, system configuration, and the complexity of the automated process. EAS implements validation checks and error handling, but these measures reduce rather than eliminate the risk of incorrect outputs.

### 3. AI Summarization and Interpretation

AI-powered meeting summaries, document analysis, and content generation may omit relevant context, misattribute statements to incorrect speakers, misinterpret intent or tone, or produce factually inaccurate content. Human review of all AI-generated content is strongly recommended, particularly for content involving critical business decisions, legal matters, financial commitments, or customer-facing communications.

### 4. Third-Party Service Dependencies

Automations rely on third-party APIs, platforms, and services (including but not limited to CRM systems, phone providers, calendar services, email platforms, and cloud infrastructure). These third-party services may change their APIs, alter pricing, degrade in performance, experience outages, or discontinue entirely without advance notice. EAS will use commercially reasonable efforts to adapt automations to such changes within the scope of Managed Operations, or notify Client promptly if changes require a new SOW.

### 5. Monitoring Requirements

All automated systems require ongoing monitoring to ensure continued correct operation. Unmonitored automations may process data incorrectly, fail silently, accumulate errors over time, or behave unexpectedly due to changes in input data patterns or external conditions. Client is responsible for monitoring automations that are not covered under a Managed Operations agreement.

### 6. Not Professional Advice

EAS provides automation consulting services only. EAS does not provide legal, medical, financial, tax, regulatory compliance, or other professional advice. All automations that touch regulated areas (healthcare, finance, legal, insurance, real estate, etc.) must be reviewed and approved by Client's qualified compliance personnel or professional advisors before deployment. Client bears sole responsibility for ensuring that automated processes comply with applicable laws and regulations.

### 7. Performance Estimates

Performance metrics, time savings projections, cost reduction estimates, and ROI calculations provided by EAS are estimates based on comparable implementations in similar industries. Actual results will vary based on Client's specific business size, industry, data quality, operational complexity, staff adoption, customer behavior, and other factors outside EAS's control. Past performance of similar implementations does not guarantee future results.

### 8. Data Transit Through Third-Party Services

Client data may be transmitted through, processed by, and temporarily stored on third-party platforms as part of the automation workflows. A list of third-party services used in each engagement is provided in the applicable SOW. While EAS selects third-party providers with reasonable security practices, EAS cannot guarantee the security practices or data handling procedures of third-party services. Client should review the privacy policies and terms of service of all third-party providers identified in the SOW.

### 9. Client Control

Client retains full operational control over all deployed automations and may disable, pause, or modify any automation at any time. EAS recommends that Client maintain documented procedures for emergency shutdown of automated systems. EAS will provide kill-switch or pause functionality for all deployed automations.

### 10. Open-Source Software

Deliverables may incorporate open-source software components (including but not limited to n8n, Node.js libraries, Python packages, and similar tools). Open-source components are governed by their respective open-source licenses, not the MSA. EAS does not warrant, guarantee, or provide indemnification for open-source software. Client is responsible for reviewing and complying with applicable open-source license terms. Open-source projects may be discontinued, modified, or may contain security vulnerabilities discovered after deployment.

---

## SECTION B: ELEVATED RISKS — FINANCIAL AND HEALTHCARE DATA

The following additional risks apply to engagements involving financial data, healthcare data, or other sensitive regulated information. Client shall indicate which categories apply by initialing below.

### 11. Financial Data Automations

[ ] **Applicable to this engagement** (Client initial: ______)

Automations involving financial data (including invoicing, payment processing, reconciliation, expense categorization, and financial reporting) carry elevated risk due to the potential for monetary loss from processing errors. EAS strongly recommends that Client implement human approval steps for all automated financial transactions above a Client-defined dollar threshold. Automated financial processes should be reconciled against manual records on a regular basis during the initial deployment period. EAS is not responsible for financial losses resulting from automated transactions that were not subject to human review.

### 12. Healthcare Data (PHI/HIPAA)

[ ] **Applicable to this engagement** (Client initial: ______)

Engagements involving Protected Health Information (PHI) as defined under the Health Insurance Portability and Accountability Act (HIPAA) require execution of a separate Business Associate Agreement (BAA) before any project work commences. PHI processing will be logged and auditable. Client is responsible for ensuring that all automated workflows involving PHI comply with HIPAA Privacy, Security, and Breach Notification Rules. EAS will implement reasonable technical safeguards but does not guarantee HIPAA compliance of Client's overall operations. Client must conduct its own HIPAA risk assessment.

---

## SECTION C: EAS RISK MITIGATION PRACTICES

EAS implements the following practices to mitigate the risks described above. These practices reduce but do not eliminate risk.

### Rollback Plans
All pilot implementations include documented rollback procedures to restore prior manual workflows if automated systems underperform or encounter critical issues.

### Human-in-the-Loop Checkpoints
Critical decision points within automated workflows include human review and approval steps. The specific checkpoints are documented in each SOW and can be adjusted based on Client's risk tolerance.

### Telemetry and Monitoring
Deployed automations include telemetry, logging, and monitoring capabilities that track system performance, error rates, and processing volumes. Alerting thresholds are configured to notify appropriate personnel of anomalies.

### Runbooks and Troubleshooting Guides
Each deployment includes a comprehensive runbook documenting: standard operating procedures, common error scenarios and resolutions, escalation procedures, and emergency shutdown instructions.

### Performance Reviews
Managed Operations engagements include monthly review of automation performance, accuracy metrics, and optimization opportunities. Quarterly business reviews assess overall ROI and strategic alignment.

### AI Disclosure Compliance
All AI-facing interactions (phone calls, chatbots, email responses) include clear disclosure that the communication is AI-generated, in compliance with California SB 243 (effective January 1, 2026) and comparable state regulations. Specific disclosure language is documented in each deployment's runbook.

### Recording and Consent Compliance
All voice AI deployments that record or log conversations include explicit consent mechanisms compliant with two-party consent states (California, Illinois, and 9 others). Consent is obtained at the start of each interaction via clear verbal or written disclosure. Client is responsible for ensuring compliance with industry-specific regulations (HIPAA, GLBA, etc.) that may impose additional recording requirements.

### Wiretap Risk Mitigation
In light of growing chatbot wiretap litigation (30+ class actions filed 2021-2025, including cases against Peloton and Apple's $95M Siri settlement), all EAS deployments that involve customer-facing AI communication include: (a) clear disclosure that the interaction involves AI, (b) affirmative consent before any recording or logging, (c) opt-out mechanism for customers who prefer human interaction, and (d) data retention policies that limit storage duration of conversation logs.

---

## ACKNOWLEDGMENT AND AGREEMENT

By signing below, Client acknowledges that:

1. Client has read and understands all risks described in this Addendum.

2. Client has had the opportunity to ask questions about these risks and has received satisfactory answers.

3. Client enters into the engagement with EAS with full knowledge of these risks and voluntarily assumes the risks described herein.

4. EAS's liability for outcomes related to the risks acknowledged in this Addendum is governed by the Limitation of Liability provisions set forth in Section 7 of the MSA.

5. This Addendum does not expand or limit the rights and obligations of either Party beyond what is set forth in the MSA, but serves as evidence that Client was informed of and accepted the inherent risks of AI and automation systems.

6. Client is responsible for maintaining appropriate insurance coverage for its business operations, including coverage for risks that may arise from the use of automated systems.

---

## SIGNATURES

**CLIENT: [CLIENT_NAME]**

| | |
|---|---|
| Signature: | ________________________________ |
| Name: | [AUTHORIZED_SIGNATORY_NAME] |
| Title: | [TITLE] |
| Date: | [DATE] |

---

**ENTERPRISE AUTOMATION SOLUTIONS, a trade name of [LLC_NAME] LLC**

| | |
|---|---|
| Signature: | ________________________________ |
| Name: | [EAS_SIGNATORY_NAME] |
| Title: | [TITLE] |
| Date: | [DATE] |
