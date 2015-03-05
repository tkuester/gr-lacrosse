#!/usr/bin/env python
import sys
import math
import socket
import crcmod

if len(sys.argv) != 2:
    print 'Usage: %s [temp_f]' % sys.argv[0]
    print '  ex: %s -18.2' % sys.argv[0]
    sys.exit(1)

temp_f = float(sys.argv[1])
temp_c = (temp_f - 32) / 1.8

temp_scale = int((temp_c + 40.000001) / 10)
temp_val = ((temp_c + 40) - (temp_scale * 10.0)) / 0.0646332607
temp_val = int(round(temp_val))

print 'Temp C: %3.1f' % temp_c
print 'Scale: %d' % temp_scale
print 'Val: 0x%02x (%d)' % (temp_val, temp_val)

dat = bytearray([0x2d, 0xd4, 0x95, 0xa0 | temp_scale, temp_val, 0x6a])
print 'Packet:', str(dat).encode('hex')
calc_checksum = crcmod.mkCrcFun(0x131, initCrc=0x3a, rev=False)
csum = calc_checksum(str(dat))

packet = bytearray([0x00] * 128 + [0x10] + [0xaa] * 4)
packet += dat
packet += bytearray([csum] + [0xaa]*2 + [0x00] * 22)

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect(('localhost', 52001))
ret = cs.send(str(packet))
cs.close()

print ret, len(packet)
