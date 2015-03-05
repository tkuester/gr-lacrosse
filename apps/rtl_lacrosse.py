#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Rtl Lacrosse
# Generated: Thu Mar  5 08:32:25 2015
##################################################

# Call XInitThreads as the _very_ first thing.
# After some Qt import, it's too late

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
import osmosdr
import reveng
import time

class rtl_lacrosse(gr.top_block):

    def __init__(self, rf_gain=25):
        gr.top_block.__init__(self, "Rtl Lacrosse")

        ##################################################
        # Parameters
        ##################################################
        self.rf_gain = rf_gain

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(915.1e6, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(rf_gain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.reveng_pattern_dump_0 = reveng.pattern_dump([1,0]*16, 24+8+8+8+8+16, "%Y-%m-%d %H:%M:%S,%[bits]", False, "", False)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=4,
                decimation=58,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 100e3, 50e3, firdes.WIN_HAMMING, 6.76))
        self.lacrosse_TX29U_0 = lacrosse.TX29U()
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(4, 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_rotator_cc_0 = blocks.rotator_cc(2*3.14*125e3/samp_rate)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.reveng_pattern_dump_0, 'out'), (self.lacrosse_TX29U_0, 'in'))    
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.blocks_rotator_cc_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.reveng_pattern_dump_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_rotator_cc_0, 0))    


    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.rtlsdr_source_0.set_gain(self.rf_gain, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 50e3, firdes.WIN_HAMMING, 6.76))
        self.blocks_rotator_cc_0.set_phase_inc(2*3.14*125e3/self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("-g", "--rf-gain", dest="rf_gain", type="intx", default=25,
        help="Set RF Gain [default=%default]")
    (options, args) = parser.parse_args()
    tb = rtl_lacrosse(rf_gain=options.rf_gain)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()
