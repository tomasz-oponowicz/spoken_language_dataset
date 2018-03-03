from tools import common, sox


class SpeedDeformer:
    SUFFIX = '.speed@n'

    def __init__(self, input_files_key, output_files_key, speeds, fragment_duration_in_sec):
        self.input_files_key = input_files_key
        self.output_files_key = output_files_key
        self.speeds = speeds
        self.fragment_duration_in_sec = fragment_duration_in_sec

    def execute(self, context):
        input_files = context[self.input_files_key]
        output_files = context[self.output_files_key] = []

        for input_file in input_files:
            output_pattern = common.append_suffix_to_filename(input_file, SpeedDeformer.SUFFIX)

            for index, speed in enumerate(self.speeds):

                # start indexing with 1 to be compatible with sox
                output_file = output_pattern.replace('@n', str(index + 1))
                output_files.append(output_file)

                sox.adjust_speed(input_file, output_file, speed=speed, expected_duration_in_sec=self.fragment_duration_in_sec)
