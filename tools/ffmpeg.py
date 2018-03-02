from tools import common


def transcode(input, output):
    # -loglevel error: show errors only
    common.run_in_foreground("/usr/bin/ffmpeg -loglevel error -i {input} {output}".format(input=input, output=output))
