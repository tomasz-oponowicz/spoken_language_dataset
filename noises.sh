#!/usr/bin/env bash

# fail fast
set -e

# Noise sounds has been download from https://freesound.org .
#
# Coffee shop sample source:
# https://freesound.org/people/ZackCornick/sounds/267273/
#
# Street traffic sample source:
# https://freesound.org/people/saphe/sounds/173955/
#
# Car (closed window) sample source:
# https://freesound.org/people/deleted_user_7146007/sounds/383464/
#
# Wildlife sample source:
# https://freesound.org/people/InspectorJ/sounds/398980/

SAMPLE_RATE=22050
BIT_DEPTH=16
CHANNELS=1
FRAGMENT_DURATION=10
FRAGMENT_COUNT=3

DURATION=$(($FRAGMENT_COUNT*$FRAGMENT_DURATION))

function fetch_and_extract_fragments {
    GDRIVE_FILE_ID=$1
    FILENAME=$2
    EXTENSION=$3
    VOLUME=$4

    # Fetch a background noise from a mirror (i.e. Google Drive)
    wget "https://drive.google.com/uc?id=${GDRIVE_FILE_ID}&export=download" -O $FILENAME.$EXTENSION

    if [[ $EXTENSION == *"wav"* ]]; then

        # Convert wav to flac
        ffmpeg -i $FILENAME{.wav,.compressed.flac}
    fi

    if [[ $EXTENSION == *"flac"* ]]; then

        # It's already a flac, rename
        mv $FILENAME{.flac,.compressed.flac}
    fi

    # Normalize input
    #
    # We need 3 samples (10 seconds each). This a background noise has to be at least 30 seconds.
    sox -v $VOLUME $FILENAME.compressed.flac -r $SAMPLE_RATE -b $BIT_DEPTH -c $CHANNELS $FILENAME.normalized.flac trim 0 $DURATION

    # Split into fragments, 10 seconds each
    sox $FILENAME.normalized.flac $FILENAME.fragment%1n.flac trim 0 $FRAGMENT_DURATION : newfile : restart

    # Remove leftovers
    rm -f $FILENAME{.wav,.compressed.flac,.normalized.flac}
}

TARGET=noises
rm -Rf $TARGET && mkdir $TARGET && cd $TARGET

fetch_and_extract_fragments "1ORFHf1jVDZrxOmuAgzC1ndVslu7TdQR6" "street_traffic" "flac" 0.5
fetch_and_extract_fragments "1Ruloj0mkyDPIbECDKWntoRHQ4PZtHhbr" "car" "wav" 0.5
fetch_and_extract_fragments "1p-jzZrqjsWGBKLZxdUtarX4Ur_QF7BPu" "coffee_shop" "wav" 1
fetch_and_extract_fragments "1a0seW-AaFLqbBI5FBjvbyAM3cUDAPXBC" "wildlife" "wav" 1

