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
- SSH public key authentication
- LVM and checksum verification
- systemd service and timer verification
- Post-reboot persistence testing
- CPU, RAM, swap, and disk I/O diagnostics
- Three incidents and root cause analyses

Overall LAB 01 acceptance is not yet complete.
