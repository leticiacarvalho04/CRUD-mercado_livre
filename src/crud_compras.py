import conexao
db = conexao.db

def create_compras():
    # Insert
    global db
    mycol_compra = db.compras
    mycol_produto = db.produtos
    mycol_usuario = db.usuarios
    mycol_vendedor = db.vendedor

    cpf_cliente = input("Digite o cpf do cliente: ")
    cpf_vendedor = input("Digite o cpf do vendedor: ")

    vendedor = mycol_vendedor.find_one({"cpf": cpf_vendedor})
    if vendedor is None:
        print("Vendedor não encontrado.")
        return

    print("\nProdutos disponíveis:")
    for produto_id in vendedor.get('produtos', []):
        produto = mycol_produto.find_one({"_id": produto_id})
        if produto is not None:
            print(f"ID: {produto['_id']}, Nome: {produto['nome']}, Preço: {produto['preco']}")
        
    produto_id = input("Digite o ID do produto desejado: ")

    if produto_id not in vendedor.get('produtos', []):
        print("Produto não pertence ao vendedor selecionado.")
        return
    
    produto = mycol_produto.find_one({"_id": produto_id})
    if produto is None:
        print("Produto não encontrado.")
        return

    print("\nInserindo uma nova compra")
    qnt = int(input("Quantidade: "))  
    total = int(produto["preco"]) * qnt  

    # Dados do cliente
    cliente = mycol_usuario.find_one({"cpf": cpf_cliente})
    if cliente is None:
        print("Cliente não encontrado.")
        return

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

    mydoc = {
        "produto": produto_data,
        "quantidade": qnt,
        "total": total,
        "usuario": usuario,
        "vendedor_cpf": cpf_vendedor  
    }

    x = mycol_compra.insert_one(mydoc)
    print("Documento inserido com ID ", x.inserted_id)

def read_compras(nome):
    # Read
    global db
    mycol_compras = db.compras

    myquery = {"usuario.nome": nome}
    mydoc = mycol_compras.find(myquery)

    count = mycol_compras.count_documents(myquery)

    if count == 0:
        print("Nenhuma compra encontrada para este cliente.")
        return

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
    
    indice = int(input(f"Digite o número da compra que deseja excluir (1-{len(compras)}): "))
    
    if indice < 1 or indice > len(compras):
        print("Índice inválido.")
        return
    
    compra_selecionada = compras[indice - 1]
    
    mycol.delete_one({"_id": compra_selecionada["_id"]})
    
    print(f"Compra do produto '{compra_selecionada['produto']['nome']}' deletada com sucesso para o usuário {nome_usuario}.")