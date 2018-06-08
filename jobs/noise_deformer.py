from . import common
from audio_toolbox import sox


class NoiseDeformer:
    SUFFIX = '.noise@n'

    def __init__(
            self,
            input_files_key,
            output_files_key,
            input_noise_files_key):
        self.input_files_key = input_files_key
        self.output_files_key = output_files_key
        self.input_noise_files_key = input_noise_files_key

    def execute(self, context):
        input_files = context[self.input_files_key]
        output_files = context[self.output_files_key] = []
        input_noise_files = context[self.input_noise_files_key]

        for input_file in input_files:
            output_pattern = common.append_suffix_to_filename(
                input_file, NoiseDeformer.SUFFIX)

            for index, input_noise_file in enumerate(input_noise_files):

                # start indexing with 1 to be compatible with sox
                output_file = output_pattern.replace('@n', str(index + 1))
                output_files.append(output_file)

                sox.mix(input_file, input_noise_file, output_file)
