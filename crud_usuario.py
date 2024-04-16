from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://<user>:<senha>@<nome_colecao>.tooadgk.mongodb.net/?retryWrites=true&w=majority&appName=<nome_colecao>"

client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercado_livre

def create_usuario():
    #Insert
    global db
    mycol = db.usuarios
    print("\nInserindo um novo usuário")
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cpf = input("CPF: ")
    email = input("Email: ")
    key = 'S'  
    end = []
    while (key.upper() != 'N'):
        print("\nInserindo um novo endereço")
        rua = input("Rua: ")
        num = input("Num: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        cep = input("CEP: ")
        endereco = {        
            "rua":rua,
            "num": num,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }
        end.append(endereco) 
        key = input("Deseja cadastrar um novo endereço (S/N)? ")
    mydoc = { "nome": nome, "sobrenome": sobrenome, "cpf": cpf, "endereco": end, "email": email }
    x = mycol.insert_one(mydoc)
    print("Documento inserido com ID ",x.inserted_id)

def read_all_usuario():
    #Read
    global db
    mycol = db.usuarios
    mydoc = mycol.find()
    for x in mydoc:
        print(f'Nome do usuário: {x.get("nome")}')
        print(f'Sobrenome do usuário: {x.get("sobrenome")}')
        print(f'CPF do usuário: {x.get("cpf")}')
        print(f'Email do usuário: {x.get("email")}')
        print("Endereços do usuário: ")
        print(f'Endereço do usuário: {x.get("endereco")}')
        print(f'Favoritos do usuário: {x.get("favoritos")}')
        print("-------------------------------------------------------------------------------------------------------")

def read_usuario(nome):
    #Read
    global db
    mycol = db.usuarios
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

def update_usuario():
    # Update
    global db
    mycol_usuario = db.usuarios

    for usuario in mycol_usuario.find():
        print(f'Nome do usuário: {usuario.get("nome")}')
        print(f'CPF do usuário: {usuario.get("cpf")}')
        print("---------------------------------------")

    # Encontrar o usuário pelo CPF
    cpf_usuario = input("Digite o CPF do usuário que deseja atualizar: ")
    usuario = mycol_usuario.find_one({"cpf": cpf_usuario})

    if usuario is None:
        print("Usuário não encontrado.")
        return

    # Solicitar as atualizações dos dados do usuário
    novo_nome = input(f"Novo nome ({usuario['nome']}): ").strip()
    novo_sobrenome = input(f"Novo sobrenome ({usuario['sobrenome']}): ").strip()
    novo_cpf = input(f"Novo CPF ({usuario['cpf']}): ").strip()
    novo_email = input(f"Novo email ({usuario['email']}): ").strip()

    # Atualizar os endereços do usuário
    novos_enderecos = []
    for endereco in usuario['endereco']:
        print("\nEndereço atual:")
        print("Rua:", endereco["rua"])
        print("Número:", endereco["num"])
        print("Bairro:", endereco["bairro"])
        print("Cidade:", endereco["cidade"])
        print("Estado:", endereco["estado"])
        print("CEP:", endereco["cep"])
        print("-" * 20)
        key = input("Deseja atualizar este endereço (S/N)? ").strip().upper()
        if key == 'S':
            novo_rua = input("Nova rua: ").strip()
            novo_num = input("Novo número: ").strip()
            novo_bairro = input("Novo bairro: ").strip()
            nova_cidade = input("Nova cidade: ").strip()
            novo_estado = input("Novo estado: ").strip()
            novo_cep = input("Novo CEP: ").strip()
            novo_endereco = {
                "rua": novo_rua if novo_rua else endereco["rua"],
                "num": novo_num if novo_num else endereco["num"],
                "bairro": novo_bairro if novo_bairro else endereco["bairro"],
                "cidade": nova_cidade if nova_cidade else endereco["cidade"],
                "estado": novo_estado if novo_estado else endereco["estado"],
                "cep": novo_cep if novo_cep else endereco["cep"]
            }
            novos_enderecos.append(novo_endereco)
        else:
            novos_enderecos.append(endereco)

    # Atualizar os dados do usuário
    novos_dados_usuario = {
        "nome": novo_nome if novo_nome else usuario['nome'],
        "sobrenome": novo_sobrenome if novo_sobrenome else usuario['sobrenome'],
        "cpf": novo_cpf if novo_cpf else usuario['cpf'],
        "email": novo_email if novo_email else usuario['email'],
        "endereco": novos_enderecos
    }

    # Atualizar o documento do usuário no banco de dados
    mycol_usuario.update_one({"_id": usuario["_id"]}, {"$set": novos_dados_usuario})

    print("Usuário atualizado com sucesso!")

def delete_usuario(cpf):
    #Delete
    global db
    mycol = db.usuarios
    myquery = {"cpf": cpf}

    usuario = mycol.find_one(myquery)
    if usuario is None:
        print("Usuário não encontrado.")
        return

    nome_usuario = usuario["nome"]

    mydoc = mycol.delete_one(myquery)
    print("Deletado o usuário ",nome_usuario)