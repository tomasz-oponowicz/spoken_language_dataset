from . import common
from audio_toolbox import sox


class PitchDeformer:
    SUFFIX = '.pitch@n'

    def __init__(self, input_files_key, output_files_key, semitones):
        self.input_files_key = input_files_key
        self.output_files_key = output_files_key
        self.semitones = semitones

    def execute(self, context):
        input_files = context[self.input_files_key]
        output_files = context[self.output_files_key] = []

        for input_file in input_files:
            output_pattern = common.append_suffix_to_filename(input_file, PitchDeformer.SUFFIX)

            for index, semitone in enumerate(self.semitones):

                # start indexing with 1 to be compatible with sox
                output_file = output_pattern.replace('@n', str(index + 1))
                output_files.append(output_file)

                sox.adjust_pitch(input_file, output_file, semitone=semitone)
