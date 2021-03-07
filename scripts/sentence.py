import re
import string


# Define what the alphabet is and substring that can affect parsing
ALPHABETS = "([A-Za-z])"
PREFIXES = "(Mr|St|Mrs|Ms|Dr|Mgmt)[.]"
SUFFIXES = "(Inc|Ltd|Jr|Sr|Co)"
STARTERS = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
ACRONYMS = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
WEBSITES = "[.](com|net|org|io|gov)"


class Sentence(object):
    __sentence = None

    # These must both be integer values
    _value = None
    _weight = None
    _length = None
    _rnn_val = None

    def __init__(self, sentence, custom_weight=None):
        """
        :param sentence: string for text
        :param custom_weight: if user wants to use a custom weight instead of the length. must be of type int
        """
        self.__sentence = sentence
        if custom_weight is not None:
            if isinstance(custom_weight, int):
                self._weight = custom_weight
            else:
                raise TypeError("Sentence custom_weight must be of type int.")
        self._value = 0
        self._rnn_val = 2

    def __len__(self):
        if self._length is None:
            self._length = len(parse_words(self.text))
        return self._length

    @property
    def text(self):
        return self.__sentence

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def weight(self):
        if self._weight is None:
            return len(self)  # test to see if self.__len__ works
        else:
            return self._weight

    @property
    def rnn_val(self):
        return self._rnn_val

    @rnn_val.setter
    def rnn_val(self, val):
        self._rnn_val = val


def parse_sentences(text, ret_type=str):
    """
    Splits a string into sentences.
    This functions works by replacing '.' that are not instances of text endings with <prd> so it isnt confused.
    This is a modified version of what can be found here:
    https://stackoverflow.com/questions/4576077/how-can-i-split-a-text-into-sentences
    :param text: string of original text
    :param ret_type: will return a list of ret_type. must have ctor that accepts str. example ret_type=Sentence
    :return:
    """
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(PREFIXES, "\\1<prd>", text)
    text = re.sub(WEBSITES, "<prd>\\1", text)
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + ALPHABETS + "[.] ", " \\1<prd> ", text)
    text = re.sub(ACRONYMS + " " + STARTERS, "\\1<stop> \\2", text)
    text = re.sub(ALPHABETS + "[.]" + ALPHABETS + "[.]" + ALPHABETS + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(ALPHABETS + "[.]" + ALPHABETS + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + SUFFIXES + "[.] " + STARTERS, " \\1<stop> \\2", text)
    text = re.sub(" " + SUFFIXES + "[.]", " \\1<prd>", text)
    text = re.sub(" " + ALPHABETS + "[.]", " \\1<prd>", text)
    text = re.sub(r"(\d*)[.](\d+)", "\\1<prd>\\2", text)
    text = re.sub(r"[.]{3}", "<prd><prd><prd>", text)
    if "”" in text:
        text = text.replace(".”", "”.")
    if "\"" in text:
        text = text.replace(".\"", "\".")
    if "!" in text:
        text = text.replace("!\"", "\"!")
    if ")" in text:
        text = text.replace(".)", ").")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [ret_type(s.strip()) for s in sentences]
    return sentences


def parse_words(text, to_lower=False):
    """
    This add both words and numbers. So "Is 1.5 a word?" would have 4 words
    :param text:
    :param to_lower: returns a list of lower case words
    :return:
    """
    if to_lower:
        return [i.lower().strip(string.punctuation) for i in text.split()]
    else:
        return [i.strip(string.punctuation) for i in text.split()]