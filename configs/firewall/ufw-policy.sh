#!/usr/bin/env bash
set -euo pipefail

# LAB 01 - UFW network access policy
#
# Host: ubuntu-ops-01
# Management: ens34 / 172.28.50.10
# Allowed SSH client: 172.28.50.1
#
# Run only after validating interface addresses
# and ensuring VMware console access.

if [[ $EUID -ne 0 ]]; then
    echo "ERROR: Run as root." >&2
    exit 1
fi

# Default firewall policies
ufw default deny incoming
ufw default allow outgoing

# SSH administration via management network only
ufw allow in on ens34 \
    from 172.28.50.1 \
    to 172.28.50.10 \
    port 22 proto tcp

# Activation is intentionally manual.
# Review the rules before running: ufw enable
ufw show added
