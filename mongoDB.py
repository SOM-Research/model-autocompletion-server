import pymongo

URL = "mongodb+srv://model-autocompletion:model-autocompletion@model-autocompletion-cl.wcpdc.mongodb.net/model-autocompletion-db?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
client = pymongo.MongoClient(URL)
db = client.get_default_database()

workspace = db['Workspace']

def create_workspace(workspace_name, model_name, path, model_tag):
    workspace.insert_one({"workspace_name": workspace_name, "model_name": model_name, "path": path, "model_tag": model_tag})

def get_general_models_trained_in_workspace(workspace_name):
    entries = workspace.find({'workspace_name': workspace_name, 'model_tag': "GENERAL"})
    models = []
    for ws in entries:
        models.append(ws.get('model_name'))
    return models 

def get_contextual_models_trained_in_workspace(workspace_name):
    entries = workspace.find({'workspace_name': workspace_name, 'model_tag': "CONTEXTUAL"})
    models = []
    for ws in entries:
        models.append(ws.get('model_name'))
    return models 

def get_workspaces_available():
    workspaces = workspace.distinct( "workspace_name")
    return workspaces 
    
def disconnect_database():
    client.close()