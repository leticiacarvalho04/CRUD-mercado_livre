from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://<user>:<senha>@<nome_colecao>.tooadgk.mongodb.net/?retryWrites=true&w=majority&appName=<nome_colecao>"

client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre

def create_compras():
    # Insert
    global db
    mycol_compra = db.compras
    mycol_produto = db.produtos
    mycol_usuario = db.usuarios
    mycol_vendedor = db.vendedor

    cpf_cliente = input("Digite o cpf do cliente: ")
    cpf_vendedor = input("Digite o cpf do vendedor: ")

    # Listar todos os produtos com seus preços
    print("\nProdutos disponíveis:")
    for produto in mycol_produto.find():
        print(f"Nome: {produto['nome']}, Preço: {produto['preco']}")
        
    nome_produto = input("Digite o nome do produto: ")

    cliente = mycol_usuario.find_one({"cpf": cpf_cliente})
    if cliente is None:
        print("Cliente não encontrado.")
        return
    
    # Encontrar o vendedor pelo cpf fornecido
    vendedor = mycol_vendedor.find_one({"cpf": cpf_vendedor})
    if vendedor is None:
        print("Vendedor não encontrado.")
        return
        
    produto = mycol_produto.find_one({"nome": nome_produto})
    if produto is None:
        print("Produto não encontrado.")
        return

    print("\nInserindo uma nova compra")
    qnt = int(input("Quantidade: "))  # Convertendo para inteiro
    total = produto["preco"] * qnt  # Calculando o total da compra

    # Dados do cliente
    usuario = {
        "nome": cliente["nome"],
        "sobrenome": cliente["sobrenome"],
        "email": cliente["email"],
    }

    # Dados do produto
    produto_data = {
        "nome": produto["nome"],
        "preco": produto["preco"],
    }

    # Dados do vendedor
    vendedor_data = {
        "nome": vendedor["nome"],
        "sobrenome": vendedor["sobrenome"],
        "cpf": vendedor.get("cpf")  
    }

    mydoc = {
        "produto": produto_data,
        "quantidade": qnt,
        "total": total,
        "usuario": usuario,
        "vendedor": vendedor_data
    }

    x = mycol_compra.insert_one(mydoc)
    print("Documento inserido com ID ", x.inserted_id)

    # Atualizar a coleção de vendedores para incluir a compra
    if "_id" in vendedor:  # Verificando se o campo _id existe
        mycol_vendedor.update_one(
            {"_id": vendedor["_id"]},  # Usando o _id do vendedor para atualização
            {"$push": {"compras": mydoc}}
        )
    else:
        print("ID do vendedor não encontrado. A compra não foi registrada para o vendedor.")

def read_compras(nome):
    # Read
    global db
    mycol_compras = db.compras

    # Busca todas as compras do cliente
    myquery = {"usuario.nome": nome}
    mydoc = mycol_compras.find(myquery)

    # Conta os documentos retornados pelo cursor
    count = mycol_compras.count_documents(myquery)

    # Verifica se o cliente tem compras
    if count == 0:
        print("Nenhuma compra encontrada para este cliente.")
        return

    # Imprime todas as compras do cliente
    print(f"Compras de {nome}:")
    for compra in mydoc:
        print(compra)

def read_all_compras():
    #Read
    global db
    mycol = db.compras
    mydoc = mycol.find()
    for x in mydoc:
        print(x)

def delete_compras(nome_usuario):
    # Delete
    global db
    mycol = db.compras
    
    # Busca todas as compras do usuário pelo nome
    myquery = {"usuario.nome": nome_usuario}
    compras = list(mycol.find(myquery))
    
    if not compras:
        print(f"Nenhuma compra encontrada para o usuário {nome_usuario}.")
        return
    
    print(f"Compras encontradas para o usuário {nome_usuario}:")
    for i, compra in enumerate(compras, 1):
        nome_produto = compra['produto']['nome'] if 'produto' in compra and 'nome' in compra['produto'] else 'Produto Desconhecido'
        total = compra['total'] if 'total' in compra else 'Total Desconhecido'
        print(f"{i}. Nome do Produto: {nome_produto}, Total: {total}")
    
    # Pergunta ao usuário qual compra ele deseja excluir
    indice = int(input(f"Digite o número da compra que deseja excluir (1-{len(compras)}): "))
    
    if indice < 1 or indice > len(compras):
        print("Índice inválido.")
        return
    
    compra_selecionada = compras[indice - 1]
    
    # Deleta a compra selecionada
    mycol.delete_one({"_id": compra_selecionada["_id"]})
    
    print(f"Compra do produto '{compra_selecionada['produto']['nome']}' deletada com sucesso para o usuário {nome_usuario}.")