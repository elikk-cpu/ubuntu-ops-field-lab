# INC-01 — HTTP API Unavailable

## Status
Resolved (controlled LAB 01 incident).

## Environment
- Host: ubuntu-ops-01
- Service: ubuntu-ops-api.service
- Endpoint: http://127.0.0.1:8080/health
- Incident date: 2026-10-14 (UTC)

## Symptoms
- systemctl is-active returned inactive.
- HTTP health check failed with curl exit code 7.
- Connection to 127.0.0.1:8080 was refused.

## Investigation
systemctl status showed inactive (dead).

The journal recorded at 16:09:15 UTC:
- Stopping ubuntu-ops-api.service
- Deactivated successfully
- Stopped ubuntu-ops-api.service

The process received SIGTERM.

## Root Cause
The service was intentionally stopped using
systemctl stop during a controlled incident test.

Restart=on-failure does not automatically restart
a service after an intentional administrative stop.

## Resolution
Started the service using:

sudo systemctl start ubuntu-ops-api.service

## Verification
- Service state: active
- HTTP health check: successful
- API response:
  {"status": "ok", "service": "ubuntu-ops-api"}

## Prevention and Lessons Learned
- Restrict service stop permissions.
- Maintain health checks and review their logs.
- Consider adding failure alerts for unavailable services.
- Distinguish administrative stops from process crashes.
- Do not assume Restart=on-failure handles every outage.
