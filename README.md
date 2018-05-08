# spoken language dataset

The dataset contains audio samples of English, German and Spanish speech.
LibriVox recordings were used to prepare the dataset. Samples are equally balanced between languages, genders and speakers.
. The dataset is divided into train and test sets. Speakers in test samples are not present in train samples. This is essential to test a generalization error.

The core of the train set is based on 420 minutes of original recordings. After applying data augmentation (pitch, speed and noise) the train set has been extended to 12180 minutes.

The test set contains 90 minutes of original recordings.

## Build

### Prerequisites

* docker is installed (tested with 18.04.0)

### Steps

1. Fetch original recordings and generate samples:

       $ make build
1. Fix samples permissions after copying them from docker container:

       $ make fix_permissions
