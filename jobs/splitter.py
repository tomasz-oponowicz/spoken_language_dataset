from . import common
from audio_toolbox import sox
import math


class Splitter:
    SUFFIX = '.fragment@n'

    def __init__(self, input_files_key, output_files_key, duration_in_sec, fragment_duration_in_sec):
        self.input_files_key = input_files_key
        self.output_files_key = output_files_key
        self.duration_in_sec = duration_in_sec
        self.fragment_duration_in_sec = fragment_duration_in_sec

    def execute(self, context):
        input_files = context[self.input_files_key]
        output_files = context[self.output_files_key] = []

        for input_file in input_files:
            output_pattern = common.append_suffix_to_filename(input_file, Splitter.SUFFIX)
            sox.split(input_file, output_pattern, fragment_duration_in_sec=self.fragment_duration_in_sec)

            # 1. sox starts indexing with 1.
            # 1. if total duration is 31s and fragment duration is 10s then sox will create 4 fragments.
            fragment_count = int(math.ceil(self.duration_in_sec / self.fragment_duration_in_sec))
            for fragment_index in range(1, fragment_count + 1):
                output_files.append(output_pattern.replace('@n', str(fragment_index)))

