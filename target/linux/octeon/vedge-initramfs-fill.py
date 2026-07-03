#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only
"""Post-link fill for the Cisco vEdge 1000 netboot initramfs-repair patch.

U-Boot on the vEdge 1000 overwrites a small, fixed-address window (~64 MiB
physical) of a large netboot initramfs with its console log after loading it,
breaking the (compressed) initramfs unpack. The kernel patch keeps a spare copy
of that window plus a checksum inside itself and restores it in an early
initcall. This script fills those in after the (initramfs) kernel is linked:

  - extract the correct VEDGE_REPAIR_WIN bytes at physical VEDGE_SCRATCH_PA out
    of the compressed initramfs embedded in the ELF,
  - compute an FNV-1a-32 of the whole initramfs,
  - write them, plus an "armed" marker, into the `vedge_repair` struct.

If the initramfs does not extend across VEDGE_SCRATCH_PA (a small image that
cannot be hit) the struct is left disarmed and the runtime repair is a no-op.

Usage: vedge-initramfs-fill.py <kernel.elf> <symbol-map>
  <symbol-map> is nm / System.map format ("<addr> <type> <name>").
"""
import re
import struct
import subprocess
import sys

BASE = 0xffffffff80000000	# MIPS64 CKSEG0: virtual = BASE + physical
SCRATCH_PA = 0x04000000		# must match VEDGE_SCRATCH_PA in the kernel patch
MAGIC = 0x56454447		# 'VEDG'
ARMED = 0x41524d44		# 'ARMD'


def die(msg):
	sys.stderr.write("vedge-fill: %s\n" % msg)
	sys.exit(1)


def main():
	if len(sys.argv) != 3:
		die("usage: %s <kernel.elf> <symbol-map>" % sys.argv[0])
	elf_path, symmap = sys.argv[1], sys.argv[2]

	syms = {}
	for ln in open(symmap):
		m = re.match(r'\s*([0-9a-fA-F]+)\s+\S\s+(\S+)\s*$', ln)
		if m:
			syms[m.group(2)] = int(m.group(1), 16)
	for want in ('__initramfs_start', '__initramfs_size', 'vedge_repair'):
		if want not in syms:
			die("symbol %s not found in %s" % (want, symmap))

	secs = []
	out = subprocess.check_output(['readelf', '-SW', elf_path]).decode()
	for ln in out.splitlines():
		m = re.match(r'\s*\[\s*\d+\]\s+\S+\s+\S+\s+([0-9a-f]{16})\s+'
			     r'([0-9a-f]+)\s+([0-9a-f]+)', ln)
		if m:
			a, o, s = (int(m.group(1), 16), int(m.group(2), 16),
				   int(m.group(3), 16))
			if a and s:
				secs.append((a, o, s))

	def v2f(v):
		for a, o, s in secs:
			if a <= v < a + s:
				return o + (v - a)
		die("vaddr 0x%x not in any section" % v)

	data = bytearray(open(elf_path, 'rb').read())

	irs_v = syms['__initramfs_start']
	size = struct.unpack('>Q', data[v2f(syms['__initramfs_size']):][:8])[0]
	irs_f = v2f(irs_v)
	ramfs_pa = irs_v - BASE
	off = SCRATCH_PA - ramfs_pa

	vpf = v2f(syms['vedge_repair'])
	if struct.unpack('>I', data[vpf:vpf + 4])[0] != MAGIC:
		die("vedge_repair magic mismatch at file off 0x%x" % vpf)
	win = struct.unpack('>I', data[vpf + 4:vpf + 8])[0]

	if off < 0 or off + win > size:
		print("vedge-fill: initramfs (pa 0x%x, %d bytes) does not reach 0x%x; "
		      "leaving repair disarmed" % (ramfs_pa, size, SCRATCH_PA))
		return

	good = bytes(data[irs_f + off:irs_f + off + win])
	h = 2166136261
	for b in data[irs_f:irs_f + size]:
		h = ((h ^ b) * 16777619) & 0xffffffff

	struct.pack_into('>I', data, vpf + 8, h)		# crc
	struct.pack_into('>I', data, vpf + 12, ARMED)		# armed
	data[vpf + 16:vpf + 16 + win] = good
	open(elf_path, 'wb').write(data)
	print("vedge-fill: armed; initramfs pa 0x%x size %d off 0x%x win 0x%x crc %08x"
	      % (ramfs_pa, size, off, win, h))


if __name__ == '__main__':
	main()
