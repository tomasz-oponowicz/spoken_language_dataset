
# # NOISE
# NoiseDownloader(output_files_key='noise_downloader_files', output_volumes_key='noise_downloader_volumes', data='noise.csv', download_directory='./noises')
# Transcoder(input_files_key='noise_downloader_files', output_files_key='noise_transcoder_files', codec='flac')
# Normalizer(input_files_key='noise_transcoder_files', input_volumes_key='noise_downloader_volumes', output_files_key='noise_normalizer_files', duration_in_sec=30)
# Splitter(input_files_key='noise_normalizer_files', output_files_key='noise_splitter_files', fragment_duration_in_sec=10)
#
# FileRemover(input_files_key='noise_downloader_files')
# FileRemover(input_files_key='noise_transcoder_files')
# FileRemover(input_files_key='noise_normalizer_files')
#
# SuffixRemover(input_files_key='noise_splitter_files', suffixes=SUFFIXES)
#
# # TRAIN
#
# Transcoder(input_files_key='train_speech_downloader_files', output_files_key='train_transcoder_files', codec='flac')
# Normalizer(input_files_key='train_transcoder_files', output_files_key='train_normalizer_files', duration_in_sec=300)
# Splitter(input_files_key='train_normalizer_files', output_files_key='train_splitter_files', fragment_duration_in_sec=10)
#
# FileRemover(input_files_key='train_speech_downloader_files')
# FileRemover(input_files_key='train_transcoder_files')
# FileRemover(input_files_key='train_normalizer_files')
#
# SpeedDeformer(input_files_key='train_splitter_files', output_files_key='train_speed_deformer_files', speeds=[0.75, 1, 1.25], fragment_duration_in_sec=10)
# NoiseDeformer(input_files_key='train_splitter_files', input_noise_files_key='noise_splitter_files', output_files_key='train_noise_deformer_files')
# PitchDeformer(input_files_key='train_splitter_files', output_files_key='train_pitch_deformer_files', semitones=[-100, 100])
#
# SuffixRemover(input_files_key='train_splitter_files', suffixes=SUFFIXES)
# SuffixRemover(input_files_key='train_speed_deformer_files', suffixes=SUFFIXES)
# SuffixRemover(input_files_key='train_noise_deformer_files', suffixes=SUFFIXES)
# SuffixRemover(input_files_key='train_pitch_deformer_files', suffixes=SUFFIXES)

from tools import common
import pandas as pd
import os
import hashlib

GROUP_ATTR = 'Group'
LANGUAGE_ATTR = 'Language'
SEX_ATTR = 'Sex'
EXTENSION_ATTR = 'Extension'
URL_ATTR = 'Url'


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
