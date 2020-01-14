'''
Here we try to estimate the average of syllables per word, to optimize time in verse generating
'''
import pickle
from math import sqrt

from utils.spanish_syllables import *


def get_mean_syllable(model):
    syllable_count = 0
    for word in model.vocabulary():
        syllable_count += how_many_syllables_word(word)
    return syllable_count / model.V()


def get_standard_deviation_syllable(model):
    syllable_count = 0
    media = get_mean_syllable(model)
    for word in model.vocabulary():
        syllable_count += how_many_syllables_word(word) - media
    s = syllable_count/(model.V()-1)
    return sqrt(s)
