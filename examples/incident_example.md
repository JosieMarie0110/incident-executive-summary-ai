# Example Incident Executive Summary

### Executive Summary
On March 3rd, the API Gateway experienced elevated error rates for approximately 32 minutes due to a memory leak introduced during a recent deployment. Approximately 25% of requests failed during the incident window. Engineering teams quickly identified the issue and rolled back the deployment, restoring service.

No data loss occurred. Additional monitoring has been implemented to detect similar conditions earlier.

### Customer Impact
- Duration: 32 minutes
- Services affected: API Gateway
- Who was impacted: ~25% of API requests
- What users experienced: intermittent request failures (500 errors)
- Data integrity: No impact

### Timeline
- Detection: 02:10 UTC — automated monitoring alert
- Investigation: 02:18 UTC — engineering engaged
- Root cause identified: 02:30 UTC — memory leak discovered
- Resolution: 02:42 UTC — deployment rollback restored service

### Root Cause (Plain English)
- A software deployment introduced a memory leak in the API service
- As memory consumption increased, requests began failing

### Mitigations Applied
- Deployment rollback
- Service restart
- Monitoring review

### Prevention / Next Steps
- Add memory utilization alerts
- Implement automated rollback safeguards
- Improve deployment validation tests

### Customer-facing Update (Email-ready)

Subject: Service disruption update

Hi team,

Earlier today we experienced a service disruption affecting the API Gateway for approximately 32 minutes. During this time, some requests may have failed.

Our engineering team quickly identified the issue and rolled back the deployment that introduced the problem. Service has been fully restored and no data was impacted.

We are implementing additional safeguards to reduce the likelihood of recurrence.

Please let us know if you have any questions.

Best regards  
Customer Success Team
