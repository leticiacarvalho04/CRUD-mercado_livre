from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://<user>:<senha>@<nome_colecao>.tooadgk.mongodb.net/?retryWrites=true&w=majority&appName=<nome_colecao>"

client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre

def create_favoritos():
    # Insert
    global db
    mycol_produto = db.produtos
    mycol_usuario = db.usuarios  

    cpf_cliente = input("Digite o CPF do cliente: ")
    nome_produto = input("Digite o nome do produto: ")
    parcelas = int(input("Digite o número de parcelas: ")) 

    cliente = mycol_usuario.find_one({"cpf": cpf_cliente})
    if cliente is None:
        print("Cliente não encontrado.")
        return
        
    produto = mycol_produto.find_one({"nome": nome_produto})
    if produto is None:
        print("Produto não encontrado.")
        return

    # Transforma 'favoritos' em um array se for um objeto
    if not isinstance(cliente.get('favoritos'), list):
        mycol_usuario.update_one(
            {"_id": cliente["_id"]},
            {"$set": {"favoritos": []}}
        )

    # Adiciona o novo produto aos 'favoritos'
    result = mycol_usuario.update_one(
        {"_id": cliente["_id"]},
        {"$addToSet": {"favoritos": {
            "produto_id": produto["_id"],
            "nome": produto["nome"],
            "preco": produto["preco"],
            "parcelas": parcelas
        }}}
    )

    if result.modified_count > 0:
        print("Produto adicionado aos favoritos do cliente!")
    else:
        print("Erro ao adicionar o produto aos favoritos.")

def read_all_favoritos():
    global db
    clientes_col = db.usuarios
    
    print("Clientes e seus favoritos: ")
    
    # Encontra todos os clientes
    clientes = clientes_col.find()
    
    for cliente in clientes:
        cliente_nome = cliente["nome"]  # Supondo que o campo do nome do cliente é "nome"
        
        print(f"Cliente: {cliente_nome}")
        
        # Verifica se o campo "favoritos" existe no cliente
        if "favoritos" in cliente:
            favoritos = cliente.get("favoritos", [])  # Obtém o array "favoritos" ou uma lista vazia se não existir
            
            print("Favoritos:")
            for favorito in favoritos:
                print(f"- {favorito}")  # Imprime cada favorito do array "favoritos"
        else:
            print("Sem favoritos.")
        
        print("----------------------")

def read_favoritos(cpf):
    global db
    clientes_col = db.usuarios
    
    # Busca o cliente pelo CPF
    cliente = clientes_col.find_one({"cpf": cpf})  # Supondo que o campo do CPF é "cpf"
    
    if cliente:
        cliente_nome = cliente["nome"]  # Supondo que o campo do nome do cliente é "nome"
        
        print(f"Favoritos do cliente {cliente_nome} (CPF: {cpf}):")
        
        # Verifica se o campo "favoritos" existe no cliente
        if "favoritos" in cliente:
            favoritos = cliente["favoritos"]
            
            for favorito in favoritos:
                print(f"- {favorito}")  
        else:
            print("Sem favoritos.")

        if not favoritos:
            print("O cliente não possui favoritos.")
    else:
        print(f"Cliente com CPF {cpf} não encontrado.")

def update_favoritos():
    # Update
    global db
    mycol_usuario = db.usuarios
    mycol_produto = db.produtos

    # Buscar clientes que possuem favoritos
    clientes_com_favoritos = mycol_usuario.find({"favoritos": {"$exists": True, "$ne": []}})
    
    # Listar clientes que possuem favoritos
    for cliente in clientes_com_favoritos:
        print(f'Nome do cliente: {cliente.get("nome")}')
        print(f'CPF do cliente: {cliente.get("cpf")}')
        print(f'Favoritos do cliente: {cliente.get("favoritos")}')
        print("---------------------------------------\n")

    cpf_cliente = input("Digite o CPF do cliente: ")
    favorito_antigo = ObjectId(input("Digite o id do favorito antigo: "))
    novo_produto_id = ObjectId(input("Digite o id do novo produto favorito: "))

    cliente = mycol_usuario.find_one({"cpf": cpf_cliente})
    if cliente is None:
        print("Cliente não encontrado.")
        return

    # Buscar o objeto de favorito pelo ID antigo
    favorito_antigo_obj = [fav for fav in cliente['favoritos'] if fav['produto_id'] == favorito_antigo]
    
    if not favorito_antigo_obj:
        print("Favorito antigo não encontrado.")
        return

    novo_produto_obj = mycol_produto.find_one({"_id": novo_produto_id})
    if novo_produto_obj is None:
        print("Novo produto não encontrado.")
        return

    # Solicitar quantidade de parcelas
    quantidade_parcelas = int(input("Digite a quantidade de parcelas desejadas: "))

    try:
        # Atualiza o favorito
        result = mycol_usuario.update_one(
            {"cpf": cpf_cliente, "favoritos.produto_id": favorito_antigo},
            {"$set": {"favoritos.$": {
                "produto_id": novo_produto_id,
                "nome": novo_produto_obj["nome"],
                "preco": novo_produto_obj["preco"],
                "parcelas": quantidade_parcelas  # Adiciona o campo 'parcelas'
            }}}
        )

        if result.modified_count > 0:
            print("Favorito atualizado com sucesso")
        else:
            print("Erro ao atualizar o favorito")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        
def delete_favoritos():
    # Delete
    global db
    mycol = db.usuarios

    for cliente in mycol.find():
        print(f'Nome do cliente: {cliente.get("nome")}')
        print(f'CPF do cliente: {cliente.get("cpf")}')
        print(f'Favoritos do cliente: {cliente.get("favoritos")}')
        print("---------------------------------------")
    cpf_cliente = input("Digite o CPF do cliente: ")
    nome_favorito = input("Digite o nome do favorito a ser deletado: ")

    cliente = mycol.find_one({"cpf": cpf_cliente})
    if cliente is None:
        print("Cliente não encontrado.")
        return

    # Verifica se o favorito existe na lista de favoritos do cliente
    favorito_existe = any(favorito for favorito in cliente["favoritos"] if favorito["nome"] == nome_favorito)
    if not favorito_existe:
        print("Favorito não encontrado.")
        return

    confirmacao = input("Tem certeza que deseja deletar este favorito? (S/N)").upper()
    if confirmacao != 'S':
        print("Operação cancelada.")
        return

    # Remove o favorito da lista de favoritos do cliente
    cliente["favoritos"] = [favorito for favorito in cliente["favoritos"] if favorito["nome"] != nome_favorito]

    # Atualiza o documento do cliente no banco de dados
    result = mycol.update_one({"_id": cliente["_id"]}, {"$set": {"favoritos": cliente["favoritos"]}})
    if result.modified_count > 0:
        print("Favorito deletado com sucesso!")
    else:
        print("Erro ao deletar o favorito.")