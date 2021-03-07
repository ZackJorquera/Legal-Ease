import flask
from flask import request, jsonify, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
#from summarizer import Summarizer
from pdf_parser import pdf_parser

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = "uploads/"
@app.route('/', methods=['GET'])
def home():
    return "<h1>Text Summarizer</h1><p>This site is a prototype API</p>"
@app.route('/upload')
def upload():
    data = ""
    return render_template('upload.html')

@app.route('/processpdf', methods=['GET', 'POST'])
def process_pdf():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        number = request.form['id']
        #        sentences = pdf_parser(f.filename)
        # summarizer = Summarizer(sentences=sentences)
        session['data'] = "HELLO"
        return redirect(url_for(".return_data", ids=number))
    else:
        return ""
@app.route('/processpdf/<ids>', methods=['GET', 'POST'])
def return_data(ids):
    return session.pop('data', None)
    
    
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
 #   summarizer = Summarizer(text, headline)
  #  _, summary = summarizer.get_optimal_subset_by_percent_words(.1, ret_as='str')

    return ""


app.run()
