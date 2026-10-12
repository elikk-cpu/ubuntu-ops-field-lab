# LAB 01 — Installation and Environment Setup

## 1. Purpose

This document describes how to reproduce the Ubuntu Server infrastructure used in LAB 01.

The environment runs locally on VMware Workstation without requiring a paid cloud provider.

The installation establishes the baseline for further Linux administration, access control, LVM storage, systemd services, and troubleshooting experiments.

## 2. Prerequisites

Required components:

- Windows host operating system
- VMware Workstation 25H2
- Ubuntu Server 24.04.5 LTS ISO (AMD64)
- Available resources for one VM: 2 vCPU, 2 GiB RAM, and 32 GB of provisioned virtual disk capacity
- SSH client on the Windows host

The installation ISO was downloaded from the official Ubuntu release repository.

The image integrity should be checked against the official SHA256SUMS file before installation.

## 3. Virtual Machine Configuration

Create a new virtual machine using the advanced configuration wizard.

| Parameter | Value |
|---|---|
| VM name | ubuntu-ops-01 |
| Guest OS | Ubuntu 64-bit |
| Firmware | Legacy BIOS |
| Processor | 2 vCPU |
| Memory | 2048 MB |
| SCSI controller | LSI Logic |
| System disk | 20 GB |
| Data disk 1 | 6 GB |
| Data disk 2 | 6 GB |
| Primary network | VMnet10 — NAT |
| Secondary network | VMnet11 — Host-only |

All virtual disks use the SCSI interface.

The virtual disk files are configured without full space preallocation.

The system disk is 20 GB instead of the 18 GB specified in the original lab requirements. This is a documented deviation.

## 4. VMware Network Configuration

### 4.1 NAT Network

Configure VMnet10:

- Network type: NAT
- Subnet: `10.50.0.0/24`
- VMware DHCP: enabled
- Host virtual adapter: connected

The first VM network adapter must be explicitly assigned to VMnet10 using the Custom network option.

During installation, the server received `10.50.0.128/24` through DHCP.

This address is not guaranteed to remain unchanged.

### 4.2 Management Network

Configure VMnet11:

- Network type: Host-only
- Subnet: `172.28.50.0/24`
- VMware DHCP: disabled
- Host virtual adapter: enabled

Assign the second VM network adapter explicitly to VMnet11.

The Windows management adapter uses `172.28.50.1/24`.

## 5. Ubuntu Server Installation

Boot the VM from the Ubuntu Server installation ISO.

Use the standard Ubuntu Server installation rather than the minimized variant.

Do not install additional featured server snaps.

### 5.1 Disk Partitioning

Select the 20 GB system disk `/dev/sda`.

Use the guided disk layout with LVM disabled for the operating system.

The installer creates:

- BIOS boot partition (approximately 1 MB)
- ext4 root filesystem mounted at `/`

Leave `/dev/sdb` and `/dev/sdc` unallocated.

These disks will be used for the separate LVM storage exercise.

### 5.2 Initial User

Configure:

- Hostname: `ubuntu-ops-01`
- Administrator username: `ubuntu`
- Authentication: local password

Do not place passwords in the repository.

### 5.3 SSH Installation

Install OpenSSH Server during the Ubuntu installation.

Password authentication is temporarily enabled for initial access.

SSH key authentication and password-login restrictions will be configured in later stages.

## 6. Static Management Address

Ubuntu uses Netplan for network configuration.

Create `/etc/netplan/90-management.yaml`:

```yaml
network:
  version: 2
  ethernets:
    ens34:
      dhcp4: false
      addresses:
        - 172.28.50.10/24
      optional: true
```

Restrict access to the configuration file:

```bash
sudo chmod 600 /etc/netplan/90-management.yaml
```

Validate and apply:

```bash
sudo netplan generate
sudo netplan try --timeout 120
```

Confirm the configuration when connectivity is preserved.

No additional default gateway is configured on the management interface.

## 7. Initial Verification

Inspect the operating system:

```bash
cat /etc/os-release
```

Inspect disks:

```bash
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINTS
```

Inspect interfaces and routes:

```bash
ip -br addr
ip route
```

Check SSH:

```bash
systemctl is-active ssh
systemctl is-enabled ssh
```

Connect from Windows:

```powershell
ssh ubuntu@172.28.50.10
```

The initial SSH connection and post-reboot checks were successful.

External Internet connectivity and repository access require separate verification.

## 8. Recovery Checkpoint

A VMware snapshot named `LAB01-01-Clean-OS-Network-SSH` is planned as the initial recovery checkpoint.

Its creation and identification must be confirmed in VMware Snapshot Manager before recording this step as complete.

Snapshots are not substitutes for independent backups.

## 9. Known Limitations

- A single VM provides no high availability.
- SSH password authentication is not yet disabled.
- LVM service storage has not yet been implemented.
- External package repository connectivity has not yet been independently verified.
- Further hardening and permission checks remain pending.
