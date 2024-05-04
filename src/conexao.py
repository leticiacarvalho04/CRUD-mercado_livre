from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#Troque <email>, <password> e <bd> pelos seus dados
uri = "mongodb+srv://<email>:<password>@<bd>.tooadgk.mongodb.net/?retryWrites=true&w=majority&appName=<bd>"

client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre