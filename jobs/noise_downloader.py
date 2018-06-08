from . import common
import pandas as pd
import os

FILENAME_ATTR = 'Filename'
VOLUME_ATTR = 'Volume'
URL_ATTR = 'Mirror'


class NoiseDownloader:
    def __init__(
            self,
            output_files_key,
            output_volumes_key,
            data,
            download_directory):
        self.output_files_key = output_files_key
        self.output_volumes_key = output_volumes_key
        self.data = data
        self.download_directory = download_directory

    def execute(self, context):
        output_files = context[self.output_files_key] = []
        output_volumes = context[self.output_volumes_key] = []

        common.create_directory(self.download_directory)

        data = pd.read_csv(self.data)
        for index, row in data.iterrows():
            output_volumes.append(float(row[VOLUME_ATTR]))

            output_file = os.path.join(
                self.download_directory, row[FILENAME_ATTR])
            output_files.append(output_file)

            common.fetch(row[URL_ATTR], output_file)
