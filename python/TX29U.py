#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr
import pmt
import crcmod

class TX29U(gr.sync_block):
    """
    docstring for block TX29U
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="TX29U",
            in_sig=None,
            out_sig=None)

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.calc_checksum = crcmod.mkCrcFun(0x131, initCrc=0x3a, rev=False)

    def handle_msg(self, msg_pmt):
        msg = pmt.to_python(msg_pmt)
        msg = msg[1]

        bytez = bytearray()
        for i in xrange(7):
            bytez.append(int(msg[8*i:8*(i+1)], 2))

        dev_id = bytez[0:3]
        cfg = bytez[3]
        temp_scale = cfg & 0x0f
        temp = bytez[4]
        hum = bytez[5]
        csum = bytez[6]
        temp_c = -40 + (10 * temp_scale) + (temp * 0.0646332607)
        temp_f = temp_c * 1.8 + 32

        print 'Packet:', str(bytez).encode('hex')
        print
        print 'ID?', str(dev_id).encode('hex')
        print 'Cfg? 0x%02x (Temp Scale: %d)' % (cfg, cfg & 0x0f)
        print 'Temp: 0x%02x (%d)' % (temp, temp)
        print 'Humidity? 0x%02x (%d)' % (hum, hum)
        print 'Checksum:', hex(csum),
        if csum == self.calc_checksum(str(bytez[0:6])):
            print '[ OK ]'
        else:
            print '[FAIL]'
        print
        print '%3.1f C / %3.1f F' % (temp_c, temp_f)
        print '-'*30

    def work(self, input_items, output_items):
        return 0
