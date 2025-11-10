# Deployment Patterns - Pattern Library

Reference deployment patterns. Use AFTER understanding functionality (see SKILL.md Steps 1-2).

## Deployment Pattern Library

### Pattern 1: Blue-Green Deployment

**Use when**: Zero-downtime deployment needed for functionality.

**Example**:

```bash
# Deploy to green environment (new version)
npm run deploy:green

# Verify functionality works
curl https://green.example.com/api/files/upload -X POST -F "file=@test.pdf"
# Expected: 200 OK

# Switch traffic to green
aws elbv2 modify-listener --listener-arn arn:aws:elasticloadbalancing:... --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...:targetgroup/green/...

# Monitor functionality
watch -n 5 'curl https://api.example.com/metrics | jq ".upload.success_rate"'
# Expected: > 95%

# Rollback if functionality broken (switch back to blue)
if [ $(curl -s https://api.example.com/metrics | jq ".upload.success_rate") -lt 95 ]; then
  aws elbv2 modify-listener --listener-arn arn:aws:elasticloadbalancing:... --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...:targetgroup/blue/...
fi
```

### Pattern 2: Canary Deployment

**Use when**: Gradual rollout needed to test functionality at scale.

**Example**:

```bash
# Deploy canary version (5% of traffic)
kubectl set image deployment/file-upload file-upload=file-upload:v2
kubectl scale deployment/file-upload-canary --replicas=1

# Route 5% of traffic to canary
kubectl apply -f canary-traffic-split.yaml
# Expected: 5% traffic to canary, 95% to stable

# Monitor functionality metrics
watch -n 5 'curl https://api.example.com/metrics | jq ".upload.success_rate"'
# Expected: > 95%

# Increase canary traffic if functionality works
if [ $(curl -s https://api.example.com/metrics | jq ".upload.success_rate") -ge 95 ]; then
  kubectl apply -f canary-traffic-split-25.yaml
  # Expected: 25% traffic to canary
fi

# Rollback if functionality broken
if [ $(curl -s https://api.example.com/metrics | jq ".upload.success_rate") -lt 95 ]; then
  kubectl delete deployment/file-upload-canary
  # Expected: All traffic back to stable
fi
```

### Pattern 3: Feature Flag Deployment

**Use when**: Instant rollback needed for functionality.

**Example**:

```bash
# Deploy with feature flag disabled
export FILE_UPLOAD_ENABLED=false
npm run deploy:production

# Enable feature flag for 10% of users
curl -X POST https://feature-flags.example.com/flags/file-upload -d '{"enabled": true, "rollout_percent": 10}'

# Monitor functionality
watch -n 5 'curl https://api.example.com/metrics | jq ".upload.success_rate"'
# Expected: > 95%

# Increase rollout if functionality works
if [ $(curl -s https://api.example.com/metrics | jq ".upload.success_rate") -ge 95 ]; then
  curl -X POST https://feature-flags.example.com/flags/file-upload -d '{"enabled": true, "rollout_percent": 50}'
fi

# Rollback if functionality broken (disable feature flag)
if [ $(curl -s https://api.example.com/metrics | jq ".upload.success_rate") -lt 95 ]; then
  curl -X POST https://feature-flags.example.com/flags/file-upload -d '{"enabled": false}'
  # Expected: Functionality disabled instantly
fi
```

## Rollback-Ready Design Patterns

**1. Feature Flags**

```typescript
// Every new feature behind a flag
const isEnabled = process.env.NEW_AUTH_ENABLED === "true";
if (isEnabled) {
  return newAuthFlow(user);
}
return legacyAuthFlow(user);
```

**2. Backward-Compatible Migrations**

```javascript
// ADD columns, don't REMOVE
// NEW tables, don't MODIFY existing
// Can rollback code without DB rollback
await db.schema.alterTable("users", (table) => {
  table.string("new_field").nullable(); // Nullable for compatibility
});
```

**3. Configuration-Driven Behavior**

```javascript
// Allow runtime changes without code deploy
const config = {
  maxRetries: process.env.MAX_RETRIES || 3,
  timeout: process.env.API_TIMEOUT || 5000,
};
```
