#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: File Lacrosse
# Generated: Thu Dec 24 13:58:38 2015
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import lacrosse
import math
import reveng


class file_lacrosse(gr.top_block):

    def __init__(self, file_name="", freq_offset=0, samp_rate=int(1e6)):
        gr.top_block.__init__(self, "File Lacrosse")

        ##################################################
        # Parameters
        ##################################################
        self.file_name = file_name
        self.freq_offset = freq_offset
        self.samp_rate = samp_rate

        ##################################################
        # Blocks
        ##################################################
        self.reveng_pattern_dump_0 = reveng.pattern_dump([1,0]*16, 24+8+8+8+8+16, "%Y-%m-%d %H:%M:%S,%[bits]", False, "", False)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=4,
                decimation=58,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 200e3, 100e3, firdes.WIN_HAMMING, 6.76))
        self.lacrosse_TX29U_0 = lacrosse.TX29U()
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(4, 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(32, True)
        self.blocks_rotator_cc_0 = blocks.rotator_cc(2*math.pi*freq_offset/samp_rate)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, file_name, False)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.reveng_pattern_dump_0, 'out'), (self.lacrosse_TX29U_0, 'in'))    
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.blocks_file_source_0, 0), (self.blocks_rotator_cc_0, 0))    
        self.connect((self.blocks_rotator_cc_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.reveng_pattern_dump_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.dc_blocker_xx_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))    


    def get_file_name(self):
        return self.file_name

    def set_file_name(self, file_name):
        self.file_name = file_name
        self.blocks_file_source_0.open(self.file_name, False)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.blocks_rotator_cc_0.set_phase_inc(2*math.pi*self.freq_offset/self.samp_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_rotator_cc_0.set_phase_inc(2*math.pi*self.freq_offset/self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 200e3, 100e3, firdes.WIN_HAMMING, 6.76))


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("-f", "--file-name", dest="file_name", type="string", default="",
        help="Set File [default=%default]")
    parser.add_option("-o", "--freq-offset", dest="freq_offset", type="intx", default=0,
        help="Set Frequency Offset [default=%default]")
    parser.add_option("-r", "--samp-rate", dest="samp_rate", type="intx", default=int(1e6),
        help="Set Sample Rate [default=%default]")
    (options, args) = parser.parse_args()
    tb = file_lacrosse(file_name=options.file_name, freq_offset=options.freq_offset, samp_rate=options.samp_rate)
    tb.start()
    tb.wait()
