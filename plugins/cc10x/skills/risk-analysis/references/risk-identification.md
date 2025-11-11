# Risk Identification - Functionality-Focused

**Reference**: Part of `risk-analysis` skill. See main SKILL.md for overview.

## Risk Identification (AFTER Functionality Understood)

**⚠️ IMPORTANT**: Only identify risks AFTER you understand functionality. Focus on risks specific to that functionality.

## Functionality-Focused Risk Checklist

**Priority: Critical (Blocks Functionality)**:

- [ ] Data flow risks that break functionality (invalid data, missing validation, data corruption)
- [ ] Dependency risks that break functionality (external API down, service unavailable, integration failure)
- [ ] Timing risks that break functionality (timeouts, race conditions, concurrency issues)
- [ ] Security risks that break functionality (injection attacks, broken auth, unauthorized access)
- [ ] Performance risks that break functionality (timeouts, crashes, resource exhaustion)
- [ ] Failure risks that break functionality (network errors, storage failures, system crashes)

**Priority: Important (Affects Functionality)**:

- [ ] UX risks that degrade functionality (confusing flows, missing feedback, poor error messages)
- [ ] Performance risks that degrade functionality (slow loading, laggy interactions, high latency)
- [ ] Scalability risks that affect functionality (can't handle load, resource limits)

**Priority: Minor (Can Defer)**:

- [ ] Generic risks that don't affect functionality
- [ ] Perfect risk mitigation (if functionality works)
- [ ] Ideal risk monitoring (if functionality works)

## Risk Identification by Flow Type

### User Flow Risks

**Risks that break user interactions**:

- Missing UI feedback (user doesn't know what's happening)
- Confusing flows (user can't complete tasks)
- Poor error messages (user doesn't know what went wrong)

### System Flow Risks

**Risks that break system processing**:

- Invalid data (system can't process)
- Missing validation (bad data breaks system)
- Data corruption (system processes corrupted data)

### Integration Flow Risks

**Risks that break external integrations**:

- External API down (integration fails)
- Service unavailable (integration breaks)
- Integration failure (functionality breaks)

## Example Risk Identification

**Example: File Upload to CRM**

**Based on Functionality Analysis**:

**Critical Risks (Blocks Functionality)**:

1. **CRM API Down Prevents File Upload**
   - **Source**: Integration flow requirement (System Flow step 4)
   - **Impact**: Completely breaks functionality
   - **Probability**: Occasional

2. **File Validation Fails, Malicious Files Break Functionality**
   - **Source**: System flow requirement (System Flow step 2)
   - **Impact**: Breaks functionality
   - **Probability**: Rare but possible

3. **Network Failure During Upload Breaks Functionality**
   - **Source**: User flow requirement (User Flow step 3)
   - **Impact**: Breaks functionality
   - **Probability**: Common

## Risk Identification Checklist

After risk identification:

- [ ] User Flow risks identified
- [ ] System Flow risks identified
- [ ] Integration Flow risks identified
- [ ] Risks mapped to functionality flows
- [ ] Risks prioritized by functionality impact
- [ ] Ready for risk analysis

---

**See Also**: `references/functionality-analysis.md` for functionality analysis, `references/risk-framework.md` for risk analysis framework.
