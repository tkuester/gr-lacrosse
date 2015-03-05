# GR-Lacrosse

## Requirements
 - [gr-reveng](http://github.com/tkuester/gr-reveng)
 - GNU Radio 3.7.2+ (Should work fine... only tested on 3.7.6)
 - python-crcmod

## Packet Structure

Packets are in the form of

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
I don't have a DC block to help for tuning offsets, so use osmocom_fft to
troubleshoot if you're having problems.

```
cd ./apps
./rtl_lacrosse.py

Packet: 2dd49ea6546ad1

ID? 2dd49e
Cfg? 0xa6 (Temp Scale: 6)
Temp: 0x54 (84)
Humidity? 0x6a (106)
Checksum: 0xd1 [ OK ]

25.4 C / 77.8 F
------------------------------
...
```

### Spoofing packets with a USRP B200

This works intermittently. For now, I'm going to blame this on how
GNU Radio's scheduler handles async packets. Definitely a TODO.

The La Crosse WS-9160U-IT looks for sensors the first ~2 minutes after boot.
During this time, bcast.py will sporadically work and set the temperature.
However, after the ~2 minute period, the receiver only listens at ~15 sec
intervals. My guess is if you aren't transmitting exactly when it's
listening, your packet gets dropped.

```
cd ./apps
./usrp_lacrosse_spoof.py &

./bcast.py 73.2
```
