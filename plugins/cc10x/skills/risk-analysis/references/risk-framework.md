# Risk Analysis Framework

**Reference**: Part of `risk-analysis` skill. See main SKILL.md for overview.

## Risk Analysis Framework (Based on Functionality)

**⚠️ Use this framework to analyze functionality-specific risks, not generic risks**.

## 7-Stage Risk Framework

### 1. Data Flow Risks

**Risks related to data processing**:

- Invalid data breaks functionality
- Missing validation allows bad data
- Data corruption breaks processing

**Focus**: How data flow risks affect functionality flows.

### 2. Dependency Risks

**Risks related to external dependencies**:

- External API down breaks functionality
- Service unavailable breaks integration
- Integration failure breaks functionality

**Focus**: How dependency risks affect functionality flows.

### 3. Timing/Concurrency Risks

**Risks related to timing and concurrency**:

- Timeouts break functionality
- Race conditions break functionality
- Concurrency issues break functionality

**Focus**: How timing risks affect functionality flows.

### 4. UX & Accessibility Risks

**Risks related to user experience**:

- Confusing flows degrade functionality
- Missing feedback degrades functionality
- Poor error messages degrade functionality

**Focus**: How UX risks affect functionality flows.

### 5. Security & Compliance Risks

**Risks related to security**:

- Injection attacks break functionality
- Broken auth breaks functionality
- Unauthorized access breaks functionality

**Focus**: How security risks affect functionality flows.

### 6. Performance & Scalability Risks

**Risks related to performance**:

- Timeouts break functionality
- Crashes break functionality
- Resource exhaustion breaks functionality

**Focus**: How performance risks affect functionality flows.

### 7. Failure & Recovery Risks

**Risks related to failures**:

- Network errors break functionality
- Storage failures break functionality
- System crashes break functionality

**Focus**: How failure risks affect functionality flows.

## Risk Scoring Guide (Functionality-Focused)

**Probability Scale** (1-5):

- 1: Very rare
- 2: Rare but possible
- 3: Occasional
- 4: Common
- 5: Very common

**Impact Scale** (1-5):

- 1: Minor impact on functionality
- 2: Some impact on functionality
- 3: Significant impact on functionality
- 4: Major impact on functionality
- 5: Completely breaks functionality

**Risk Score**: Probability × Impact

**Risk Priority**:

- **Critical**: Score 15+ (blocks functionality)
- **Important**: Score 8-14 (affects functionality)
- **Minor**: Score <8 (can defer)

## Risk Mitigation Patterns

**Common mitigation patterns**:

- **Retry logic**: For dependency failures
- **Fallback storage**: For storage failures
- **Graceful degradation**: For performance issues
- **Validation**: For data flow risks
- **Rate limiting**: For performance risks
- **Idempotency**: For timing/concurrency risks

**Reference**: `references/mitigation-strategies.md` for detailed mitigation strategies.

---

**See Also**: `references/functionality-analysis.md` for functionality analysis, `references/mitigation-strategies.md` for mitigation strategies.
