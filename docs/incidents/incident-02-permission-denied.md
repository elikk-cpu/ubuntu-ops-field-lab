# INC-02 — Permission Denied

## Status
Resolved (controlled LAB 01 incident).

## Environment
- Host: ubuntu-ops-01
- User: developer
- File: /etc/ubuntu-ops-lab01-incident02/settings.conf
- Date: 2026-10-14 (UTC)

## Symptoms
The developer attempted to append configuration data.
Linux returned Permission denied.

## Investigation
- File owner: root:root
- File permissions: 0644
- Parent directories: 0755
- Developer belongs to app-developers, not root.
- The original configuration remained unchanged.

## Root Cause
The developer lacked write permission on a
root-owned configuration file.

## Resolution
An authorized administrator modified the file
using sudo tee without changing its ownership
or permissions.

The original mode=production configuration
was restored after testing.

## Verification
- Developer write attempt: DENIED
- File permissions: 0644 root:root
- Restored configuration: mode=production
- HTTP API health check: PASS
- Temporary test environment: removed

## Lessons Learned
- Diagnose permissions with stat and namei.
- Follow the principle of least privilege.
- Avoid chmod 777 and unnecessary sudo grants.
- Use authorized deployment procedures.
- Verify configuration integrity after changes.

## Evidence
[Permission verification](../evidence/incident-02-permissions.txt)
