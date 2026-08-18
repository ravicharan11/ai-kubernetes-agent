# Test Failure Scenarios

This document describes common Kubernetes failure scenarios you can use to test the AI Kubernetes Agent.

## Scenario 1 — CrashLoopBackOff

### Cause
Missing environment variable or configuration.

### How to Reproduce
```bash
# Create a deployment with missing env var
kubectl create deployment test-app --image=nginx:latest
kubectl set env deployment/test-app MISSING_VAR=required
kubectl delete pod -l app=test-app
```

### Expected AI Diagnosis
- **Root Cause**: Missing environment variable
- **Explanation**: Application failed during startup due to missing required configuration
- **Suggested Fix**: Add missing environment variable using ConfigMap or Secret
- **Command**: `kubectl edit deployment test-app`
- **Confidence**: High (90%+)

---

## Scenario 2 — ImagePullBackOff

### Cause
Invalid or non-existent image tag.

### How to Reproduce
```bash
# Create deployment with wrong image
kubectl create deployment bad-image --image=nginx:nonexistent-tag-12345
```

### Expected AI Diagnosis
- **Root Cause**: Invalid image tag or repository
- **Explanation**: Container runtime cannot pull the specified image
- **Suggested Fix**: Update deployment with correct image tag
- **Command**: `kubectl set image deployment/bad-image nginx=nginx:latest`
- **Confidence**: High (95%+)

---

## Scenario 3 — OOMKilled

### Cause
Container exceeded memory limits.

### How to Reproduce
```bash
# Create deployment with low memory limit
kubectl create deployment memory-hog --image=polinux/stress
kubectl set resources deployment/memory-hog --limits=memory=64Mi
kubectl set env deployment/memory-hog -- "-m 128m --vm 1 --vm-bytes 128M"
```

### Expected AI Diagnosis
- **Root Cause**: Container exceeded memory limit
- **Explanation**: Pod was killed due to Out of Memory (OOM)
- **Suggested Fix**: Increase memory requests/limits in deployment
- **Command**: `kubectl set resources deployment/memory-hog --limits=memory=256Mi`
- **Confidence**: High (90%+)

---

## Scenario 4 — Service Selector Mismatch

### Cause
Service selector does not match pod labels.

### How to Reproduce
```bash
# Create deployment
kubectl create deployment webapp --image=nginx --replicas=3

# Create service with wrong selector
kubectl expose deployment webapp --port=80 --type=ClusterIP
kubectl patch svc webapp -p '{"spec":{"selector":{"app":"wrong-label"}}}'
```

### Expected AI Diagnosis
- **Root Cause**: Service selector does not match pod labels
- **Explanation**: Service cannot route traffic to pods due to label mismatch
- **Suggested Fix**: Update service selector to match pod labels
- **Command**: `kubectl patch svc webapp -p '{"spec":{"selector":{"app":"webapp"}}}'
- **Confidence**: Medium (70-80%)

---

## Scenario 5 — Pending State (Insufficient Resources)

### Cause
Cluster lacks sufficient CPU/memory resources.

### How to Reproduce
```bash
# Create deployment with high resource requests
kubectl create deployment big-app --image=nginx
kubectl set resources deployment/big-app --requests=cpu=10,memory=10Gi
```

### Expected AI Diagnosis
- **Root Cause**: Insufficient cluster resources
- **Explanation**: Pod cannot be scheduled due to high resource requirements
- **Suggested Fix**: Reduce resource requests or add more nodes to cluster
- **Command**: `kubectl set resources deployment/big-app --requests=cpu=500m,memory=512Mi`
- **Confidence**: High (85%+)

---

## Scenario 6 — Readiness Probe Failure

### Cause
Application not ready within probe timeout.

### How to Reproduce
```bash
# Create deployment with failing readiness probe
kubectl create deployment probe-fail --image=nginx
kubectl set deployment probe-fail --image=nginx
kubectl patch deployment probe-fail -p '{"spec":{"template":{"spec":{"containers":[{"name":"nginx","readinessProbe":{"httpGet":{"path":"/health","port":8080},"initialDelaySeconds":5,"periodSeconds":10}}]}}}}'
```

### Expected AI Diagnosis
- **Root Cause**: Readiness probe failing
- **Explanation**: Container not passing readiness checks, not receiving traffic
- **Suggested Fix**: Fix readiness probe configuration or application health endpoint
- **Command**: `kubectl edit deployment probe-fail`
- **Confidence**: Medium (75-85%)

---

## Testing Checklist

When testing the AI Kubernetes Agent, verify:

- [ ] Cluster selection works (kubeconfig and AWS EKS)
- [ ] Investigation progress displays correctly
- [ ] Error messages are beginner-friendly
- [ ] Root cause identification is accurate
- [ ] Suggested fixes are actionable
- [ ] kubectl commands are correct
- [ ] Confidence scores are reasonable
- [ ] Healthy cluster shows empty state
- [ ] Investigation history saves correctly
- [ ] Loading states work properly

---

## Tips for Testing

1. **Start with a healthy cluster** - Verify baseline behavior
2. **Test one scenario at a time** - Clean up between tests
3. **Check logs** - Review backend logs for investigation details
4. **Verify kubectl access** - Ensure proper permissions
5. **Test with different clusters** - Validate multi-cluster support
6. **Monitor resource usage** - Ensure agent doesn't overload cluster

## Cleanup Commands

```bash
# Clean up test deployments
kubectl delete deployment test-app bad-image memory-hog webapp big-app probe-fail
kubectl delete svc webapp
```
