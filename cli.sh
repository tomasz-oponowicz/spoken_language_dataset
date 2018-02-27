#!/usr/bin/env bash

# sox doesn't behave correctly when reading and writing to the same file

# download manually
ffmpeg -i coffee_shop{.wav,.compressed.flac}
# background noise has to be at least 30 seconds. we need 3 samples (10 seconds each).
sox -v 1 coffee_shop.compressed.flac -r 22050 -b 16 -c 1 coffee_shop.normalized.flac trim 0 30
sox coffee_shop.normalized.flac coffee_shop.fragment%1n.flac trim 0 10 : newfile : restart
rm coffee_shop{.wav,.compressed.flac,.normalized.flac}

# decrease volume, the background noise can't be too loud
sox -v 0.5 street_traffic.compressed.flac -r 22050 -b 16 -c 1 street_traffic.normalized.flac trim 0 30
sox street_traffic.normalized.flac street_traffic.fragment%1n.flac trim 0 10 : newfile : restart
rm street_traffic{.compressed.flac,.normalized.flac}

ffmpeg -i car{.wav,.compressed.flac}
sox -v 0.5 car.compressed.flac -r 22050 -b 16 -c 1 car.normalized.flac trim 0 30
sox car.normalized.flac car.fragment%1n.flac trim 0 10 : newfile : restart
rm car{.wav,.compressed.flac,.normalized.flac}

ffmpeg -i wildlife{.wav,.compressed.flac}
sox -v 1 wildlife.compressed.flac -r 22050 -b 16 -c 1 wildlife.normalized.flac trim 0 30
sox wildlife.normalized.flac wildlife.fragment%1n.flac trim 0 10 : newfile : restart
rm wildlife{.wav,.compressed.flac,.normalized.flac}

# TODO prepare noise files:
# change volume
# split

sox car.flac frag_car.flac trim 0 10 : newfile : restart
mp3splt test.mp3 0.30.0 300.30.0 -n -o trim_speech
mp3splt trim_speech.mp3 -t 0.10.0 -o "frag_speech@n"

# convert mp3 to flac
#
# TODO check needed dependencies
ffmpeg -i frag_speech01.mp3 frag_speech01.flac
# normalize samples, 22050 Hz, mono at a bit-depth of 16
sox frag_speech01.flac -r 22050 -b 16 -c 1 output.flac

sox --info frag_car001.flac
sox frag_car001.flac -r 22050 -b 16 -c 1 output.flac

# apply noise
sox -m frag_car001.flac frag_speech01.flac mixed.flac

# time shift
#
# slow down
sox frag_speech22.mp3 slow.flac speed 0.5 trim 0 10
# speed up
#
# add padding at the end which equals the max duration of the sample
sox frag_speech22.mp3 fast.flac speed 1.5 pad 0 10
# trim
sox fast.flac fast2.flac trim 0 10

# pitch
# 
# TODO add x8 variations to simulate different voices
#
# low voice
sox frag_speech01.flac pitch.flac pitch -250
# high voice
sox frag_speech01.flac pitch.flac pitch 250
