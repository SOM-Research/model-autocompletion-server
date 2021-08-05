from flask import Flask,request, redirect, flash, url_for 
from werkzeug.utils import secure_filename
import os
import numpy as np
import recommender as recommendations
import lemmatizer as lemmas
import re


def process_concepts(concepts):
    concepts_without_semicolon = re.split(';', concepts)
    result = []
    for concept in concepts_without_semicolon:
        list_without_commas = re.split(',', concept)
        result.append(list_without_commas)
    return result

def process_negative_concepts(negative_concepts):
    concepts_without_commas = re.split(',', negative_concepts)  
    return concepts_without_commas

def load_glove(path):
    embeddings_dict = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            token = values[0]
            vector = np.asarray(values[1:], "float32")
            embeddings_dict[token] = vector
    print("GloVe Embeddings loaded")
    return embeddings_dict

class PrefixMiddleware(object):
 
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix
 
    def __call__(self, environ, start_response):
 
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]
 
class MyFlaskApp(Flask):
  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
    if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
      with self.app_context():
        global general_embeddings_dict, contextual_embeddings_dict
        general_embeddings_dict = load_glove("glove.6B.300d.txt")
        contextual_embeddings_dict = load_glove("vectors_emasa_en.txt")
    super(MyFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


UPLOAD_FOLDER = '/opt/model-autocompletion-server/files/'
#UPLOAD_FOLDER = '/files/'
ALLOWED_EXTENSIONS = {'txt'}

app = MyFlaskApp(__name__)
my_prefix = '/model-autocompletion' # Change to the URL prefix you need
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=my_prefix)


@app.route('/')
def index():
    return '<h1>I am the Flask Server, currently running</h1>'

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/pre-process-text', methods=['POST'])
def preprocessing():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            print('Saved')
            path = find(filename, UPLOAD_FOLDER)
            print(path)

            tokenized = lemmas.tokenize_text(path) #tokenizing text
            tokenized = [lemmas.remove_punctuation(i) for i in tokenized] #removing punctuation symbols from the tokenized text
            #tokenized = lemmas.lower(tokenized)
            filtered_and_tokenized = [elem for elem in tokenized if elem != ''] #removing empty elements from the list
            print("After removing punctuation and empty elements")
            print(filtered_and_tokenized)
            #lemmatized_list = lemmas.lemmatize_list(filtered_and_tokenized)
            #print("Now it has been lemmatized")
            #print(lemmatized_list)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
#TO DO: DECIDE WHAT TO DO WITH RETURN    

@app.route('/<model>/<positive_concepts>/<negative_concepts>/<number>/<together>')
def query(model, positive_concepts, negative_concepts, number, together):
    suggestions = []
    suggestions_second_model = []
    positive_concepts_processed = []
    negative_concepts_processed = []
    log = ""
    result = ''
    
    if positive_concepts: #Positive concepts list is not empty
        positive_concepts_processed = process_concepts(positive_concepts)
        
    if negative_concepts: #Negative concepts list is not empty
        negative_concepts_processed = process_negative_concepts(negative_concepts)
        
    if model == "general" and positive_concepts_processed and number: #Checking number is not null
        suggestions = find_general_suggestions(positive_concepts_processed, negative_concepts_processed, int(number))
        if suggestions:
            result = '<h1>Suggestions are: {}</h1>'.format(suggestions)
        else:
            log = 'No suggestions were found in the general model'
    elif model == "contextual" and positive_concepts_processed and number:
        suggestions = find_contextual_suggestions(positive_concepts_processed, negative_concepts_processed, int(number))
        if suggestions:
            result = '<h1>Suggestions are: {}</h1>'.format(suggestions)
        else:
            log = 'No suggestions were found in the contextual model'
    elif model == "general;contextual" and positive_concepts_processed and number and together:
        suggestions = find_general_suggestions(positive_concepts_processed, negative_concepts_processed, int(number))
        suggestions_second_model = find_contextual_suggestions(positive_concepts_processed, negative_concepts_processed, int(number))
        if int(together) == 1:
            result = '<h1>Suggestions are: {}</h1>'.format(suggestions + suggestions_second_model)
        else:
            if suggestions_second_model:
                result = '<h1>Suggestions are: general: {}, contextual: {}</h1>'.format(suggestions, suggestions_second_model)
            else:
                result = '<h1>Suggestions are: general: {}</h1>'.format(suggestions)
                log = 'No suggestions were found in the contextual model' 
    else:
        log = "No model has been specified"
        
    return '<h1>Log: {}</h1>'.format(log) + result

# allow both GET and POST requests
#@app.route('/form-example', methods=['GET', 'POST'])
#def form_example():
#     if request.method == 'POST':
def find_general_suggestions(positive_concepts, negative_concepts, number):
    suggestions = []
    for slice in positive_concepts:
        suggestions = recommendations.get_suggestions(general_embeddings_dict, slice, negative_concepts, number)
    return suggestions 

def find_contextual_suggestions(positive_concepts, negative_concepts, number):
    #Positive concepts come from a partial model
    #Negative concepts are just words
    suggestions = []
    for slice in positive_concepts:
        suggestions = recommendations.get_suggestions(contextual_embeddings_dict, slice, negative_concepts, number)
    return suggestions

app.run(host='0.0.0.0', port=8080)
