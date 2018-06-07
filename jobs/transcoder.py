from . import common
from audio_toolbox import ffmpeg

class Transcoder:
    SUFFIX = '.transcoder'

    def __init__(self, input_files_key, output_files_key, codec):
        self.input_files_key = input_files_key
        self.output_files_key = output_files_key
        self.codec = codec

    def execute(self, context):
        input_files = context[self.input_files_key]
        output_files = context[self.output_files_key] = []

        for input_file in input_files:
            output_file = common.change_extension(input_file, self.codec)
            output_file = common.append_suffix_to_filename(output_file, Transcoder.SUFFIX)
            output_files.append(output_file)

            ffmpeg.transcode(input_file, output_file)
