import numpy as np

from jobs.transcoder import Transcoder
from jobs.file_remover import FileRemover
from jobs.suffix_remover import SuffixRemover
from jobs.normalizer import Normalizer
from jobs.splitter import Splitter
from jobs.speed_deformer import SpeedDeformer
from jobs.pitch_deformer import PitchDeformer
from jobs.noise_deformer import NoiseDeformer
from jobs.noise_downloader import NoiseDownloader
from jobs.speech_downloader import SpeechDownloader
from jobs.pipeline import Pipeline


SUFFIXES = [Transcoder.SUFFIX, Normalizer.SUFFIX]

# 8 speeds between (0.8, 1.2); remove the speed with value 1
SPEEDS = np.delete(np.linspace(0.8, 1.2, 9), 4)

# 8 semitones between (-200, 200); remove the semitone with value 0
SEMITONES = np.delete(np.linspace(-200, 200, 9), 4)

OFFSET_IN_SEC = 30
FRAGMENT_DURATION_IN_SEC = 10
NOISE_DURATION_IN_SEC = 30
TRAIN_DURATION_IN_SEC = 5 * 60
TEST_DURATION_IN_SEC = 15 * 60

pipeline = Pipeline(jobs=[

    # prepare noises
    NoiseDownloader(
        output_files_key='noise_downloader_files',
        output_volumes_key='noise_downloader_volumes',
        data='./noise.csv',
        download_directory='./noises'),
    Transcoder(
        input_files_key='noise_downloader_files',
        output_files_key='noise_transcoder_files',
        codec='flac'),
    Normalizer(
        input_files_key='noise_transcoder_files',
        input_volumes_key='noise_downloader_volumes',
        output_files_key='noise_normalizer_files',
        duration_in_sec=NOISE_DURATION_IN_SEC),
    Splitter(
        input_files_key='noise_normalizer_files',
        output_files_key='noise_splitter_files',
        duration_in_sec=NOISE_DURATION_IN_SEC,
        fragment_duration_in_sec=FRAGMENT_DURATION_IN_SEC),
    SuffixRemover(
        input_files_key='noise_splitter_files',
        suffixes=SUFFIXES),
    FileRemover(input_files_key='noise_transcoder_files'),
    FileRemover(input_files_key='noise_normalizer_files'),
    FileRemover(input_files_key='noise_downloader_files'),

    # prepare train
    SpeechDownloader(
        output_files_key='train_speech_downloader_files',
        data='speech.csv',
        group='train',
        download_directory='./train'),
    Transcoder(
        input_files_key='train_speech_downloader_files',
        output_files_key='train_transcoder_files',
        codec='flac'),
    Normalizer(
        input_files_key='train_transcoder_files',
        output_files_key='train_normalizer_files',
        offset_in_sec=OFFSET_IN_SEC,
        duration_in_sec=TRAIN_DURATION_IN_SEC),
    Splitter(
        input_files_key='train_normalizer_files',
        output_files_key='train_splitter_files',
        duration_in_sec=TRAIN_DURATION_IN_SEC,
        fragment_duration_in_sec=FRAGMENT_DURATION_IN_SEC),
    SpeedDeformer(
        input_files_key='train_splitter_files',
        output_files_key='train_speed_deformer_files',
        speeds=SPEEDS,
        fragment_duration_in_sec=FRAGMENT_DURATION_IN_SEC),
    PitchDeformer(
        input_files_key='train_splitter_files',
        output_files_key='train_pitch_deformer_files',
        semitones=SEMITONES),
    NoiseDeformer(
        input_files_key='train_splitter_files',
        output_files_key='train_noise_deformer_files',
        input_noise_files_key='noise_splitter_files'),
    SuffixRemover(input_files_key='train_splitter_files', suffixes=SUFFIXES),
    SuffixRemover(
        input_files_key='train_speed_deformer_files',
        suffixes=SUFFIXES),
    SuffixRemover(
        input_files_key='train_pitch_deformer_files',
        suffixes=SUFFIXES),
    SuffixRemover(
        input_files_key='train_noise_deformer_files',
        suffixes=SUFFIXES),
    FileRemover(input_files_key='train_transcoder_files'),
    FileRemover(input_files_key='train_normalizer_files'),
    FileRemover(input_files_key='train_speech_downloader_files'),

    # prepare test
    SpeechDownloader(
        output_files_key='test_speech_downloader_files',
        data='speech.csv',
        group='test',
        download_directory='./test'),
    Transcoder(
        input_files_key='test_speech_downloader_files',
        output_files_key='test_transcoder_files',
        codec='flac'),
    Normalizer(
        input_files_key='test_transcoder_files',
        output_files_key='test_normalizer_files',
        offset_in_sec=OFFSET_IN_SEC,
        duration_in_sec=TEST_DURATION_IN_SEC),
    Splitter(
        input_files_key='test_normalizer_files',
        output_files_key='test_splitter_files',
        duration_in_sec=TEST_DURATION_IN_SEC,
        fragment_duration_in_sec=FRAGMENT_DURATION_IN_SEC),
    SuffixRemover(input_files_key='test_splitter_files', suffixes=SUFFIXES),
    FileRemover(input_files_key='test_transcoder_files'),
    FileRemover(input_files_key='test_normalizer_files'),
    FileRemover(input_files_key='test_speech_downloader_files')
])

pipeline.execute()
