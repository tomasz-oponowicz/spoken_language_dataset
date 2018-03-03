from tools import common


class FileRemover:
    def __init__(self, input_files_key):
        self.input_files_key = input_files_key

    def execute(self, context):
        input_files = context[self.input_files_key]

        for input_file in input_files:
            common.remove_file(input_file)

        context[self.input_files_key] = []
