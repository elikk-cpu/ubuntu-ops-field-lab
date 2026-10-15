# LAB 01 — Verification Protocol

## 1. Status

All planned technical LAB 01 verification exercises have been completed. Final documentation review and GitHub publication remain.

File permission verification: 8/8 tests passed.

Test date: 2026-10-12.
Time reference: UTC, as recorded in evidence.

## 2. Initial State

Host: ubuntu-ops-01
OS: Ubuntu Server 24.04.5 LTS

Accounts:
- ubuntu — administrator
- developer — member of app-developers
- operator — member of app-operators

Directories:
- /srv/ubuntu-ops/app
  Owner: root
  Group: app-developers
  Mode: 2770

- /srv/ubuntu-ops/reports
  Owner: root
  Group: app-operators
  Mode: 2750

Test file:
- /srv/ubuntu-ops/reports/sample-report.txt
  Owner: root
  Group: app-operators
  Mode: 0640

These tests verify standard Linux DAC permissions.
ACL-01 through ACL-08 are test identifiers,
not extended POSIX ACL rules.

## 3. Tests ACL-01–ACL-05

### ACL-01 — Developer Creates Application File

Initial state: developer belongs to app-developers.
Test: create dev-evidence.txt as developer.
Expected: successful write and group inheritance.
Actual: exit code 0; owner developer;
group app-developers; mode 664.
Result: PASS.

### ACL-02 — Operator Cannot Write to Application Directory

Initial state: operator is not in app-developers.
Test: attempt to create operator-evidence.txt.
Expected: Permission denied; file remains absent.
Actual: exit code 1; file absent check 0.
Result: PASS.

### ACL-03 — Developer Cannot List Reports

Initial state: developer is not in app-operators.
Test: list /srv/ubuntu-ops/reports.
Expected: Permission denied.
Actual: exit code 2.
Result: PASS.

### ACL-04 — Operator Can List Reports

Initial state: operator belongs to app-operators.
Test: list files in the reports directory.
Expected: successful listing.
Actual: exit code 0.
Result: PASS.

### ACL-05 — Operator Cannot Create Reports

Initial state: app-operators lacks directory write permission.
Test: attempt to create operator-evidence.txt.
Expected: Permission denied; file remains absent.
Actual: exit code 1; file absent check 0.
Result: PASS.

Evidence: [ACL-01–05](evidence/acl-01-05.txt).

## 4. Tests ACL-06–ACL-08

### ACL-06 — Operator Reads Report

Initial state: file owned by root:app-operators, mode 0640.
Test: read sample-report.txt as operator.
Expected: successful read.
Actual: exit code 0; content returned.
Result: PASS.

### ACL-07 — Report Integrity Protection

Initial state: operator has read-only file access.
Test: attempt to append Modified to sample-report.txt.
Expected: Permission denied; SHA256 unchanged.
Actual: exit code 2; SHA256 matched before and after.
Result: PASS.

### ACL-08 — Developer Cannot Read Report

Initial state: developer is not in app-operators.
Test: read sample-report.txt as developer.
Expected: Permission denied.
Actual: exit code 1.
Result: PASS.

Evidence: [ACL-06–08](evidence/acl-06-08.txt).

## 5. Conclusions

All eight file permission tests produced the expected results.

Confirmed:
- Group-based access separation
- SGID group inheritance
- Unauthorized write prevention
- Authorized report reading
- Test file integrity preservation

The default umask 0002 produced file mode 0664.
A temporary umask 0007 produced file mode 0660.
SGID group inheritance and access restrictions were verified.
Unauthorized system file modification was denied.

Evidence: [Final permission tests](evidence/permissions-final.txt).

## 6. Verification Completion Status

Technical verification completed by 2026-10-14:

- SSH and UFW security checks
- DAC, SGID, umask, and unauthorized write checks
- Restricted sudo and actual API service restart
- LVM expansion, persistence, and SHA256 integrity
- Systemd API recovery and reboot persistence
- Periodic systemd healthcheck timer
- CPU, memory, swap, and disk I/O diagnostics
- Three controlled incidents with RCA reports
- Windows SSH tests and saved client transcript

Remaining project tasks:

- Final bilingual documentation review
- Repository consistency checks
- Git commit and GitHub push

## 7. Sudo Privilege Verification

Test date: 2026-10-12.

Initial state:
- ubuntu has full administrative sudo privileges.
- developer has no sudo privileges.
- operator initially had no sudo privileges.

Configured policy:
- operator may restart ubuntu-ops-api.service as root.
- No general systemctl or unrestricted sudo access is granted.
- The sudoers file is owned by root:root with mode 0440.
- Full sudoers syntax validation passed.

Test results:
- SUDO-01: API restart authorization; exit 0; PASS.
- SUDO-02: SSH restart authorization denied; exit 1; PASS.
- SUDO-03: Developer API restart not authorized; exit 1; PASS.
- SUDO-04: Arbitrary root command not executed; exit 1; PASS.

The API service is installed and enabled.
An authorized restart by operator was successfully executed,
and the service process PID changed.

Evidence: [Sudo policy](evidence/sudo-policy.txt).

Configuration: [Operator sudoers](../configs/sudoers/ubuntu-ops-operator).

The operator was denied write permission on both
the systemd unit and the API source file.

Evidence: [Service file protection](evidence/sudo-service-file-protection.txt).

## 8. SSH Security Verification

Test date: 2026-10-12.

Initial state:
- OpenSSH was installed with password authentication enabled.
- The administrative user was ubuntu.
- Management address: 172.28.50.10/24.
- PasswordAuthentication was enabled by cloud-init.

Implemented changes:
- Generated a dedicated Ed25519 key pair on Windows.
- Installed the public key in ubuntu's authorized_keys.
- Restricted SSH directory and file permissions.
- Disabled password and keyboard-interactive authentication.
- Disabled direct root SSH login.
- Preserved public key authentication.

### SSH-01 — Public Key Authentication

Expected: successful login using the selected Ed25519 key
with password authentication disabled on the client.

Actual: successful SSH login as ubuntu.
Result: PASS.

### SSH-02 — Password Authentication Rejection

Expected: connection rejected when public key
authentication is disabled on the client.

Actual: Permission denied (publickey).
SSH client exit code: 255.
Result: PASS.

### SSH-03 — SSH Configuration Validation

Expected: valid configuration with public key authentication
enabled and password authentication disabled.

Actual:
- sshd syntax validation: exit code 0
- PubkeyAuthentication: yes
- PasswordAuthentication: no
- KbdInteractiveAuthentication: no
- PermitRootLogin: no

Result: PASS.

### SSH-04 — Post-Reboot Persistence

Expected: SSH accessibility and management network
configuration remain functional after reboot.

Actual:
- ssh.socket: enabled
- ssh.socket: active
- ens33: 10.50.0.128/24
- ens34: 172.28.50.10/24
- Remote SSH session established
- Effective SSH hardening settings preserved

Result: PASS.

## SSH Evidence

- [Server hardening](evidence/ssh-server-hardening.txt)
- [Post-reboot verification](evidence/ssh-post-reboot.txt)
- [SSH configuration](../configs/ssh/00-lab01-hardening.conf)

Positive and negative SSH authentication tests were
repeated from Windows. The client transcript was saved.

Evidence: [Windows SSH transcript](evidence/ssh-client.txt).

## Completed SSH Network Restrictions

- Administrative SSH restricted to the management network
- SSH access through the NAT interface blocked by UFW
- Firewall persistence verified after reboot
- Unauthorized network access tests completed

See Section 9 for firewall verification evidence.

## 9. Firewall Verification

Test date: 2026-10-12.

### Initial State

- UFW installed but inactive.
- No active nftables filtering rules.
- SSH listening on IPv4 and IPv6 interfaces.
- Management access required through VMnet11.

### Implemented Policy

- Default incoming: deny.
- Default outgoing: allow.
- SSH allowed only from 172.28.50.1 to
  172.28.50.10:22/tcp via ens34.
- UFW enabled at system startup.

### Verification Results

| ID | Test | Actual Result | Status |
|---|---|---|---|
| FW-01 | Management SSH connection | Allowed | PASS |
| FW-02 | NAT SSH connection | Blocked | PASS |
| FW-03 | UFW kernel log inspection | TCP/22 block confirmed | PASS |
| FW-04 | UFW after reboot | Enabled and active | PASS |
| FW-05 | Firewall rule persistence | Rule preserved | PASS |
| FW-06 | Management SSH after reboot | TCP connection successful | PASS |
| FW-07 | NAT SSH after reboot | TCP connection blocked | PASS |

### Evidence

- [Firewall before reboot](evidence/firewall-pre-reboot.txt)
- [Firewall after reboot](evidence/firewall-post-reboot.txt)
- [Windows TCP connectivity tests](evidence/firewall-client.csv)
- [Reproduction script](../configs/firewall/ufw-policy.sh)

The Windows CSV timestamps use the Windows host's
local time, while server logs use UTC.

### Conclusion

Administrative SSH access is permitted through
the dedicated management network.

SSH connections through the NAT interface are
blocked by UFW. Firewall rules persist after reboot.

The firewall policy script requires manual review
before activation and must not be executed blindly.

## 10. Systemd Healthcheck Timer

Test date: 2026-10-14.

Implemented:
- ubuntu-ops-healthcheck.service
- ubuntu-ops-healthcheck.timer
- HTTP endpoint: http://127.0.0.1:8080/health
- Healthcheck interval: approximately 5 minutes
- Service type: oneshot
- Execution user: developer

Verification:
- Unit syntax validation: PASS
- Manual healthcheck execution: PASS
- Timer enabled: PASS
- Timer active: PASS
- Automatic scheduled execution: PASS
- HTTP health response: status ok

The timer performs periodic checks without exposing
the HTTP API outside the loopback interface.

Evidence:
- [Systemd timer verification](evidence/systemd-timer.txt)

Configuration:
- [Healthcheck service](../configs/systemd/ubuntu-ops-healthcheck.service)
- [Healthcheck timer](../configs/systemd/ubuntu-ops-healthcheck.timer)

## 11. Performance Diagnostics

Test date: 2026-10-14.

### CPU

Environment: 2 virtual CPUs.

A controlled CPU workload was generated using yes
with a 15-second timeout.

Observed:
- CPU utilization increased during the test.
- The system returned to idle after the workload.
- No disk I/O wait problem was observed.
- HTTP API remained functional after testing.

Evidence: [CPU diagnostics](evidence/performance-cpu.txt).

### RAM and Swap

A controlled Python workload allocated and touched
approximately 256 MiB of memory.

Observed:
- Used RAM increased during the workload.
- Memory usage decreased after completion.
- Swap usage remained at zero.
- No swap-in or swap-out activity was observed.
- HTTP API remained functional.

Evidence: [Memory diagnostics](evidence/performance-memory.txt).

### Disk I/O

A temporary 512 MiB file was used for controlled
write and read tests on the LVM filesystem.

Observed:
- Write operation completed.
- Read operation completed.
- Original LVM test data retained its SHA256 hash.
- Temporary I/O test file was removed.
- Filesystem capacity returned to normal.

The observed transfer rates reflect this VMware
test environment and are not physical disk benchmarks.

Evidence: [Disk I/O diagnostics](evidence/performance-disk.txt).

### Conclusion

CPU, RAM, swap, and disk I/O diagnostic procedures
were exercised successfully.

These are controlled laboratory observations,
not production performance or capacity guarantees.

## 12. Incident Response and Root Cause Analysis

Test date: 2026-10-14.

Three controlled incidents were reproduced, investigated,
resolved, and documented.

### INC-01 — HTTP API Unavailable

Scenario:
The ubuntu-ops-api.service was deliberately stopped.

Symptoms:
- Service state: inactive (dead)
- HTTP connection refused
- curl exit code: 7

Root cause:
An explicit administrative systemctl stop operation.

Resolution:
The service was started using systemctl start.

Verification:
- Service state returned to active
- HTTP /health returned status ok
- Result: PASS

An explicit stop is different from an unexpected process
failure. Restart=on-failure does not override an
intentional administrator stop.

RCA: [INC-01 — API Unavailable](incidents/incident-01-api-unavailable.md).

### INC-02 — Permission Denied

Scenario:
The developer user attempted to modify a protected
configuration file under /etc.

Symptoms:
- Permission denied
- Configuration remained unchanged

Root cause:
The configuration file was owned by root:root
with mode 0644. The developer lacked write access.

Resolution:
An authorized administrator changed the configuration
using sudo tee, without granting additional privileges.

Verification:
- Original mode=production restored
- Developer write permission remained denied
- HTTP API health check passed
- Temporary test environment removed
- Result: PASS

RCA: [INC-02 — Permission Denied](incidents/incident-02-permission-denied.md).

Evidence: [Permission incident](evidence/incident-02-permissions.txt).

### INC-03 — No Space Left on Device

Scenario:
A 70 MiB write was attempted on an isolated
64 MiB ext4 filesystem image mounted via loop.

Symptoms:
- No space left on device
- Filesystem usage: 100%
- Available capacity: 0

Root cause:
Available filesystem data blocks were exhausted.
Free inodes remained available.

Resolution:
The temporary fill.bin file was removed.

Verification:
- Filesystem usage returned to 1%
- Approximately 52 MiB became available
- New file write succeeded: recovery-ok
- Original LVM data SHA256: OK
- Temporary loop filesystem removed
- Result: PASS

RCA: [INC-03 — Disk Full](incidents/incident-03-disk-full.md).

Evidence: [Disk incident](evidence/incident-03-disk-full.txt).

### Incident Response Conclusion

All three controlled incidents were resolved.

The exercises demonstrated service troubleshooting,
Linux permission diagnostics, filesystem capacity
analysis, recovery verification, and RCA documentation.

These incidents were created intentionally in a
laboratory environment and do not represent
production outages.
