from tools import common


BIN = '/usr/bin/sox'


def normalize(input, output, sample_rate=22050, bit_depth=16, channels=1, volume=None,
              offset_in_sec=0, duration_in_sec=None):
    cmd = BIN

    if volume:
        cmd = "{cmd} -v {volume}".format(cmd=cmd, volume=volume)

    cmd = "{cmd} {input} -r {sample_rate} -b {bit_depth} -c {channels} {output}".format(
        cmd=cmd,
        input=input,
        sample_rate=sample_rate,
        bit_depth=bit_depth,
        channels=channels,
        output=output
    )

    if duration_in_sec:
        cmd = "{cmd} trim {start} {duration}".format(cmd=cmd, start=offset_in_sec, duration=duration_in_sec)

    common.run_in_foreground(cmd)


def mix(input1, input2, output):
    common.run_in_foreground("{bin} -m {input1} {input2} {output}".format(
        bin=BIN,
        input1=input1,
        input2=input2,
        output=output
    ))


def split(input, output, fragment_duration_in_sec):

    output = output.replace('@n', '%1n')

    common.run_in_foreground("{bin} {input} {output} trim 0 {duration} : newfile : restart".format(
        bin=BIN,
        input=input,
        output=output,
        duration=fragment_duration_in_sec
    ))


def adjust_speed(input, output, speed, expected_duration_in_sec):
    if speed < 1:

        # slow down
        common.run_in_foreground("{bin} {input} {output} speed {speed} trim 0 {duration}".format(
            bin=BIN,
            input=input,
            output=output,
            speed=speed,
            duration=expected_duration_in_sec
        ))
    elif speed > 1:

        # speed up

        # Increase speed (new duration will be shorter) and add padding.
        # Finally trim audio to an expected duration.
        # Padding should be the same as the initial duration.

        temporary_file = common.append_suffix_to_filename(output, '.padded')
        common.run_in_foreground("{bin} {input} {output} speed {speed} pad 0 {duration}".format(
            bin=BIN,
            input=input,
            output=temporary_file,
            speed=speed,
            duration=expected_duration_in_sec
        ))
        common.run_in_foreground("{bin} {input} {output} trim 0 {duration}".format(
            bin=BIN,
            input=temporary_file,
            output=output,
            duration=expected_duration_in_sec
        ))
        common.remove_file(temporary_file)


def adjust_pitch(input, output, semitone):
    # if semitone < 0 then low voice
    # if semitone > 0 then high voice

    common.run_in_foreground("{bin} {input} {output} pitch {semitone}".format(
        bin=BIN,
        input=input,
        output=output,
        semitone=semitone
    ))
