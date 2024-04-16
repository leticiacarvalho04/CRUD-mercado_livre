from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://<user>:<senha>@<nome_colecao>.tooadgk.mongodb.net/?retryWrites=true&w=majority&appName=<nome_colecao>"

client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre

def create_vendedor():
    #Insert
    global db
    mycol = db.vendedor
    mycol_produto = db.produtos

    print("\nInserindo um novo vendedor")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cpf = input("CPF: ")

    opcao = input("Deseja cadastrar um novo produto (N) ou adicionar um produto existente (E)? ")

    if opcao.upper() == 'N':
        nome_produto = input("Digite o nome do novo produto: ")
        preco_produto = input("Digite o preço do novo produto: ")
        produto = {"nome": nome_produto, "preco": preco_produto, "vendedor": {"nome": nome, "cpf": cpf}}
        mycol_produto.insert_one(produto)
    elif opcao.upper() == 'E':
        nome_produto = input("Digite o nome do produto existente: ")
        produto = mycol_produto.find_one({"nome": nome_produto})
        if produto is None:
            print("Produto não encontrado.")
            return
        else:
            mycol_produto.update_one({"nome": nome_produto}, {"$set": {"vendedor": {"nome": nome, "cpf": cpf}}})
    else:
        print("Opção inválida.")
        return

    mydoc = { "nome": nome, "sobrenome": sobrenome, "cpf": cpf, 'produtos': produto }
    x = mycol.insert_one(mydoc)
    print("Documento inserido com ID ",x.inserted_id)

def read_vendedor(nome):
    #Read
    global db
    mycol = db.vendedor
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

def read_all_vendedor():
    #Read
    global db
    mycol = db.vendedor
    mydoc = mycol.find()
    for x in mydoc:
        print(f'Nome vendedor: {x.get("nome")}\nSobrenome vendedor: {x.get("sobrenome")}\nCPF vendedor: {x.get("cpf")}\nProdutos: {x.get("produtos")}\n')

def update_vendedor(cpf):
    # Ler dados do vendedor
    global db
    mycol_vendedor = db.vendedor
    mycol_produto = db.produtos
    myquery = {"cpf": cpf}
    mydoc = mycol_vendedor.find_one(myquery)

    if mydoc is None:
        print("Vendedor não encontrado.")
        return

    print("Dados do usuário: ", mydoc)
    
    nome = input("Mudar nome:")
    if nome:
        mydoc["nome"] = nome

    sobrenome = input("Mudar Sobrenome:")
    if sobrenome:
        mydoc["sobrenome"] = sobrenome

    novo_cpf = input("Mudar CPF:")
    if novo_cpf:
        mydoc["cpf"] = novo_cpf

    # Verifica se o vendedor possui o array de produtos
    if "produtos" in mydoc and mydoc["produtos"]:
        # Pergunta se quer atualizar os produtos vendidos
        atualizar_produtos = input("Deseja atualizar os produtos vendidos? (s/n): ").lower()
        
        if atualizar_produtos == 's':
            produto_antigo_id = input("Digite o id do produto a ser atualizado: ")
            novo_produto_id = input("Digite o id do novo produto: ")

            # Busca o novo produto na coleção de produtos
            novo_produto = mycol_produto.find_one({"_id": ObjectId(novo_produto_id)})
            
            if novo_produto is None:
                print("Produto não encontrado.")
                return

            # Atualiza o produto vendido correspondente na lista de produtos vendidos do vendedor
            for i, produto in enumerate(mydoc["produtos"]):
                if produto["_id"] == ObjectId(produto_antigo_id):
                    mydoc["produtos"][i] = novo_produto
                    break

    newvalues = {"$set": mydoc}
    mycol_vendedor.update_one(myquery, newvalues)
    print("Vendedor atualizado com sucesso.")

def delete_vendedor(cpf):
    #Delete
    global db
    mycol = db.vendedor
    myquery = {"cpf": cpf}

    # Encontra o vendedor antes de deletá-lo
    vendedor = mycol.find_one(myquery)
    if vendedor is None:
        print("Vendedor não encontrado.")
        return

    nome_vendedor = vendedor["nome"]

    # Deleta o vendedor
    mycol.delete_one(myquery)

    print("Deletado o usuário ", nome_vendedor)