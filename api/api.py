import flask
from flask import request, jsonify

from summarizer import Summarizer
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Text Summarizer</h1><p>This site is a prototype API</p>"


@app.route('/api/summarizetext', methods=['GET'])
def api_summarize_text():
    headline = ""
    if 'text' in request.args:
        text = str(request.args['text'])
    else:
        return "Error: No text field provided. Please specify text."

    if 'headline' in request.args:
        headline = str(request.args['headline'])

    # Create an empty list for our results
    summarizer = Summarizer(text, headline)
    _, summary = summarizer.get_optimal_subset_by_percent_words(.1, ret_as='str')

    return summary


app.run()
