from . import common
from audio_toolbox import sox


class Normalizer:
    SUFFIX = '.normalizer'

    def __init__(
            self,
            input_files_key,
            output_files_key,
            duration_in_sec,
            offset_in_sec=0,
            input_volumes_key=None):
        self.input_files_key = input_files_key
        self.output_files_key = output_files_key
        self.duration_in_sec = duration_in_sec
        self.offset_in_sec = offset_in_sec
        self.input_volumes_key = input_volumes_key

    def execute(self, context):
        input_files = context[self.input_files_key]
        output_files = context[self.output_files_key] = []

        for index, input_file in enumerate(input_files):
            output_file = common.append_suffix_to_filename(
                input_file, Normalizer.SUFFIX)
            output_files.append(output_file)

            volume = None
            if self.input_volumes_key:
                volume = context[self.input_volumes_key][index]

            sox.normalize(
                input_file,
                output_file,
                volume=volume,
                offset_in_sec=self.offset_in_sec,
                duration_in_sec=self.duration_in_sec)
