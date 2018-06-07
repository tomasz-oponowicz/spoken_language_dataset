from . import common
import pandas as pd
import os
import hashlib

GROUP_ATTR = 'Group'
LANGUAGE_ATTR = 'Language'
SEX_ATTR = 'Sex'
EXTENSION_ATTR = 'Extension'
URL_ATTR = 'Mirror'


class SpeechDownloader:
    def __init__(self, output_files_key, data, group, download_directory):
        self.output_files_key = output_files_key
        self.data = data
        self.group = group
        self.download_directory = download_directory

    def execute(self, context):
        output_files = context[self.output_files_key] = []

        common.create_directory(self.download_directory)

        data = pd.read_csv(self.data)
        for index, row in data.iterrows():
            group = row[GROUP_ATTR]
            if group == self.group:
                language = row[LANGUAGE_ATTR]
                sex = row[SEX_ATTR][0]  # first letter, i.e. `f` or `m`
                extension = row[EXTENSION_ATTR]
                url = row[URL_ATTR]
                url_hash = hashlib.md5(url.encode()).hexdigest()

                filename = "{lang}_{sex}_{url_hash}.{extension}".format(
                    lang=language, sex=sex, url_hash=url_hash, extension=extension)
                output_file = os.path.join(self.download_directory, filename)
                output_files.append(output_file)

                common.fetch(url, output_file)
