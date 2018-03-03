from tools import common


def transcode(input, output):
    # -loglevel error: show errors only
    # -map_metadata -1: does not write ID3v1
    common.run_in_foreground("/usr/bin/ffmpeg -loglevel error -i {input} -map_metadata -1 {output}".format(
        input=input, output=output))
