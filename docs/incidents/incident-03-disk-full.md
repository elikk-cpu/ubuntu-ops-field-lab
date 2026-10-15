# INC-03 — No Space Left on Device

## Status
Resolved (controlled LAB 01 incident).

## Environment
- Host: ubuntu-ops-01
- Storage: VMware virtual disks, LVM, ext4
- Isolated filesystem: /dev/loop0
- Mount point: /mnt/lab01-inc03
- Filesystem image: 64 MiB
- Date: 2026-10-14 (UTC)

## Symptoms
A 70 MiB write operation failed with:

No space left on device

The dd command returned exit code 1.

## Investigation
The isolated ext4 filesystem showed:

- Total usable capacity: 56 MiB
- Available before failure: 52 MiB
- Available during incident: 0
- Filesystem usage: 100%
- Free inodes: 16371
- Test directory size: 52 MiB

## Root Cause
The test file exhausted the available data blocks
of the isolated ext4 filesystem.

The problem was not inode exhaustion.

## Resolution
Removed the temporary fill.bin file.

Available space recovered to approximately 52 MiB,
with filesystem usage returning to 1%.

## Recovery Verification
- New file creation: PASS
- Recovery file content: recovery-ok
- Original LVM SHA256: OK
- Filesystem unmounted successfully
- Loop device released
- Temporary filesystem image removed

## Prevention and Lessons Learned
- Monitor filesystem capacity with df -hT.
- Check inode availability with df -i.
- Identify large files and directories with du.
- Use disk usage alerts before capacity reaches 100%.
- Keep temporary data and tests isolated.
- Verify data integrity after recovery.

## Evidence
[Disk exhaustion and recovery](../evidence/incident-03-disk-full.txt)
