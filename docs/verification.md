# LAB 01 — Verification Protocol

## 1. Status

The laboratory is currently in progress.

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

The developer-created file has mode 664.
The effective restriction currently depends on the
parent directory. The umask policy requires further review.

## 6. Pending Verification

- Unauthorized system file modification test
- Least-privilege sudo verification
- LVM and checksum verification
- systemd service and timer verification
- Post-reboot persistence testing
- CPU, RAM, swap, and disk I/O diagnostics
- Three incidents and root cause analyses

Overall LAB 01 acceptance is not yet complete.

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

The API service is not yet installed. The permitted
operation was checked against sudo policy, not executed.

Evidence: [Sudo policy](evidence/sudo-policy.txt).

Configuration: [Operator sudoers](../configs/sudoers/ubuntu-ops-operator).

Pending: test the actual service restart and verify
that service files and executables cannot be modified
by the operator.

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

The positive and negative client authentication tests
were observed interactively; a stored client-side transcript
is still pending.

## Remaining Security Work

- Restrict administrative SSH access to the management network.
- Verify the SSH network restrictions after reboot.
- Test unauthorized sources.

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
