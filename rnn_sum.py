import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.text import one_hot
import os

# TODO: move to `__init__` input
CONFIG_MAX_WORDS = 10000
CONFIG_EMBEDDING_OUTPUT_SIZE = 128
CONFIG_NUM_CLASSES = 10
CONFIG_INTERNAL_UNITS = 128
CONFIG_DECODER_DENSE_OUTPUTS = 10
CONFIG_MAX_INPUT_LEN = 10000


def get_custom_test_comments():
    '''
    Returns a sample test which is easy to manually validates
    '''
    print('\nCreating Manual Test...')

    test_comments = [
        "This is a stupid example.",
        "This is another statement, perhaps this will trick the network",
        "I don't understand",
        "What's up?",
        "open the app",
        "This is another example",
        "Do what I tell you",
        "come over here and listen",
        "how do you know what to look for",
        "Remember how good the concert was?",
        "Who is the greatest basketball player of all time?",
        "Eat your cereal.",
        "Usually the prior sentence is not classified properly.",
        "Don't forget about your homework!",
        "Can the model identify a sentence without a question mark",
        "Everything speculated here is VC money and financial bubble with unrelaible financial values. Zomato, uber, paytm, flipkart throw discounts at the rate of losses. May be few can survive at the end. This hurts a lot for SMB too.",
        "I am trying to keep tabs on electric two-wheeler startup industry in India. Ather energy is emerging as a big name. Anyone knows how they are doing?",
        "generally a pretty intuitive way to accomplish a task. Want to trash an app Drag it to the trash Want to print a PDF",
        "Make sure ownership is clear and minimizing opportunities for such problematic outcomes in the second place",
        "Stop the video and walk away."
    ]

    test_comments_category = [
        "statement",
        "statement",
        "statement",
        "question",
        "command",
        "statement",
        "command",
        "command",
        "question",
        "question",
        "question",
        "command",
        "statement",
        "command",
        "question",
        "statement",
        "question",
        "question",
        "statement",
        "command"
    ]

    return test_comments, test_comments_category


class RnnSummarizer(object):

    def __init__(self):
        self.vocab_size = CONFIG_MAX_WORDS
        encoder_input = layers.Input(shape=(None,), name='encoder_input')
        encoder_embedded = layers.Embedding(input_dim=self.vocab_size, output_dim=CONFIG_EMBEDDING_OUTPUT_SIZE,
                                            input_length=CONFIG_MAX_INPUT_LEN)(encoder_input)
        encoder_lstm = layers.LSTM(CONFIG_INTERNAL_UNITS, return_state=True, name="encoder")
        encoder_output, encoder_state_h, encoder_state_c = encoder_lstm(encoder_embedded)
        encoder_state = [encoder_state_h, encoder_state_c]

        decoder_input = layers.Input(shape=(None,), name='decoder_input')
        decoder_embedded = layers.Embedding(input_dim=self.vocab_size, output_dim=CONFIG_EMBEDDING_OUTPUT_SIZE,
                                            input_length=CONFIG_MAX_INPUT_LEN)(decoder_input)
        decoder_lstm = layers.LSTM(units=CONFIG_INTERNAL_UNITS, return_state=True, return_sequences=True, name='decoder')
        decoder_output, _, _ = decoder_lstm(decoder_embedded, initial_state=encoder_state)

        decoder_dense = layers.Dense(CONFIG_DECODER_DENSE_OUTPUTS)
        dense_output = decoder_dense(decoder_output)

        self.max_input_seq_length = 1

        # this is complicated, i will comment (or ask me, i think it understands)
        model = keras.Model([encoder_input, decoder_input], dense_output)

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        self.model = model

        # we use the encoder_model and decoder_model to interface with the model
        self.encoder_model = keras.Model(encoder_input, encoder_state)

        decoder_state_input = [layers.Input(shape=(CONFIG_INTERNAL_UNITS,)), layers.Input(shape=(CONFIG_INTERNAL_UNITS,))]
        decoder_output, decoder_state_h, decoder_state_c = decoder_lstm(decoder_embedded, initial_state=decoder_state_input)
        decoder_state = [decoder_state_h, decoder_state_c]
        dense_output = decoder_dense(decoder_output)
        self.decoder_model = keras.Model([decoder_input] + decoder_state_input, [dense_output] + decoder_state)

    def summary(self):
        self.model.summary()
        self.encoder_model.summary()
        self.decoder_model.summary()

    def load_weights(self, weight_file_path):
        if os.path.exists(weight_file_path):
            self.model.load_weights(weight_file_path)

    def save_weights(self, weight_file_path):
        self.model.save_weights(weight_file_path)

    def fit(self, x_train, y_train, x_test, y_test):
        self.model.fit(x_train, y_train, batch_size=128, epochs=5, validation_data=(x_test, y_test))

    def classify(self, input_text):
        # TODO: allow for all uppercase to be different work
        # TODO: split bu sentence not line
        encoded_lines = np.array([one_hot(input_text_line, self.vocab_size) for input_text_line in input_text.splitlines()])
        encoded_full_doc = [item for sublist in encoded_lines for item in sublist]
        input_seq = np.array(encoded_full_doc).reshape((1,-1,1))
        input_seq_lines = [np.array(encoded_line).reshape((1,-1,1)) for encoded_line in encoded_lines]
        print(input_seq, input_seq_lines)

        states_value = self.encoder_model.predict(input_seq)
        output_data = []
        for input_line_seq in input_seq_lines:
            output_tokens, h, c = self.decoder_model.predict([np.asarray(input_line_seq)] + states_value)

            sample_token_idx = np.argmax(output_tokens[0, -1, :])
            output_data.append(sample_token_idx)

            states_value = [h, c]

        return output_data


if __name__ == '__main__':
    summer = RnnSummarizer()
    summer.save_weights("model/init.ckpt")
    print(summer.classify("tes test hello what party.\n hello."))
