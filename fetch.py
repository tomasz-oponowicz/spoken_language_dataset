import pandas as pd
import os
import shutil
import requests
import subprocess
import hashlib
import muda
import jams

GROUP_ATTR = 'Group'
LANGUAGE_ATTR = 'Language'
SEX_ATTR = 'Sex'
URL_ATTR = 'Url'

TEMP_DIR = '.temp'

MP3_INPUT_FILE = 'input.mp3'
FLAC_INPUT_FILE = 'input.flac'

INPUT_OFFSET = 30

TRAIN_INPUT_DURATION = 300
TEST_INPUT_DURATION = TRAIN_INPUT_DURATION * 3

FRAG_DURATION = 10
FRAG_FILE = "{lang}_{sex}_{url_hash}_{index}.flac"

# `-map_metadata -1`: remove metadata
FFMPEG_CONVERT = "ffmpeg -i {0} -ss {2} -t {3} -map_metadata -1 {1}"
FFMPEG_SPLIT = "ffmpeg -i {0} -f segment -segment_time {2} -c copy {1}"

# remove first 30s and limit lenght to 5m
# -n: remove metadata
# mp3splt test.mp3 0.30.0 5.30.0 -n -o out

# frag files into 10s chunks
# mp3splt out.mp3 -t 0.10.0 -o out_@n

JAMS_FILE = "{0}/test.jams".format(TEMP_DIR)
NOISES_DIR = "noises"
NOISE_FILES = [
    "{0}/car.flac".format(NOISES_DIR),
    "{0}/birds.flac".format(NOISES_DIR),
    "{0}/coffee_shop.flac".format(NOISES_DIR),
    "{0}/street_traffic.flac".format(NOISES_DIR)
]


def run_in_foreground(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    process.communicate()

    if process.wait() != 0:
        print("An error occurs whilst executing command:\n{0}".format(cmd))
        raise SystemExit


def fetch_resource(url, path):
    response = requests.get(url, stream=True)
    with open(path, 'wb') as file:
        shutil.copyfileobj(response.raw, file)
    del response


def deform(input):
    jam = jams.JAMS()

    # enable quick loading audio files
    audio = muda.load_jam_audio(jam, input)

    input_without_ext = os.path.splitext(input)[0]

    # negative: deep voice
    print("Creating pitch variations...")
    pitch = muda.deformers.PitchShift(n_semitones=[-2, -1, 1, 2])
    for index, output in enumerate(pitch.transform(audio)):
        muda.save('{0}_pitch_{1}.flac'.format(input_without_ext, index), JAMS_FILE, output)

    # less 1.0: longer
    print("Creating speed variations...")
    stretch = muda.deformers.TimeStretch(rate=[0.81, 0.93, 1.07, 1.23])
    for index, output in enumerate(stretch.transform(audio)):
        muda.save('{0}_speed_{1}.flac'.format(input_without_ext, index), JAMS_FILE, output)

    print("Creating noise variations...")
    # can we speed up loading noises files?
    noise = muda.deformers.BackgroundNoise(n_samples=3, files=NOISE_FILES, weight_min=0.1, weight_max=0.2)
    for index, output in enumerate(noise.transform(audio)):
        muda.save('{0}_noise_{1}.flac'.format(input_without_ext, index), JAMS_FILE, output)


# https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

data = pd.read_csv('data.csv')

groups = data[GROUP_ATTR].unique()
for group in groups:
    if os.path.isdir(group):
        shutil.rmtree(group)
    os.mkdir(group)

for sample_index, row in data.iterrows():
    print("===> Sample #{0}".format(sample_index))

    group = row[GROUP_ATTR]
    language = row[LANGUAGE_ATTR]
    sex = row[SEX_ATTR][0]  # first letter
    url = row[URL_ATTR]

    is_test = group == 'test'
    if is_test:
        input_duration = TEST_INPUT_DURATION
    else:
        input_duration = TRAIN_INPUT_DURATION

    frag_count = input_duration // FRAG_DURATION
    url_hash = hashlib.md5(url.encode()).hexdigest()
    mp3_input_path = os.path.join(TEMP_DIR, MP3_INPUT_FILE)
    flac_input_path = os.path.join(TEMP_DIR, FLAC_INPUT_FILE)
    frag_pattern = os.path.join(TEMP_DIR, FRAG_FILE.format(lang=language, sex=sex, url_hash=url_hash, index='%d'))

    if os.path.isdir(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.mkdir(TEMP_DIR)

    print("Downloading a sample...")
    fetch_resource(url, mp3_input_path)

    # mp3splt test.mp3 0.30.0 5.30.0 -n -o out
    # mp3splt out.mp3 -t 0.10.0 -o out_@n

    print("Converting a sample to FLAC...")
    run_in_foreground(FFMPEG_CONVERT.format(mp3_input_path, flac_input_path, INPUT_OFFSET, input_duration))

    print("Splitting a sample into smaller chunks")
    run_in_foreground(FFMPEG_SPLIT.format(flac_input_path, frag_pattern, FRAG_DURATION))

    for frag_index in range(0, frag_count):
        print('======> Fragment #{0}'.format(frag_index))

        filename = FRAG_FILE.format(lang=language, sex=sex, url_hash=url_hash, index=frag_index)
        source_path = os.path.join(TEMP_DIR, filename)
        target_path = os.path.join(group, filename)

        # copy frag file to test/valid/test dir
        shutil.copy2(source_path, target_path)

        # if not is_test:
        #     deform(target_path)

# remove temporary files
shutil.rmtree(TEMP_DIR)
