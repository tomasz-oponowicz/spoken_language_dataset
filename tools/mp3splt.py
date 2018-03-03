from tools import common

# TODO remove if not unused


# -n: does not write ID3v1
# -Q: very quiet mode
BIN = '/usr/bin/mp3splt -n -Q'

MINUTE_IN_SECONDS = 60


def build_base_cmd(input, output):
    output_directory = common.get_dirname(output)
    output_filename = common.get_filename(output)

    cmd = "{bin} -o {filename}".format(bin=BIN, filename=output_filename)

    if len(output_directory) > 0:
        cmd = "{cmd} -d {directory}".format(cmd=cmd, directory=output_directory)

    cmd = "{cmd} {input}".format(cmd=cmd, input=input)

    return cmd


def trim(input, output, offset_in_sec, duration_in_sec):
    offset_min_part = offset_in_sec // MINUTE_IN_SECONDS
    offset_sec_part = offset_in_sec % MINUTE_IN_SECONDS

    duration_min_part = duration_in_sec // MINUTE_IN_SECONDS
    duration_sec_part = duration_in_sec % MINUTE_IN_SECONDS

    cmd = "{cmd} {start_min_part}.{start_sec_part}.0 {end_min_part}.{end_sec_part}.0".format(
        cmd=build_base_cmd(input, output),
        start_min_part=offset_min_part,
        start_sec_part=offset_sec_part,
        end_min_part=offset_min_part+duration_min_part,
        end_sec_part=offset_sec_part+duration_sec_part
    )

    common.run_in_foreground(cmd)


def split(input, output, duration_in_sec):

    # Add 1 to the number of digits to output. This will prevent padding.
    output = output.replace('@n', '@n1')

    duration_min_part = duration_in_sec // MINUTE_IN_SECONDS
    duration_sec_part = duration_in_sec % MINUTE_IN_SECONDS

    cmd = "{cmd} -t {duration_min_part}.{duration_sec_part}.0".format(
        cmd=build_base_cmd(input, output),
        duration_min_part=duration_min_part,
        duration_sec_part=duration_sec_part
    )

    common.run_in_foreground(cmd)

