# spoken language dataset

[![Build Status](https://travis-ci.org/tomasz-oponowicz/spoken_language_dataset.svg?branch=master)](https://travis-ci.org/tomasz-oponowicz/spoken_language_dataset)

The dataset contains speech samples of English, German and Spanish languages.
Samples are equally balanced between languages, genders and speakers.
The ready to use dataset can be [downloaded from Kaggle][kg].

The repository contains scripts used to generate the final dataset. 
Take a look at the [Build](#build) section if you want to generate the dataset yourself.

## Background

The project was inspired by the TopCoder contest, [Spoken Languages 2][tc].
The given dataset contains 10 second of speech recorded in 1 of 176 languages.
The entire dataset has been based on bible readings. 
Poorly, in many cases there is a single speaker per language (male in most cases).
Even worse the same single speaker exists in the test set.
Of course this can't lead to a good generic solution.

There are two ways we can take:

* First approach is to use a big dataset where all voice or language properties (e.g. gender, age, accent) become equally possible. 
  A good example is [the Common Voice from Mozilla][cv].
  Most likely this leads to the best performance.
  However processing such a huge dataset is expensive and adding new languages is challenging.
* Second approach is to use a small handcrafted dataset and boost it with data augmentation. 
  The advantage is that we can add new languages quickly.
  Last but not least the dataset is small thus it can be processed quickly.

The second approach has been taken.

LibriVox recordings were used to prepare the dataset. 
Samples are equally balanced between languages, genders and speakers. 

The dataset is divided into train and test sets. 
Speakers present in the test set, are not present in the train set. 
This is essential to test a generalization error.

The core of the train set is based on 420 minutes (2520 samples) of original recordings.
After applying several audio transformations (pitch, speed and noise) the train set was extended to 12180 minutes (73080 samples).
The test set contains 90 minutes (540 samples) of original recordings. No data augmentation has been applied.

## Data structure

The dataset is divided into 2 directories:

* *train* (73080 samples)
* *test* (540 samples)

Each sample is an FLAC audio file with:

* sample rate: 22050
* bit depth: 16
* channels: 1
* duration: 10 seconds (sharp)

The original recordings are MP3 files but they are converted into FLAC files quickly 
to avoid re-encoding (and losing quality) during transformations. 

The filename of the sample has following syntax:

    <language>_<gender>_<recording ID>.fragment<index>[.<transformation><index>].flac

...and variables:

* *language*: `en`, `de`, or `es`
* *gender*: `m` or `f`
* *recording ID*: a hash of the URL
* *fragment index*: 1-30
* *transformation*: `speed`, `pitch` or `noise`
* *transformation index*:
  * if `speed`: 1-8
  * if `pitch`: 1-8
  * if `noise`: 1-12

For example:

    es_m_f7d959494477e5e7e33d4666f15311c9.fragment9.speed8.flac

## Sample Model

The dataset was used to train [the spoken language identification model][sli]. 
The trained model has 97% score (i.e. F1 metric) against the test set. 
Additionally it generalizes well which was confirmed against real life content. 
The fact that samples are prefeclty stratified was one of the reasons to achieve such a high performance.

Feel free to create your own model and share results!

## Build

It is possible to add new samples or new languages easily. 
A good start point for changes is [speech.csv](speech.csv).
After adjusting scripts, generate your custom dataset using steps below.

### Prerequisites

* docker is installed (tested with 18.04.0)

### Steps

1. Fetch original recordings and generate samples:

       $ make build
1. Fix samples permissions after copying them from a docker container:

       $ make fix_permissions

## Release History

* 20018-07-06 / v1.0 / Initial version

[tc]: https://community.topcoder.com/longcontest/?module=ViewProblemStatement&rd=16555&pm=13978
[sli]: https://github.com/tomasz-oponowicz/spoken_language_identification
[cv]: https://voice.mozilla.org/en/languages
[kg]: https://www.kaggle.com/toponowicz/spoken-language-identification
