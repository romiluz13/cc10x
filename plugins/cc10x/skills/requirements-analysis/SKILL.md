---
name: requirements-analysis
description: Identifies requirements best practices including stakeholder analysis, elicitation, acceptance criteria, scope management, and validation. Used by the planning workflow and related subagents to capture complete requirements before design or implementation.
---

# Requirements Analysis

## Progressive Loading Stages

### Stage 1: Metadata
- **Skill**: Requirements Analysis
- **Purpose**: Gather, analyze, and validate requirements clearly
- **When**: Requirements gathering, feature planning, scope definition
- **Core Rule**: Unclear requirements lead to failed projects
- **Sections Available**: Elicitation, Acceptance Criteria, Scope Management, Quick Checks

---

### Stage 2: Quick Reference

#### Requirements Analysis Checklist

```
Requirement Quality:
- [ ] Requirement is clear and unambiguous
- [ ] Requirement is testable/measurable
- [ ] Requirement is feasible
- [ ] Requirement is necessary
- [ ] Acceptance criteria defined
- [ ] Dependencies identified
- [ ] Constraints documented
- [ ] Assumptions listed
- [ ] Stakeholders identified
- [ ] Priority assigned
```

#### Critical Requirement Patterns

**SMART Criteria**:
```
BAD REQUIREMENT
"The system should be fast"
"Users should be able to search"
"The API should be reliable"

GOOD REQUIREMENT (SMART)
Specific: "Users can search by product name, category, or SKU"
Measurable: "Search results return within 500ms"
Achievable: "Using Elasticsearch with proper indexing"
Relevant: "Improves user experience and reduces support tickets"
Time-bound: "Complete by Q2 2024"
```

**Acceptance Criteria**:
```
VAGUE
Feature: User Registration
Scenario: User can register
  Given user is on registration page
  When user enters data
  Then user is registered

CLEAR
Feature: User Registration
Scenario: User can register with valid email
  Given user is on registration page
  When user enters:
    - Valid email (user@example.com)
    - Password (12+ chars, upper, lower, number, symbol)
    - Confirm password (matches)
  And clicks "Register"
  Then user account is created
  And confirmation email is sent
  And user is redirected to login page

Scenario: User cannot register with invalid email
  Given user is on registration page
  When user enters invalid email (notanemail)
  And clicks "Register"
  Then error message appears: "Invalid email format"
  And user account is NOT created
```

**User Stories**:
```
INCOMPLETE
"As a user, I want to search products"

COMPLETE
"As a customer, I want to search products by name
So that I can quickly find items I'm looking for
Acceptance Criteria:
- Search box visible on homepage
- Results return within 500ms
- Results show product name, price, image
- No results shows helpful message
- Search is case-insensitive
- Partial matches supported"
```

#### Red Flags FLAG
```bash
# Vague requirements
grep -r "should be\|nice to have\|maybe\|possibly" requirements/

# Missing acceptance criteria
grep -r "Feature:" requirements/ | grep -v "Scenario:"

# Unclear scope
grep -r "and\|or\|etc\|etc\." requirements/

# Missing constraints
grep -r "Feature:" requirements/ | grep -v "Constraint:"
```

---

### Stage 3: Detailed Guide

## Requirement Elicitation Techniques

### Stakeholder Interviews

```
Questions to Ask:
1. What problem are we solving?
2. Who are the users?
3. What are their pain points?
4. What success looks like?
5. What are the constraints?
6. What's the timeline?
7. What's the budget?
8. What are the risks?
9. What are the dependencies?
10. How will we measure success?
```

### User Story Mapping

```
Epic: User Management
|-Story 1: User Registration
  |-Task: Email validation
  |-Task: Password hashing
  `-Task: Confirmation email
|-Story 2: User Login
  |-Task: Credential validation
  |-Task: Session creation
  `-Task: Remember me option
`-Story 3: User Profile
    |-Task: View profile
    |-Task: Edit profile
    `-Task: Delete account
```

### Requirements Traceability Matrix

```
| ID | Requirement | User Story | Test Case | Status |
|----|-------------|-----------|-----------|--------|
| R1 | Users can register | US-1 | TC-1, TC-2 | Done |
| R2 | Email validation | US-1 | TC-3, TC-4 | In Progress |
| R3 | Password strength | US-1 | TC-5 | Pending |
```

## Acceptance Criteria Patterns

### Given-When-Then Format

```
Scenario: User can reset password
  Given user is logged out
  And user has registered account
  When user clicks "Forgot Password"
  And enters registered email
  And clicks "Send Reset Link"
  Then confirmation message appears
  And reset email is sent
  And reset link expires in 1 hour
```

### Checklist Format

```
Feature: Payment Processing
Acceptance Criteria:
- [ ] User can enter card details
- [ ] Card validation performed
- [ ] Payment processed securely
- [ ] Confirmation email sent
- [ ] Order created in database
- [ ] Inventory updated
- [ ] User can view order status
```

### Rule Format

```
Feature: Discount Calculation
Rules:
- Discount applies only to items over $50
- Maximum discount is 20%
- Discount codes expire after 30 days
- One discount code per order
- Discount cannot be combined with sales
```

## Scope Management

### Scope Statement

```
Project: E-commerce Platform

In Scope:
- User registration and login
- Product catalog browsing
- Shopping cart
- Checkout process
- Order history
- Basic search

Out of Scope:
- Inventory management
- Admin dashboard
- Reporting
- Mobile app
- Payment gateway integration (Phase 2)
- Recommendation engine (Phase 2)

Constraints:
- Budget: $50,000
- Timeline: 3 months
- Team: 5 developers
- Technology: Node.js, React, MongoDB
```

## Requirement Validation

### Validation Checklist

```
For Each Requirement:
- [ ] Is it clear and unambiguous?
- [ ] Is it testable/measurable?
- [ ] Is it feasible with current resources?
- [ ] Is it necessary for MVP?
- [ ] Are acceptance criteria defined?
- [ ] Are dependencies identified?
- [ ] Are constraints documented?
- [ ] Have stakeholders approved?
- [ ] Is priority assigned?
- [ ] Is effort estimated?
```

## Requirements Analysis Checklist

### Gathering
- [ ] All stakeholders identified
- [ ] Interviews conducted
- [ ] User stories created
- [ ] Use cases documented
- [ ] Constraints identified
- [ ] Assumptions listed
- [ ] Risks identified

### Analysis
- [ ] Requirements are clear
- [ ] Requirements are testable
- [ ] Requirements are feasible
- [ ] Requirements are necessary
- [ ] Acceptance criteria defined
- [ ] Dependencies mapped
- [ ] Conflicts resolved

### Validation
- [ ] Stakeholders approve
- [ ] Requirements are prioritized
- [ ] Effort estimated
- [ ] Timeline realistic
- [ ] Resources allocated
- [ ] Risks mitigated
- [ ] Traceability matrix created

### Documentation
- [ ] Requirements documented
- [ ] User stories written
- [ ] Acceptance criteria clear
- [ ] Use cases documented
- [ ] Constraints listed
- [ ] Assumptions documented
- [ ] Glossary provided

---

**Remember**: Good requirements prevent bad implementations. Invest time upfront!
