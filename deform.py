import os
import muda
import jams
import glob

TEMP_DIR = '.temp'
JAMS_FILE = "test.jams".format(TEMP_DIR)
NOISES_DIR = "noises"
NOISE_FILES = [
    "{0}/car.flac".format(NOISES_DIR),
    "{0}/birds.flac".format(NOISES_DIR),
    "{0}/coffee_shop.flac".format(NOISES_DIR),
    "{0}/street_traffic.flac".format(NOISES_DIR)
]


def deform(input):
    jam = jams.JAMS()

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
    noise = muda.deformers.BackgroundNoise(n_samples=3, files=NOISE_FILES, weight_min=0.1, weight_max=0.2)
    for index, output in enumerate(noise.transform(audio)):
        muda.save('{0}_noise_{1}.flac'.format(input_without_ext, index), JAMS_FILE, output)


errors = 0
files = glob.glob("train/*.flac")
for file in files:
    print(file)

    try:
        deform(file)
    except Exception as e:
        print("An error occurred", e)
        errors += 1

print("Errors no. ", errors)

# files = glob.glob("valid/*.flac")
# for file in files:
#     deform(file)

os.remove(JAMS_FILE)
