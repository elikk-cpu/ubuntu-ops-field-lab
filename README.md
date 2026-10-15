# Ubuntu Operations Lab — DevOps Portfolio

[English](README.md) | [Русский](README_RU.md)

A hands-on Linux infrastructure and operations project built with Ubuntu Server 24.04.5 LTS and VMware Workstation.

The lab demonstrates Linux administration, network security, access control, storage management, service operations, performance troubleshooting, and incident response.

## Project Status

**LAB 01 — Technical implementation and testing completed.**

Final documentation review and GitHub publication are in progress.

The final infrastructure checks were performed on 2026-10-14.

## Infrastructure Overview

| Component | Implementation |
|---|---|
| Hypervisor | VMware Workstation |
| Operating system | Ubuntu Server 24.04.5 LTS |
| Virtual machine | `ubuntu-ops-01` |
| Compute | 2 vCPU, 2 GiB RAM |
| Networking | NAT + Host-only management |
| Remote administration | OpenSSH with Ed25519 keys |
| Firewall | UFW |
| Access control | Linux DAC, groups, SGID, sudo |
| Storage | LVM with ext4 |
| Application | Python HTTP health API |
| Service manager | systemd |
| Monitoring | systemd healthcheck timer |

## Network Architecture

The virtual machine uses two network interfaces:

- **ens33:** VMware NAT network for outbound connectivity.
- **ens34:** Host-only management network, `172.28.50.10/24`.

The Windows host accesses Ubuntu through the dedicated management network at `172.28.50.1`.

SSH is restricted to authorized management access. The HTTP API listens exclusively on `127.0.0.1:8080` and is not exposed to external networks.

See [Architecture](docs/architecture.md).

## Implemented Features

### 1. Linux Access Control

- Created separate `developer` and `operator` accounts.
- Configured dedicated application and operations groups.
- Implemented directory permissions and SGID inheritance.
- Verified eight positive and negative DAC tests.
- Tested umask `0002` and a stricter umask `0007`.
- Protected system configuration against unauthorized changes.
- Restricted operator sudo access to a specific API restart.

### 2. SSH and Firewall Security

- Configured Ed25519 public key authentication.
- Disabled SSH password authentication.
- Disabled direct root SSH login.
- Applied UFW default-deny incoming policy.
- Restricted administrative SSH to the management network.
- Verified allowed and denied connections.
- Confirmed configuration persistence after reboot.

### 3. LVM Storage Operations

- Created an LVM volume group using additional virtual disks.
- Created and mounted an ext4 logical volume.
- Expanded the logical volume online from approximately 6 GiB to 12 GiB.
- Configured persistent mounting.
- Verified data integrity using SHA256.
- Confirmed storage availability after reboot.

See [Storage Operations](docs/storage.md).

### 4. Systemd Service Operations

- Deployed a Python HTTP API as a systemd service.
- Configured a dedicated non-root service account.
- Applied systemd security restrictions.
- Configured automatic recovery after process failure.
- Tested service restart authorization and recovery.
- Verified service startup after reboot.
- Implemented a periodic healthcheck using a systemd timer.

Health endpoint: `http://127.0.0.1:8080/health`

Example response:

```json
{"status": "ok", "service": "ubuntu-ops-api"}
```

See [Systemd Operations](docs/systemd.md).

### 5. Performance Diagnostics

Performed controlled troubleshooting exercises covering:

- CPU utilization and load.
- RAM consumption.
- Swap activity.
- Disk read and write operations.
- Filesystem capacity and inode usage.

Tests were conducted inside the VMware laboratory and are not production performance benchmarks.

### 6. Incident Response

Three controlled incidents were reproduced and resolved.

| ID | Incident | Root Cause | Result |
|---|---|---|---|
| INC-01 | HTTP API unavailable | Explicit systemd service stop | Resolved |
| INC-02 | Permission denied | Insufficient file write permissions | Resolved |
| INC-03 | No space left on device | Filesystem data block exhaustion | Resolved |

Each incident includes an English and Russian RCA report.

## Documentation

| Document | English | Russian |
|---|---|---|
| Architecture | [EN](docs/architecture.md) | [RU](docs/architecture_RU.md) |
| Installation | [EN](docs/installation.md) | [RU](docs/installation_RU.md) |
| Verification | [EN](docs/verification.md) | [RU](docs/verification_RU.md) |
| Storage | [EN](docs/storage.md) | [RU](docs/storage_RU.md) |
| Systemd | [EN](docs/systemd.md) | [RU](docs/systemd_RU.md) |

### Incident Reports

| Incident | English | Russian |
|---|---|---|
| INC-01 | [RCA](docs/incidents/incident-01-api-unavailable.md) | [RCA RU](docs/incidents/incident-01-api-unavailable_RU.md) |
| INC-02 | [RCA](docs/incidents/incident-02-permission-denied.md) | [RCA RU](docs/incidents/incident-02-permission-denied_RU.md) |
| INC-03 | [RCA](docs/incidents/incident-03-disk-full.md) | [RCA RU](docs/incidents/incident-03-disk-full_RU.md) |

## Verification Evidence

Test outputs and operational evidence are available in [docs/evidence/](docs/evidence/).

The evidence includes access-control tests, firewall verification, LVM integrity checks, systemd diagnostics, performance observations, and incident recovery results.

## Quick Health Verification

Run these commands inside the Ubuntu VM:

```bash
systemctl is-active ubuntu-ops-api.service
systemctl is-active ubuntu-ops-healthcheck.timer
curl -fsS http://127.0.0.1:8080/health
df -hT /srv/ubuntu-ops/data
```

## Skills Demonstrated

Linux Administration · Ubuntu Server · VMware · SSH Hardening · UFW · Linux Permissions · Least Privilege · Sudoers · LVM · ext4 · systemd · Bash · Python · Troubleshooting · Monitoring · Incident Response · Root Cause Analysis · Git

## Project Scope

This repository documents an educational infrastructure laboratory. It demonstrates operational procedures, troubleshooting methodology, security practices, and verification evidence.

It is not a production deployment guide.
