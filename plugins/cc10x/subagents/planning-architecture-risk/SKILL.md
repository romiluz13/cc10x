---
name: planning-architecture-risk
description: Parallel subagent for PLANNING workflow. Designs system architecture and assesses risks. Loads architecture-patterns and risk-analysis skills. Runs in parallel with planning-design-deployment for 1.5x faster planning.
license: MIT
---

# Planning Architecture & Risk Subagent

**Parallel planning of system architecture and risk assessment.**

## When Used

Dispatched by PLANNING workflow when planning features for:
- System architecture design
- Technology selection
- Component breakdown
- Data model design
- API specification
- Risk identification
- Mitigation planning

## Workflow

**Pattern**: Parallel execution (runs simultaneously with other planning subagent)  
**Skills Loaded**: architecture-patterns, risk-analysis  
**Time**: ~4-5 minutes (parallel with other subagent)  

---

## Phase 1: Load Skills

**Load in independent context:**

1. **architecture-patterns**
   - System architecture design
   - Technology selection
   - Component breakdown
   - Data model design
   - API specification

2. **risk-analysis**
   - Security risk assessment
   - Performance risk assessment
   - Operational risk assessment
   - Technical risk assessment

---

## Phase 2: Design System Architecture

**Design the overall system:**

### High-Level Architecture
- [ ] Architecture diagram created
- [ ] Technology stack chosen
- [ ] Trade-offs documented
- [ ] Scalability considered
- [ ] Maintainability considered

### Component Breakdown
- [ ] Major components identified
- [ ] Component responsibilities defined
- [ ] Component interactions documented
- [ ] Component dependencies mapped
- [ ] Reusability considered

### Data Models
- [ ] Database schema designed
- [ ] Data relationships defined
- [ ] Data flow documented
- [ ] Normalization considered
- [ ] Indexing strategy planned

### API Specification
- [ ] Endpoints designed
- [ ] Request/response formats defined
- [ ] Error handling strategy
- [ ] Authentication/authorization
- [ ] Rate limiting strategy

---

## Phase 3: Assess Risks

**Identify and mitigate risks:**

### Security Risks
- [ ] Vulnerability assessment
- [ ] Attack vector analysis
- [ ] Mitigation strategies
- [ ] Security controls
- [ ] Compliance requirements

### Performance Risks
- [ ] Scalability assessment
- [ ] Performance bottlenecks
- [ ] Optimization strategies
- [ ] Load testing plan
- [ ] Caching strategy

### Operational Risks
- [ ] Deployment risks
- [ ] Monitoring needs
- [ ] Rollback strategies
- [ ] Disaster recovery
- [ ] Incident response

### Technical Risks
- [ ] Technology risks
- [ ] Integration risks
- [ ] Dependency risks
- [ ] Vendor lock-in
- [ ] Technical debt

---

## Phase 4: Compile Architecture & Risk Plan

**Organize architecture and risk findings:**

### Architecture Plan
- System architecture diagram
- Technology decisions
- Component breakdown
- Data models
- API specification

### Risk Register
- Security risks
- Performance risks
- Operational risks
- Technical risks
- Mitigation strategies
- Contingency plans

---

## Phase 5: Return Results

**Provide architecture and risk planning:**

```markdown
## System Architecture

### High-Level Design
- [Architecture description]
- [Technology stack]
- [Trade-offs]

### Components
- [Component 1]: [Description]
- [Component 2]: [Description]
- [Component 3]: [Description]

### Data Models
- [Entity 1]: [Description]
- [Entity 2]: [Description]
- [Relationships]: [Description]

### API Specification
- [Endpoint 1]: [Description]
- [Endpoint 2]: [Description]
- [Authentication]: [Description]

## Risk Assessment

### Security Risks
- [Risk 1]: [Description]
  - Mitigation: [Strategy]
  - Priority: [High/Medium/Low]

### Performance Risks
- [Risk 1]: [Description]
  - Mitigation: [Strategy]
  - Priority: [High/Medium/Low]

### Operational Risks
- [Risk 1]: [Description]
  - Mitigation: [Strategy]
  - Priority: [High/Medium/Low]

### Technical Risks
- [Risk 1]: [Description]
  - Mitigation: [Strategy]
  - Priority: [High/Medium/Low]
```

---

## Integration

**Runs in parallel with:**
- planning-design-deployment

**Merged by**: planning-workflow

**Result**: 1.5x faster planning (4-5 min vs 7 min)

