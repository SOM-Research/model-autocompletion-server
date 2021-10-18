from flask import Flask,request, redirect, flash, url_for 
from werkzeug.utils import secure_filename
import os
from os import path
import numpy as np
import recommender as recommendations
import lemmatizer as lemmas
import re
import shutil

'''Given a path to a GloVe embeddings dictionary, we open the file and we put each entry of the file inside an embeddings dictionary. The embeddings dictionary is returned.'''
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

'''Given a the file's name and the path to look for the file, we get the file's location.'''
def find_file_location(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

'''Given a filename, we check if its extension is one of our allowed extensions: e.g. suppose a file called: text.txt it will return True because txt is one of the allowed extensions.'''
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''This method clones the content in glove's github repository and prepares demo.sh file to train our own models.
This method is only called once, when the server is started.'''
def clone_glove_repository():
    if not path.isdir("glove"):
        os.system("git clone https://github.com/stanfordnlp/glove")
        print("Repository cloned")
    else:
        print("It was already cloned")

    if os.path.exists("/glove"):
        # Change the current working Directory and copy our sh file
        shutil.copy2('demo.sh', '/glove/demo.sh')   
        os.chdir("/glove")
    else:
        print("Can't change the Current Working Directory")
    
    if os.path.exists("demo.sh"):
        print("Demo sh exists")
    #prepare_demo_file("demo.sh")
    #os.system("make CC=gcc-10 CPP=g++-10 CXX=g++-10 LD=g++-10")
    os.system("make")

'''Given a list of pre-processed concepts, we store them in a txt file to train them using GloVe's script.'''
def prepare_for_training(list_of_concepts):
    f = open("/glove/training.txt", "w+")
    for concept in list_of_concepts:
        f.write(concept)
        f.write(" ")
    f.close()

'''Given an string cointaining slices (positive concepts) using this format: term1,term2,term3;slice2term1,slice2term2... We split this string and put each word inside a list.'''
def process_concepts(concepts):
    concepts_without_semicolon = re.split(';', concepts)
    result = []
    for concept in concepts_without_semicolon:
        list_without_commas = re.split(',', concept)
        result.append(list_without_commas)
    return result

'''Given an string cointaining negative concepts using this format: term1,term2,term3... We split this string and put each word inside a list.'''
def process_negative_concepts(negative_concepts):
    concepts_without_commas = re.split(',', negative_concepts)  
    return concepts_without_commas

'''Given the positive and negative concepts lists and the number of suggestions the user wants, 
we get suggestions from the general embeddings dictionary loaded when the server started running.'''
def find_general_suggestions(positive_concepts, negative_concepts, number):
    suggestions = []
    for slice in positive_concepts:
        suggestions = recommendations.get_suggestions(general_embeddings_dict, slice, negative_concepts, number)
    return suggestions[:number] 

'''Given the positive and negative concepts lists and the number of suggestions the user wants, 
we get suggestions from the contextual embeddings dictionary loaded when the server started running.'''
def find_contextual_suggestions(positive_concepts, negative_concepts, number):
    suggestions = []
    if 'contextual_embeddings_dict' in globals():
        for slice in positive_concepts:
            suggestions = recommendations.get_suggestions(contextual_embeddings_dict, slice, negative_concepts, number)
        return suggestions[:number]
    else:
        return ["No contextual embeddings loaded."]

'''Class that allows our app to have a custom URL prefix.'''
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

'''Class that allows our app to load general and contextual embeddings when the server starts. 
Both embeddings dictionaries are stored in global variables to be used in the different server queries.''' 
class MyFlaskApp(Flask):
  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
    if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
      with self.app_context():
        global general_embeddings_dict, contextual_embeddings_dict
        general_embeddings_dict = load_glove("glove.6B.300d.txt")
        clone_glove_repository()
    super(MyFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


#UPLOAD_FOLDER = '/opt/model-autocompletion-server/files/' #THIS UPLOAD FOLDER IS FOR REMOTE SERVER, inside it we store the files pre-processed.
UPLOAD_FOLDER = '/files/'
ALLOWED_EXTENSIONS = {'txt'}

app = MyFlaskApp(__name__)
my_prefix = '/model-autocompletion' #This is our custom URL prefix.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=my_prefix)


@app.route('/')
def index():
    return '<h1>I am the Flask Server, currently running</h1>'

'''Using a post request, the user sends a file to our server in order to be pre-processed. Our algorithm checks if the post request has the file. If the user did not select a file,
the browser submits an empty file without a filename. Instead, if the user selected a file, it is stored in the upload folder to make pre-processing easier. As pre-processing also takes
place here, we tokenize the text, remove punctuation and subjects from the list. After pre-processing the text, we store the content in training.txt file
to train it later.'''
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
            path = find_file_location(filename, UPLOAD_FOLDER)

            tokenized = lemmas.tokenize_text(path) #tokenizing text
            tokenized = [lemmas.remove_punctuation(i) for i in tokenized] #removing punctuation symbols from the tokenized text
            filtered_and_tokenized = [elem for elem in tokenized if elem != ''] #removing empty elements from the list
            prepare_for_training(filtered_and_tokenized)

            #filtered_tokenized_no_subjects = lemmas.remove_subjects(filtered_and_tokenized) removing subjects from the list, it may not be necessary to delete them
    return ''' PRE-PROCESSED '''   

'''When the user invokes this URL, we execute demo.sh file to train the text he/she has previously sent.'''
@app.route('/train-corpus')
def training():
    os.system("chmod +x demo.sh")
    os.system("./demo.sh")
    #STORE THE RESULT AS CONTEXTUAL_EMBEDDINGS_DICTIONARY
    contextual_embeddings_dict = load_glove("/glove/training.txt")
    return '''TRAINED'''

@app.route('/testing-lists')
def testing():
    list = ['pineaple', 'banana', 'classical items']
    list2 = ['Antonio', 'Lola', 'Maria']
    return '{}/{}'.format(list, list2) 

@app.route('/testing-lists2')
def testing2():
    list = ['pineaple', 'banana', 'classical items']
    return '{}'.format(list)

'''When the user sends us a get request, he/she specifies the model he/she wants to get suggestions from, 
the positive and negative concepts, the number of suggestions required and if he/she wants suggestions together 
in case he/she wants suggestions from both sources of knowledge.
Given those parameters and once we check if concepts lists are not empty, we find general, contextual or both type of suggestions and show them to the user.'''
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

    print(negative_concepts)    
    if negative_concepts and negative_concepts != "1": #User introduced negative concepts so the list is not empty
        negative_concepts_processed = process_negative_concepts(negative_concepts)
        
    if model == "general" and positive_concepts_processed and number: 
        suggestions = find_general_suggestions(positive_concepts_processed, negative_concepts_processed, int(number))
        if suggestions:
            result = '{}'.format(suggestions)
        else:
            log = 'No suggestions were found in the general model'
    elif model == "contextual" and positive_concepts_processed and number:
        suggestions = find_contextual_suggestions(positive_concepts_processed, negative_concepts_processed, int(number))
        if suggestions:
            result = '{}'.format(suggestions)
        else:
            log = 'No suggestions were found in the contextual model'
    elif model == "general;contextual" and positive_concepts_processed and together and number:
        suggestions = find_general_suggestions(positive_concepts_processed, negative_concepts_processed, int(number))
        suggestions_second_model = find_contextual_suggestions(positive_concepts_processed, negative_concepts_processed, int(number))
        if int(together) == 1:
            result = '{}'.format(suggestions + suggestions_second_model)
        else:
            if suggestions_second_model:
                result = '{}/{}'.format(suggestions, suggestions_second_model)
            else:
                result = '{}'.format(suggestions)
                log = 'No suggestions were found in the contextual model' 
    else:
        log = "No model has been specified"
    end = ""
    if len(log) > 0:
        if len(suggestions) > 0 or len(suggestions_second_model) > 0:
            end =  '/{}'.format(log)
        else:
            end = '{}'.format(log)     
    return result + end 

app.run(host='0.0.0.0', port=8080)
