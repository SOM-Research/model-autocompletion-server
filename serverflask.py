from flask import Flask,request 
import numpy as np
import recommender
import re

def procesar_conceptos(conceptos):
    conceptos_sin_puntoycoma = re.split(';', conceptos)
    resultado = []
    for concept in conceptos_sin_puntoycoma:
        lista = re.split(',', concept)
        resultado.append(lista)
    return resultado
    
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
        general_embeddings_dict = load_glove("general.txt")
        contextual_embeddings_dict = load_glove("vectors_emasa_en.txt")
    super(MyFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

app = MyFlaskApp(__name__)
prefijo = '/model-autocompletion' # Change to the URL prefix you need
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=prefijo)

@app.route('/')
def index():
    return '<h1>I am the Flask Server, currently running</h1>'

@app.route('/<modelo>/<positiveconcepts>/<negativeconcepts>/<number>')
def nombre(modelo, positiveconcepts, negativeconcepts, number):
    sugerencias = []
    positiveconceptsprocessed = []
    negativeconceptsprocessed = []
    errores = "No hay errores"
    print(positiveconcepts)
    print(negativeconcepts)
    if positiveconcepts: #La lista tiene elementos
        positiveconceptsprocessed = procesar_conceptos(positiveconcepts)
    print(positiveconceptsprocessed)    
    if negativeconcepts: #La lista tiene elementos
        negativeconceptsprocessed = procesar_conceptos(negativeconcepts)
        
    if modelo == "general" and positiveconceptsprocessed and number: #Comprobacion de que number no es nulo
    #Falta por aÃ±adir los conceptos negativos
        for slice in positiveconceptsprocessed:
            sugerencias = recommender.get_suggestions(general_embeddings_dict, slice, [], int(number))
    else:
        errores = "Procesando el modelo general ha habido algun error"
        
    if modelo == "conceptual" and positiveconceptsprocessed and number:
    #Falta por aÃ±adir los conceptos negativos
        for slice in positiveconceptsprocessed:
            sugerencias = recommender.get_suggestions(contextual_embeddings_dict, slice, [], int(number))
    else:
        errores = "Procesando el modelo conceptual ha habido algun error"
        
    return '<h1>Errores: {} <br> Las sugerencias son: {}</h1>'.format(errores, sugerencias)

# allow both GET and POST requests
#@app.route('/form-example', methods=['GET', 'POST'])
#def form_example():
#     if request.method == 'POST':


app.run(host='0.0.0.0', port=int("8080"))
