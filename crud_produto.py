from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://<user>:<senha>@<nome_colecao>.tooadgk.mongodb.net/?retryWrites=true&w=majority&appName=<nome_colecao>"

client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre

def create_produtos():
    #Insert
    global db
    mycol = db.produtos
    print("\nInserindo um novo produtos")
    nome = input("Nome: ")
    descricao = input("Descricao: ")
    preco = float(input("Preço: "))
    caracteristicas = input("Características: ")
    marca = input("Marca: ")
    tipo_produto = input("Tipo de produto: ")
    mydoc = { "nome": nome, "descricao": descricao, "preco": preco, "caracteristicas": caracteristicas, "marca": marca, "tipo_produto": tipo_produto }
    x = mycol.insert_one(mydoc)
    print("Documento inserido com ID ",x.inserted_id)

def read_produtos(nome):
    #Read
    global db
    mycol = db.produtos
    print("Usuários existentes: ")
    if not len(nome):
        mydoc = mycol.find().sort("nome")
        for x in mydoc:
            print(x["nome"],x["cpf"])
    else:
        myquery = {"nome": nome}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            print(x)

def read_all_produtos():
    #Read
    global db
    mycol = db.produtos
    mydoc = mycol.find()
    for x in mydoc:
        print(x)

def update_produtos(nome):
    #Read
    global db
    mycol = db.produtos
    myquery = {"nome": nome}
    mydoc = mycol.find_one(myquery)
    print("Dados do usuário: ",mydoc)
    nome = input("Mudar Nome:")
    if len(nome):
        mydoc["nome"] = nome

    descricao = input("Mudar Descrição:")
    if len(descricao):
        mydoc["descricao"] = descricao

    preco = float(input("Mudar preço:"))
    if len(preco):
        mydoc["preco"] = preco

    caracteristicas = input("Mudar Características:")
    if len(caracteristicas):
        mydoc["caracteristicas"] = caracteristicas
    
    marca = input("Mudar Marca:")
    if len(marca):
        mydoc["marca"] = marca

    tipo_produto = input("Mudar Tipo de produto:")
    if len(tipo_produto):
        mydoc["tipo_produto"] = tipo_produto

    newvalues = { "$set": mydoc }
    mycol.update_one(myquery, newvalues)

def delete_produtos(nome):
    #Delete
    global db
    mycol = db.produtos
    myquery = {"nome": nome}
    mydoc = mycol.delete_one(myquery)
    print("Deletado o usuário ",mydoc)