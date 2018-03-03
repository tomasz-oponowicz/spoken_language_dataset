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
FRAGMENT_DURATION_IN_SEC = 10
NOISE_DURATION_IN_SEC = 30
VALID_DURATION_IN_SEC = 5 * 60
TRAIN_DURATION_IN_SEC = 5 * 60
TEST_DURATION_IN_SEC = 15 * 60

pipeline = Pipeline(jobs=[

    # prepare noises
    NoiseDownloader(output_files_key='noise_downloader_files', output_volumes_key='noise_downloader_volumes',
                    data='./noise.csv', download_directory='./noises'),
    Transcoder(input_files_key='noise_downloader_files', output_files_key='train_transcoder_files', codec='flac'),
    Normalizer(input_files_key='train_transcoder_files', output_files_key='train_normalizer_files',
               duration_in_sec=NOISE_DURATION_IN_SEC),
    Splitter(input_files_key='train_normalizer_files', output_files_key='train_splitter_files',
             duration_in_sec=NOISE_DURATION_IN_SEC, fragment_duration_in_sec=FRAGMENT_DURATION_IN_SEC),
    SuffixRemover(input_files_key='train_splitter_files', suffixes=SUFFIXES),
    FileRemover(input_files_key='train_transcoder_files'),
    FileRemover(input_files_key='train_normalizer_files'),
    FileRemover(input_files_key='noise_downloader_files'),


    # prepare valid
    SpeechDownloader(output_files_key='valid_speech_downloader_files', data='speech.csv',
                     group='valid', download_directory='./valid'),
    Transcoder(input_files_key='valid_speech_downloader_files',
               output_files_key='valid_transcoder_files', codec='flac'),
    Normalizer(input_files_key='valid_transcoder_files', output_files_key='valid_normalizer_files',
               duration_in_sec=VALID_DURATION_IN_SEC),
    Splitter(input_files_key='valid_normalizer_files', output_files_key='valid_splitter_files',
             duration_in_sec=VALID_DURATION_IN_SEC, fragment_duration_in_sec=FRAGMENT_DURATION_IN_SEC),
    SuffixRemover(input_files_key='valid_splitter_files', suffixes=SUFFIXES),
    FileRemover(input_files_key='valid_transcoder_files'),
    FileRemover(input_files_key='valid_normalizer_files'),
    FileRemover(input_files_key='valid_speech_downloader_files')
])

pipeline.execute()
