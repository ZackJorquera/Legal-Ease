import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import backend
import os
from datetime import datetime
from sentence import *
import time
from collections import Counter


# TODO: move to `__init__` input
CONFIG_MAX_WORDS = 1000  # 10000
CONFIG_EMBEDDING_OUTPUT_SIZE = 20  # 128
CONFIG_INTERNAL_UNITS = 128
CONFIG_DECODER_DENSE_OUTPUTS = 4
CONFIG_MAX_INPUT_LEN = 10000

strategy = tf.distribute.MirroredStrategy()


def timeme(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))

        print(f"{str(method)} took {endTime - startTime}ms")
        return result

    return wrapper


#  help from: https://github.com/chen0040/keras-text-summarization/blob/11df7c7bf30de8ccd8aecef5a551c136c85f0092/keras_text_summarization/library/seq2seq.py#L396
# https://www.tensorflow.org/tutorials/text/text_classification_rnn#create_the_model
class RnnSummarizer(object):
    # def __init__(self):
    #     self.vocab_size = CONFIG_MAX_WORDS
    #     encoder_input = layers.Input(shape=(None,), name='encoder_input')
    #     encoder_embedded = layers.Embedding(input_dim=self.vocab_size, output_dim=CONFIG_EMBEDDING_OUTPUT_SIZE,
    #                                         input_length=CONFIG_MAX_INPUT_LEN)(encoder_input)
    #     encoder_lstm = layers.LSTM(CONFIG_INTERNAL_UNITS, return_state=True, name="encoder")
    #     encoder_output, encoder_state_h, encoder_state_c = encoder_lstm(encoder_embedded)
    #     encoder_state = [encoder_state_h, encoder_state_c]
    #
    #     decoder_input = layers.Input(shape=(None,), name='decoder_input')
    #     decoder_embedded = layers.Embedding(input_dim=self.vocab_size, output_dim=CONFIG_EMBEDDING_OUTPUT_SIZE,
    #                                         input_length=CONFIG_MAX_INPUT_LEN)(decoder_input)
    #     decoder_lstm = layers.LSTM(units=CONFIG_INTERNAL_UNITS, return_state=True, return_sequences=True,
    #                                name='decoder')
    #     decoder_output, _, _ = decoder_lstm(decoder_embedded, initial_state=encoder_state)
    #
    #     decoder_dense = layers.Dense(CONFIG_DECODER_DENSE_OUTPUTS)
    #     dense_output = decoder_dense(decoder_output)
    #
    #     self.max_input_seq_length = 1
    #
    #     # this is complicated, i will comment (or ask me, i think it understands)
    #     model = keras.Model([encoder_input, decoder_input], dense_output)
    #
    #     model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    #
    #     self.model = model
    #
    #     # we use the encoder_model and decoder_model to interface with the model
    #     self.encoder_model = keras.Model(encoder_input, encoder_state)
    #
    #     decoder_state_input = [layers.Input(shape=(CONFIG_INTERNAL_UNITS,)),
    #                            layers.Input(shape=(CONFIG_INTERNAL_UNITS,))]
    #     decoder_output, decoder_state_h, decoder_state_c = decoder_lstm(decoder_embedded,
    #                                                                     initial_state=decoder_state_input)
    #     decoder_state = [decoder_state_h, decoder_state_c]
    #     dense_output = decoder_dense(decoder_output)
    #     self.decoder_model = keras.Model([decoder_input] + decoder_state_input, [dense_output] + decoder_state)

    def __init__(self):
        self.vocab_size = CONFIG_MAX_WORDS
        # TODO: make Bidirectional: https://www.tensorflow.org/tutorials/text/text_classification_rnn
        # encoder_input = layers.Input(shape=(None,), name='encoder_input')
        # encoder_embedded = layers.Embedding(input_dim=self.vocab_size, output_dim=CONFIG_EMBEDDING_OUTPUT_SIZE,
        #                                     input_length=CONFIG_MAX_INPUT_LEN)(encoder_input)
        # encoder_lstm = layers.LSTM(CONFIG_INTERNAL_UNITS, return_state=True, name="encoder")
        # encoder_output, encoder_state_h, encoder_state_c = encoder_lstm(encoder_embedded)
        # encoder_state = [encoder_state_h, encoder_state_c]
        #
        # decoder_dense = layers.Dense(CONFIG_DECODER_DENSE_OUTPUTS)
        # dense_output = decoder_dense(encoder_output)

        # this is complicated, i will comment (or ask me, i think it understands)
        #model = keras.Model(encoder_input, dense_output)

        with strategy.scope():
            model = keras.Sequential([
                layers.Input(shape=(None,), name='encoder_input'),
                layers.Embedding(input_dim=self.vocab_size, output_dim=CONFIG_EMBEDDING_OUTPUT_SIZE,
                                 input_length=CONFIG_MAX_INPUT_LEN),
                layers.Bidirectional(layers.LSTM(CONFIG_INTERNAL_UNITS, return_state=False, name="encoder")),
                layers.Dense(CONFIG_DECODER_DENSE_OUTPUTS, activation='softmax')
            ])

            self.max_input_seq_length = CONFIG_MAX_INPUT_LEN

            model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

            backend.set_value(model.optimizer.learning_rate, 0.01)
        self.model = model

        # # we use the encoder_model_get_state and encoder_model_with_state to interface with the model
        # self.encoder_model_get_state = keras.Model(encoder_input, encoder_state)
        #
        # encoder_state_input = [layers.Input(shape=(CONFIG_INTERNAL_UNITS,)), layers.Input(shape=(CONFIG_INTERNAL_UNITS,))]
        # encoder_output, encoder_state_h, encoder_state_c = encoder_lstm(encoder_embedded, initial_state=encoder_state_input)
        # encoder_state = [encoder_state_h, encoder_state_c]
        # dense_output = decoder_dense(encoder_output)
        # self.encoder_model_with_state = keras.Model([encoder_input] + encoder_state_input, [dense_output] + encoder_state)


    # def summary(self):
    #     self.model.summary()
    #     self.encoder_model.summary()
    #     self.decoder_model.summary()

    def summary(self):
        self.model.summary()
        #self.encoder_model_get_state.summary()
        #self.encoder_model_with_state.summary()

    def load_weights_unchecked(self, weight_file_path):
        with strategy.scope():
            self.model.load_weights(weight_file_path)

    def load_weights_from_dir(self, weight_dir):
        latest_ckpt = tf.train.latest_checkpoint(weight_dir)
        if latest_ckpt is not None:
            with strategy.scope():
                self.model.load_weights(latest_ckpt)

    def save_weights(self, weight_file_path):
        self.model.save_weights(weight_file_path)

    def fit(self, x_train, y_train, x_test, y_test, epochs=None, batch_size=None, model_dir_path=None):
        now = datetime.now()
        if epochs is None:
            epochs = 10
        if model_dir_path is None:
            model_dir_path = f'./model/checkpoints/{now.strftime("%Y%m%d-%H%M%S")}'
        if batch_size is None:
            batch_size = 10

        checkpoint = keras.callbacks.ModelCheckpoint(model_dir_path + '/cp-{epoch}.ckpt', save_weights_only=True)
        tb_cb = tf.keras.callbacks.TensorBoard(log_dir=f'./logs/{now.strftime("%Y%m%d-%H%M%S")}', update_freq='epoch', profile_batch=2,)

        with strategy.scope():
            x_train = [one_hot(x_elem, self.vocab_size) for x_elem in x_train]
            x_train = pad_sequences(x_train, maxlen=self.max_input_seq_length, padding='post')
            x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], 1))

            if isinstance(y_train[0], list):
                y_train_tmp = np.zeros((len(y_train), CONFIG_DECODER_DENSE_OUTPUTS))
                for i, el in enumerate(y_train):
                    y_train_tmp[i] += np.sum(keras.utils.to_categorical(el, num_classes=CONFIG_DECODER_DENSE_OUTPUTS), axis=0)
                y_train = y_train_tmp
            elif isinstance(y_train, np.ndarray):
                pass
            else:
                y_train = np.array(y_train)
                y_train = keras.utils.to_categorical(y_train, num_classes=CONFIG_DECODER_DENSE_OUTPUTS)

            if x_test is not None and y_test is not None:
                x_test = [one_hot(x_elem, self.vocab_size) for x_elem in x_test]
                x_test = pad_sequences(x_test, maxlen=self.max_input_seq_length, padding='post')
                x_test = x_test.reshape((x_test.shape[0], x_test.shape[0], 1))

                y_test = keras.utils.to_categorical(y_test, num_classes=CONFIG_DECODER_DENSE_OUTPUTS)
            else:
                x_test, y_test = None, None

            history = self.model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, callbacks=[checkpoint, tb_cb])

        return history

    # def classify(self, sentence_list):
    #     # TODO: allow for all uppercase to be different work
    #     encoded_lines = [one_hot(input_text_line, self.vocab_size) for input_text_line in sentence_list]
    #     encoded_full_doc = [item for sublist in encoded_lines for item in sublist]
    #     input_seq = np.array(encoded_full_doc).reshape((1,-1,1))
    #     input_seq_lines = [np.array(encoded_line).reshape((1,-1,1)) for encoded_line in encoded_lines]
    #     #print(input_seq, input_seq_lines)
    #
    #     states_value = self.encoder_model.predict(input_seq)
    #     output_data = []
    #     for input_line_seq in input_seq_lines:
    #         output_tokens, h, c = self.decoder_model.predict([np.asarray(input_line_seq)] + states_value)
    #
    #         sample_token_idx = np.argmax(output_tokens[0, -1, :])
    #         output_data.append(sample_token_idx)
    #
    #         states_value = [h, c]
    #
    #     return output_data

    @timeme
    def classify(self, sentence_list, batch_all=False):
        # TODO: allow for all uppercase to be different work
        encoded_lines = [one_hot(input_text_line, self.vocab_size) for input_text_line in sentence_list]
        #encoded_full_doc = [item for sublist in encoded_lines for item in sublist]
        #input_seq = np.array(encoded_full_doc).reshape((1,-1,1))
        if batch_all:
            input_seq_lines = pad_sequences(encoded_lines, maxlen=self.max_input_seq_length, )
            input_seq_lines = input_seq_lines.reshape((input_seq_lines.shape[0], input_seq_lines.shape[1], 1))

            with strategy.scope():
                output_tokens = self.model.predict(input_seq_lines)

            sample_token_idx = np.argmax(output_tokens, axis=1)

            print(sample_token_idx)
            return sample_token_idx

        else:
            input_seq_lines = [np.array(encoded_line).reshape((1,-1,1)) for encoded_line in encoded_lines]
            #print(input_seq, input_seq_lines)

            output_data = []

            for input_line_seq in input_seq_lines:
                output_tokens = self.model.predict(input_line_seq)

                sample_token_idx = np.argmax(output_tokens[-1, :])
                output_data.append(sample_token_idx)
                #print(output_tokens)

            print(output_data)
            return output_data


def load_data(sent_file, class_file):
    with open(sent_file, 'r', encoding='utf-8') as sfr:
        sents = [sent for sent in sfr.readlines()]
    with open(class_file, 'r', encoding='utf-8') as cfr:
        classes = [[int(e) - 1 for e in classif.split(",")] for classif in cfr.readlines()]

    x_train = np.array(sents)
    y_train = np.zeros((len(classes), CONFIG_DECODER_DENSE_OUTPUTS))
    for i, el in enumerate(classes):
        y_train[i] += np.sum(keras.utils.to_categorical(el, num_classes=CONFIG_DECODER_DENSE_OUTPUTS), axis=0)

    # TODO: make better code, like why
    sents = []
    classes = []

    sents = sents + list(x_train[np.where(y_train[:,0])]) + list(x_train[np.where(y_train[:,0])]) + list(x_train[np.where(y_train[:,0])]) + list(x_train[np.where(y_train[:,0])])
    classes = classes + list(y_train[np.where(y_train[:,0])]) + list(y_train[np.where(y_train[:,0])]) + list(y_train[np.where(y_train[:,0])]) + list(y_train[np.where(y_train[:,0])])

    sents = sents + list(x_train[np.where(y_train[:, 1])]) + list(x_train[np.where(y_train[:, 1])]) + list(x_train[np.where(y_train[:, 1])]) + list(x_train[np.where(y_train[:, 1])])
    classes = classes + list(y_train[np.where(y_train[:, 1])]) + list(y_train[np.where(y_train[:, 1])]) + list(y_train[np.where(y_train[:, 1])]) + list(y_train[np.where(y_train[:, 1])])

    sents = sents + list(x_train[np.where(y_train[:, 2])[0][:25]])
    classes = classes + list(y_train[np.where(y_train[:, 2])[0][:25]])

    sents = sents + list(x_train[np.where(y_train[:, 3])[0][:25]])
    classes = classes + list(y_train[np.where(y_train[:, 3])[0][:25]])

    x_train = np.array(sents)
    y_train = np.array(classes)

    p = np.random.permutation(len(sents))

    distrib = np.min(np.sum(y_train, axis=0))

    return x_train[p], y_train[p]


def sentence_to_rnn_vals(sentences, rnn_weights_dir='model'):
    summer = RnnSummarizer()
    if rnn_weights_dir is not None:
        summer.load_weights_from_dir(rnn_weights_dir)

    sent_array_str = [sentence.text for sentence in sentences]
    vals = summer.classify(sent_array_str)
    for i in range(len(sentences)):
        sentences[i].rnn_val = vals[i]


if __name__ == '__main__':
    sents, classifs = load_data('data/sentences.txt', 'data/classifications.txt')

    summer = RnnSummarizer()
    #summer.summary()
    #summer.load_weights_unchecked("model/checkpoints/20210307-010803/cp-18.ckpt")
    # summer.load_weights_from_dir('model')
    summer.fit(sents, classifs, None, None, epochs=100)
    summer.save_weights("model/final.ckpt")
    print(summer.classify(["This is a stupid example.", "Clean the desk.", "What is for lunch"]))
    print(summer.classify(["This is a stupid example.", "Clean the desk.", "What is for lunch"]))
    print(summer.classify(["This is a stupid example.", "Clean the desk.", "What is for lunch"]))
    # 0, 2, 1
