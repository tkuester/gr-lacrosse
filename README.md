# GR-Lacrosse

A sample GNU Radio based application for listening to a Lacrosse weather
station with an RTL-SDR. The design is more intended to be intuitive to new
users, instead of a tested and proven application.

Example scripts are also provided for transmitting using an Ettus B200.

## Requirements
 - GNU Radio 3.7.2+
 - [gr-osmosdr](http://sdr.osmocom.org/trac/wiki/GrOsmoSDR)
 - [gr-reveng](http://github.com/tkuester/gr-reveng)
 - python-crcmod (now optional for reception)

### For Transmitting
 - [gr-mac](https://github.com/jmalsbury/gr-mac)
 - [libuhd](http://files.ettus.com/manual/page_build_guide.html)

## Packet Structure

Packets contain a 24 bit ID, the temperature, a checksum, and a few unknown
fields. In detail below:

 - Access Code: 0x10 (First 2 MSB don't quite get sent)
 - Preamble: 0xaaaaaaaa
 - ID: 24 bits (Least sig. nibble seems to decrement on subsequent powerups)
 - ???: 4 bits
 - Temp Scale: 4 bits
 - Temp: 8 bits (Approx 0.06 C per bit)
 - ???: 8 bits
 - Checksum: 8 bits
 - Postamble?: 0xaa00

Checksum is [CRC-8-Dallas/Maxim](http://en.wikipedia.org/wiki/Cyclic_redundancy_check#Standards_and_common_use)

## Usage

### Monitoring the temperature sensor with an RTL-SDR:

Not much visual feedback implemented. Haven't done any range testing.
I now have a DC block to help for tuning offsets.

```
cd ./apps
./rtl_lacrosse.py

2015-12-24 11:14:47.410101
Packet:   2dd49466376a95

ID?       2dd494
Cfg?      0x66 (Temp Scale: 6)
Temp:     0x37 ( 55)
Humidity? 0x6a (106)
Checksum: 0x95 (149) [ crcmod not present ]

23.6 C / 74.4 F
...
```

### Monitoring the temperature sensor with a .cfile capture:

If you have a capture you want to analyze, you can use the following program.
The default setup expects the capture file to be tuned to 915 MHz, with a sample
rate of 1 MSPS. These variables can be modified on the command line. Use
`--help` to see more options.

```
cd ./apps
./file_lacrosse.py -f <your_cfile>
```

### Spoofing packets with a USRP B200

This works intermittently. Using the burst tagger from gr-mac has dramatically
improved reliability, although some temperatures don't want to print. The
scale is also off... so 40.0 F shows up as 40.2 F.

The La Crosse WS-9160U-IT looks for sensors the first ~2 minutes after boot.
During this time, bcast.py will sporadically work and set the temperature.
However, after the ~2 minute period, the receiver only listens at ~15 sec
intervals. My guess is if you aren't transmitting exactly when it's
listening, your packet gets dropped.

Perhaps, at 1 minute, the station starts looking at 920 MHz... more later.

```
cd ./apps
# This starts the USRP host, and listens for packets
./usrp_lacrosse_spoof.py &

# This builds and sends a packet to the host, which is then transmitted
# over 915 MHz
./bcast.py 73.2
```

## Getting this to work with other hardware!

It shouldn't be too difficult to make hardware like the HackRF and bladeRF work
with this radio as well. Look at `examples/temp_mon.grc` as a reference
implementation. You may need to add gain control specific to your radio, or add
an offset tune to avoid the DC Spike. Please submit a pull request if you get it
working!
