#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from config.deepspeech import *

import argparse
import numpy as np
import shlex
import subprocess

import wave
import json

from deepspeech import Model, version
from timeit import default_timer as timer

try:
    from shhlex import quote
except ImportError:
    from pipes import quote


def convert_samplerate(audio_path, desired_sample_rate):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little ' \
              '--compression 0.0 --no-dither - '.format(quote(audio_path), desired_sample_rate)
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno,
                      'SoX not found, use {}hz files or utils it: {}'.format(desired_sample_rate, e.strerror))

    return desired_sample_rate, np.frombuffer(output, np.int16)


def metadata_to_string(metadata):
    return ''.join(token.text for token in metadata.tokens)


def words_from_candidate_transcript(metadata):
    word = ""
    word_list = []
    word_start_time = 0
    # Loop through each character
    for i, token in enumerate(metadata.tokens):
        # Append character to word if it's not a space
        if token.text != " ":
            if len(word) == 0:
                # Log the start time of the new word
                word_start_time = token.start_time

            word = word + token.text
        # Word boundary is either a space or the last character in the array
        if token.text == " " or i == len(metadata.tokens) - 1:
            word_duration = token.start_time - word_start_time

            if word_duration < 0:
                word_duration = 0

            each_word = dict()
            each_word["word"] = word
            each_word["start_time"] = round(word_start_time, 4)
            each_word["duration"] = round(word_duration, 4)

            word_list.append(each_word)
            # Reset
            word = ""
            word_start_time = 0

    return word_list


def metadata_json_output(metadata):
    json_result = dict()
    json_result["transcripts"] = [{
        "confidence": transcript.confidence,
        "words": words_from_candidate_transcript(transcript),
    } for transcript in metadata.transcripts]
    return json.dumps(json_result, indent=2)


class VersionAction(argparse.Action):
    def __init__(self, *args, **kwargs):
        super(VersionAction, self).__init__(nargs=0, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        print('DeepSpeech ', version())
        exit(0)


# works best with 16000hz 16 bit pcm mono - https://www.youtube.com/watch?v=o8dEgTMZ81g for examples
def run_stt():
    parser = argparse.ArgumentParser(description='Running DeepSpeech inference.')

    parser.add_argument('--version', action=VersionAction,
                        help='Print version and exits')

    args = parser.parse_args()

    model_load_start = timer()

    ds = Model(str(model))

    model_load_end = timer() - model_load_start

    if beam_width:
        ds.setBeamWidth(beam_width)

    desired_sample_rate = ds.sampleRate()

    if scorer:
        scorer_load_start = timer()
        ds.enableExternalScorer(str(scorer))
        scorer_load_end = timer() - scorer_load_start

        if lm_alpha and lm_beta:
            ds.setScorerAlphaBeta(lm_alpha, lm_beta)

    if hot_words:
        for word_boost in hot_words.split(','):
            word, boost = word_boost.split(':')
            ds.addHotWord(word, float(boost))

    fin = wave.open(str(file_path), 'rb')
    fs_orig = fin.getframerate()
    if fs_orig != desired_sample_rate:
        fs_new, audio = convert_samplerate(file_path, desired_sample_rate)
    else:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    audio_length = fin.getnframes() * (1 / fs_orig)
    fin.close()

    inference_start = timer()

    if extended_output:
        print("extended")
        stt_out = (metadata_to_string(ds.sttWithMetadata(audio, 1).transcripts[0]))
    elif json_output:
        print("json")
        stt_out = (metadata_json_output(ds.sttWithMetadata(audio, candidate_transcripts)))
    else:
        stt_out = (ds.stt(audio))
    inference_end = timer() - inference_start

    return stt_out
