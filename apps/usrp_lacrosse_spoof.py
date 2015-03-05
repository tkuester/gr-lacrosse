#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Usrp Lacrosse Spoof
# Generated: Thu Mar  5 08:31:57 2015
##################################################

# Call XInitThreads as the _very_ first thing.
# After some Qt import, it's too late
import ctypes
import sys
if sys.platform.startswith('linux'):
    try:
        x11 = ctypes.cdll.LoadLibrary('libX11.so')
        x11.XInitThreads()
    except:
        print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import fosphor
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import PyQt4.Qwt5 as Qwt
import lacrosse
import math
import reveng
import sip
import sys
import time

from distutils.version import StrictVersion
class usrp_lacrosse_spoof(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Usrp Lacrosse Spoof")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Usrp Lacrosse Spoof")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "usrp_lacrosse_spoof")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6
        self.output_gain = output_gain = 30

        ##################################################
        # Blocks
        ##################################################
        self._output_gain_layout = Qt.QVBoxLayout()
        self._output_gain_tool_bar = Qt.QToolBar(self)
        self._output_gain_layout.addWidget(self._output_gain_tool_bar)
        self._output_gain_tool_bar.addWidget(Qt.QLabel("Output Gain"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._output_gain_counter = qwt_counter_pyslot()
        self._output_gain_counter.setRange(0, 80, 1)
        self._output_gain_counter.setNumButtons(2)
        self._output_gain_counter.setValue(self.output_gain)
        self._output_gain_tool_bar.addWidget(self._output_gain_counter)
        self._output_gain_counter.valueChanged.connect(self.set_output_gain)
        self._output_gain_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._output_gain_slider.setRange(0, 80, 1)
        self._output_gain_slider.setValue(self.output_gain)
        self._output_gain_slider.setMinimumWidth(200)
        self._output_gain_slider.valueChanged.connect(self.set_output_gain)
        self._output_gain_layout.addWidget(self._output_gain_slider)
        self.top_layout.addLayout(self._output_gain_layout)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(915.1e6, 0)
        self.uhd_usrp_source_0.set_gain(20, 0)
        self.uhd_usrp_source_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(915e6-25e3, 0)
        self.uhd_usrp_sink_0.set_gain(output_gain, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.reveng_pattern_dump_0 = reveng.pattern_dump([1,0]*16, 24+8+8+8+8+16, "%Y-%m-%d %H:%M:%S,%[bits]", False, "", True)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=58,
                decimation=1,
                taps=([1]*58),
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=4,
                decimation=58,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 100e3, 50e3, firdes.WIN_HAMMING, 6.76))
        self.lacrosse_TX29U_0 = lacrosse.TX29U()
        self.fosphor_qt_sink_c_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0.set_fft_window(window.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0.set_frequency_range(0, samp_rate)
        self._fosphor_qt_sink_c_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._fosphor_qt_sink_c_0_win)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(4, 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_vco_c_0 = blocks.vco_c(samp_rate, 2*math.pi*120e3, 1)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_SERVER", "", "52001", 10000, False)
        self.blocks_rotator_cc_0 = blocks.rotator_cc(2*3.14*125e3/samp_rate)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, "packet_len")
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-0.5, ))
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0, 'pdus'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))    
        self.msg_connect((self.reveng_pattern_dump_0, 'out'), (self.lacrosse_TX29U_0, 'in'))    
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_vco_c_0, 0))    
        self.connect((self.blocks_char_to_float_0, 0), (self.rational_resampler_xxx_0_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))    
        self.connect((self.blocks_rotator_cc_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_char_to_float_0, 0))    
        self.connect((self.blocks_vco_c_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.reveng_pattern_dump_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.fosphor_qt_sink_c_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.blocks_add_const_vxx_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_rotator_cc_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "usrp_lacrosse_spoof")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 50e3, firdes.WIN_HAMMING, 6.76))
        self.blocks_rotator_cc_0.set_phase_inc(2*3.14*125e3/self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.fosphor_qt_sink_c_0.set_frequency_range(0, self.samp_rate)

    def get_output_gain(self):
        return self.output_gain

    def set_output_gain(self, output_gain):
        self.output_gain = output_gain
        Qt.QMetaObject.invokeMethod(self._output_gain_counter, "setValue", Qt.Q_ARG("double", self.output_gain))
        Qt.QMetaObject.invokeMethod(self._output_gain_slider, "setValue", Qt.Q_ARG("double", self.output_gain))
        self.uhd_usrp_sink_0.set_gain(self.output_gain, 0)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = usrp_lacrosse_spoof()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
