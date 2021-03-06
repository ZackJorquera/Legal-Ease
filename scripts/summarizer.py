from sentence import *
from knapsacky import knapsack

import numpy as np
from enum import Enum
import math
#import lexnlp.extract.en.conditions

from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer


specified_stops = text.ENGLISH_STOP_WORDS.union(["english", "law"])
print(list(specified_stops))
stop_words = ["", " ", "\n", "i", "me", "my", "oh", 'mr', 'mrs', 'ms', 'dr', 'said', "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

stop_words = set(stop_words)
new_stop_words = set(specified_stops)
stop_words = list(stop_words|new_stop_words)

class SummarizerSettings(Enum):
    # At the moment this is hardcoded, but in the future it might be cool to include a settings file
    STD_MULT = 1  # How many point a word gets for each standard deviation above occurrences mean it is
    UNDER_MEAN = 1  # For any word with number of occurrences below the mean, this is added
    PER_WORD = 0  # baseline number of points added for every word
    CHAR_MULT = 1 / 3  # For every character in a word above 6 character it will receive this many points.
    WORD_THRES = 15  # Only sentences with this many or more words will be considered
    SW_VAL = 0  # Number of points a sentence gets for each stop word
    SENTENCE_LOC_MULT = 5  # gives sentence at the start and end more value with first and last receiving 5 extra points
    KEY_WORD_VAL = 2


class Summarizer:
    __text = None
    __sentences = None

    _total_words = None
    _words = None
    _word_values = None

    def __init__(self, text=None, sentences=None):
        """
        provide either text or sentences but not both
        :param text: string of text
        :param sentences: list of sentence, where each element is of type Sentence or child class of Sentence
        """
        if text is not None:
            self.__text = text
            self.__sentences = parse_sentences(self.__text, ret_type=Sentence)
        elif sentences is not None:
            self.__sentences = sentences

        self._total_words = 0
        self._words = {}
        self._word_values = {}

        self._calculate_sentence_values(value_q_e=True)

    def _calculate_word_values(self, ignore_stop_words=True):
        """
        Goes through every word and calculates a value
        :param ignore_stop_words:
        :return:
        """
        self._total_words = 0
        for s in self.__sentences:
            for word in parse_words(s.text, to_lower=True):
                self._total_words += 1

                if word not in stop_words or not ignore_stop_words:
                    if word in self._words:
                        self._words[word] += 1
                    else:
                        self._words[word] = 1

        mean = np.array([self._words[k] for k in self._words]).mean()
        mean_squared = np.array([self._words[k] * self._words[k] for k in self._words]).mean()
        std = np.sqrt(mean_squared - mean)

        assert std != 0.0, "Standard deviation was 0, meaning loading sentences failed"

        for word in self._words.keys():
            self._word_values[word] = max(0, int(SummarizerSettings.CHAR_MULT.value * (len(word) - 6)))
            self._word_values[word] += SummarizerSettings.PER_WORD.value

            if self._words[word] < mean + std:
                self._word_values[word] += SummarizerSettings.UNDER_MEAN.value
            else:
                self._word_values[word] = int(SummarizerSettings.STD_MULT.value * ((self._words[word] - mean) / std))

    def _calculate_sentence_values(self, value_q_e=True):
        """
        Goes through every sentence and calculates a value
        :param value_q_e:
        :return:
        """
        for s in self.__sentences:
            if value_q_e:
                if s.text[-1] == '!':
                    s.value = 2
                elif s.text[-1] == '?':
                    s.value = 2
                elif s.text[-1] == '.':
                    s.value = 0

        self._calculate_word_values()

        num_sentences = len(self.__sentences)
        for s in range(len(self.__sentences)):
            if len(self.__sentences[s]) < SummarizerSettings.WORD_THRES.value:
                self.__sentences[s].value = 0
                continue
            #LEXNLP checker
#            if(lexnlp.extract.en.conditions.get_conditions(self.__setences[s].text)):
 #               print(self.__sentences[s].text)
            self.__sentences[s].value += SummarizerSettings.SENTENCE_LOC_MULT.value * 4 * math.pow(
                s - num_sentences / 2, 2) / (math.pow(num_sentences, 2))

            for word in parse_words(self.__sentences[s].text, to_lower=True):
                self.__sentences[s].value += self._word_values.get(word, SummarizerSettings.SW_VAL.value)

            self.__sentences[s].value = int(self.__sentences[s].value)

    def get_optimal_subset(self, max_num_words, ret_as=None):
        """
        :param max_num_words:
        :param ret_as: either None, "str", or "str_list". which will return list of type sentence, single string, or
        list of string respectively.
        :return:
        """
        weights = [s.weight for s in self.__sentences]
        values = [s.value for s in self.__sentences]

        opt_val, opt_subset = knapsack(weights, values, max_num_words)
        if ret_as == "str":
            sentences = "\n".join([self.__sentences[i].text for i in opt_subset])
        elif ret_as == "list_str":
            sentences = [self.__sentences[i].text for i in opt_subset]
        else:
            sentences = [self.__sentences[i] for i in opt_subset]

        return opt_val, sentences

    def get_optimal_subset_by_percent_words(self, percent_of_words, ret_as=None):
        return self.get_optimal_subset(int(percent_of_words * self._total_words), ret_as)
