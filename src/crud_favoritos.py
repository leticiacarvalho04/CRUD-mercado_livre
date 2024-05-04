from bson import ObjectId
import conexao

db = conexao

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

    if not isinstance(cliente.get('favoritos'), list):
        mycol_usuario.update_one(
            {"_id": cliente["_id"]},
            {"$set": {"favoritos": []}}
        )

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
    
    clientes = clientes_col.find()
    
    for cliente in clientes:
        cliente_nome = cliente["nome"]  
        
        print(f"Cliente: {cliente_nome}")
        
        if "favoritos" in cliente:
            favoritos = cliente.get("favoritos", [])  
            
            print("Favoritos:")
            for favorito in favoritos:
                print(f"- {favorito}") 
        else:
            print("Sem favoritos.")
        
        print("----------------------")

def read_favoritos(cpf):
    global db
    clientes_col = db.usuarios
    
    cliente = clientes_col.find_one({"cpf": cpf}) 
    
    if cliente:
        cliente_nome = cliente["nome"]  
        
        print(f"Favoritos do cliente {cliente_nome} (CPF: {cpf}):")
        
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

    clientes_com_favoritos = mycol_usuario.find({"favoritos": {"$exists": True, "$ne": []}})
    
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

    favorito_antigo_obj = [fav for fav in cliente['favoritos'] if fav['produto_id'] == favorito_antigo]
    
    if not favorito_antigo_obj:
        print("Favorito antigo não encontrado.")
        return

    novo_produto_obj = mycol_produto.find_one({"_id": novo_produto_id})
    if novo_produto_obj is None:
        print("Novo produto não encontrado.")
        return

    quantidade_parcelas = int(input("Digite a quantidade de parcelas desejadas: "))

    try:
        result = mycol_usuario.update_one(
            {"cpf": cpf_cliente, "favoritos.produto_id": favorito_antigo},
            {"$set": {"favoritos.$": {
                "produto_id": novo_produto_id,
                "nome": novo_produto_obj["nome"],
                "preco": novo_produto_obj["preco"],
                "parcelas": quantidade_parcelas 
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

    favorito_existe = any(favorito for favorito in cliente["favoritos"] if favorito["nome"] == nome_favorito)
    if not favorito_existe:
        print("Favorito não encontrado.")
        return

    confirmacao = input("Tem certeza que deseja deletar este favorito? (S/N)").upper()
    if confirmacao != 'S':
        print("Operação cancelada.")
        return

    cliente["favoritos"] = [favorito for favorito in cliente["favoritos"] if favorito["nome"] != nome_favorito]

    result = mycol.update_one({"_id": cliente["_id"]}, {"$set": {"favoritos": cliente["favoritos"]}})
    if result.modified_count > 0:
        print("Favorito deletado com sucesso!")
    else:
        print("Erro ao deletar o favorito.")