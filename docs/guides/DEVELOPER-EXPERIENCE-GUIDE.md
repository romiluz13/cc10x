# 🎯 Developer Experience Guide

Complete guide for developers using CC10X with AI assistance.

---

## 1. JUNIOR DEVELOPER LEARNING MODE

### When to Use
- Learning new patterns
- Understanding complex code
- Building first features
- Exploring best practices

### How to Activate
```
"review this code and explain what it does"
"plan a feature and explain the architecture"
"build this component and explain each step"
```

### What You Get
- ✅ Detailed explanations
- ✅ Best practices highlighted
- ✅ Learning resources linked
- ✅ Common mistakes explained
- ✅ Verbose output (more tokens)

### Example
```
You: "review my authentication code and explain the security"

CC10X:
1. Explains what authentication is
2. Reviews your code
3. Explains each security check
4. Highlights best practices
5. Suggests learning resources
6. Explains common mistakes
```

---

## 2. SENIOR DEVELOPER EFFICIENCY MODE

### When to Use
- Quick reviews
- Fast planning
- Rapid prototyping
- Time-sensitive work

### How to Activate
```
"quick review of auth.js"
"fast plan for user dashboard"
"build component quickly"
```

### What You Get
- ✅ Concise output
- ✅ Key findings only
- ✅ Minimal explanations
- ✅ Fast execution
- ✅ Token-efficient

### Example
```
You: "quick review of auth.js"

CC10X:
- Security: ✅ Good
- Performance: ⚠️ N+1 queries
- Quality: ✅ Good
- Recommendation: Fix N+1 in getUserRoles()
```

---

## 3. EMERGENCY DEBUGGING MODE

### When to Use
- Production down
- Critical bugs
- Time-critical fixes
- Skip analysis

### How to Activate
```
"emergency: debug login endpoint"
"URGENT: fix payment processing"
"critical: database connection failing"
```

### What You Get
- ✅ Skip analysis phases
- ✅ Focus on fix only
- ✅ Minimal verification
- ✅ Fast execution
- ✅ Parallel bug fixing

### Example
```
You: "emergency: debug login endpoint"

CC10X:
1. Analyze logs (skip deep analysis)
2. Find root cause
3. Implement fix
4. Quick test
5. Return fix (skip full verification)
```

---

## 4. EXPLORATORY DEVELOPMENT MODE

### When to Use
- Exploring options
- Comparing approaches
- Prototyping ideas
- Learning alternatives

### How to Activate
```
"explore: how to implement authentication"
"compare: REST vs GraphQL for this API"
"options: what are the ways to handle state?"
```

### What You Get
- ✅ Multiple options
- ✅ Pros/cons for each
- ✅ Recommendations
- ✅ Trade-off analysis
- ✅ Learning opportunities

### Example
```
You: "explore: how to implement authentication"

CC10X:
Option 1: JWT
- Pros: Stateless, scalable
- Cons: Token revocation hard
- Best for: Microservices

Option 2: Session-based
- Pros: Simple, revocation easy
- Cons: Stateful, scaling hard
- Best for: Monoliths

Option 3: OAuth2
- Pros: Secure, delegated
- Cons: Complex, overhead
- Best for: Third-party integrations
```

---

## 5. TEAM COLLABORATION MODE

### When to Use
- Sharing findings with team
- Collaborative planning
- Team reviews
- Knowledge sharing

### How to Activate
```
"review and create team report"
"plan and share architecture with team"
"debug and document findings"
```

### What You Get
- ✅ Shareable reports
- ✅ Team-friendly format
- ✅ Decision documentation
- ✅ Rationale explained
- ✅ Easy to discuss

### Example
```
You: "review and create team report"

CC10X:
Creates:
- Executive summary
- Detailed findings
- Recommendations
- Discussion points
- Action items
- Assigned to: [team members]
```

---

## 6. PARTIAL CODE REVIEW

### When to Use
- Large files
- Specific sections
- Function review
- Line range analysis

### How to Activate
```
"review lines 50-150 of auth.js"
"review the login() function"
"review only the database queries"
"review src/auth/ directory"
```

### What You Get
- ✅ Focused analysis
- ✅ Reduced tokens
- ✅ Faster execution
- ✅ Specific findings
- ✅ Context-aware

### Example
```
You: "review lines 50-150 of auth.js"

CC10X:
Analyzing: auth.js (lines 50-150)
- Security: ✅ Good
- Performance: ⚠️ Issue found
- Quality: ✅ Good
Note: Full context may be needed for complete analysis
```

---

## 7. MULTI-INTENT WORKFLOWS

### Sequential Execution
```
"review then plan the authentication system"
→ REVIEW first, then PLAN
```

### Parallel Execution
```
"review and plan the authentication system"
→ Both workflows in parallel
```

### Conditional Execution
```
"review, then plan if no critical issues"
→ REVIEW first, then decide
```

---

## 8. ERROR RECOVERY

### If Workflow Fails
```
❌ ERROR: Subagent timeout
📝 Reason: Analysis took >10 minutes
💡 Suggestion: Try with smaller scope
🔄 Fallback: Returning partial results
```

### If Input Invalid
```
❌ ERROR: Invalid code syntax
📝 Reason: Missing closing brace
💡 Suggestion: Fix syntax and try again
🔄 Fallback: Show syntax error location
```

### If Skill Unavailable
```
❌ ERROR: Security analysis skipped
📝 Reason: security-patterns skill unavailable
💡 Suggestion: Try again later
🔄 Fallback: Using core skills only
```

---

## 9. BEST PRACTICES

### ✅ DO
- Be specific about what you want
- Provide context (files, requirements)
- Use appropriate mode for your situation
- Ask for clarification if confused
- Review results before using

### ❌ DON'T
- Ask for everything at once
- Provide invalid code
- Ignore complexity warnings
- Skip security reviews
- Use on production without testing

---

## 10. QUICK REFERENCE

| Scenario | Command | Mode |
|----------|---------|------|
| Learning | "review and explain" | Verbose |
| Quick check | "quick review" | Concise |
| Production down | "emergency: debug" | Fast |
| Exploring | "explore: options" | Options |
| Team sharing | "review and report" | Shareable |
| Partial review | "review lines 50-100" | Focused |
| Multiple tasks | "review then plan" | Sequential |

---

**Status**: ✅ Complete  
**Last Updated**: 2025-10-28

