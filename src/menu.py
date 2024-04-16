import crud_usuario
import crud_vendedor
import crud_produto
import crud_compras
import crud_favoritos

key = 0
sub = 0

while (key != 'S'.lower()):
    print("1-CRUD Usuário")
    print("2-CRUD Vendedor")
    print("3-CRUD Produto")
    print("4-CRUD Compras")
    print("5-CRUD Favoritos")
    key = input("Digite a opção desejada? (S para sair) ")

    if (key == '1'):
        print("Menu do Usuário")
        print("1-Create User")
        print("2-Read User")
        print("3-Read All User")
        print("4-Update User")
        print("5-Delete User")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            print("Create usuario")
            crud_usuario.create_usuario()
            
        elif (sub == '2'):
            crud_usuario.read_all_usuario()
            cpf = input("Read usuário, deseja algum cpf de um usuário especifico? ")
            crud_usuario.read_usuario(cpf)

        elif (sub == '3'):
            crud_usuario.read_all_usuario()
        
        elif (sub == '4'):
            crud_usuario.update_usuario()

        elif (sub == '5'):
            print("delete usuario")
            nome = input("Nome a ser deletado: ")
            sobrenome = input("Sobrenome a ser deletado: ")
            crud_usuario.delete_usuario(nome, sobrenome)
            
    elif (key == '2'):
        print("Menu do Vendedor")   
        print("1-Create Vendedor")
        print("2-Read Vendedor")
        print("3-Read Todos os Vendedores")
        print("4-Update Vendedor")
        print("5-Delete Vendedor")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            print("Create vendedor")
            crud_vendedor.create_vendedor()
            
        elif (sub == '2'):
            cpf = input("Read vendedor, deseja o cpf de um vendedor especifico? ")
            crud_vendedor.read_vendedor(cpf)

        elif (sub == '3'):
            crud_vendedor.read_all_vendedor()
        
        elif (sub == '4'):
            crud_vendedor.read_all_vendedor()
            cpf = input("Update vendedor, deseja algum cpf de um vendedor especifico? ")
            crud_vendedor.update_vendedor(cpf)

        elif (sub == '5'):
            crud_vendedor.read_all_vendedor()
            cpf = input("CPF do vendedor a ser deletado: ")
            crud_vendedor.delete_vendedor(cpf)    

    elif (key == '3'):
        print("Menu do Produto") 
        print("1-Create Produto")
        print("2-Read Produto")
        print("3-Read Todos Produto")
        print("4-Update Produto")
        print("5-Delete Produto")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            print("Create produto")
            crud_produto.create_produtos()
            
        elif (sub == '2'):
            nome = input("Read produto, deseja algum nome especifico? ")
            crud_produto.read_produtos(nome)

        elif (sub == '3'):
            crud_produto.read_all_produtos()
        
        elif (sub == '4'):
            crud_produto.read_all_produtos()
            nome = input("Update produto, deseja algum nome especifico? ")
            crud_produto.update_produtos(nome)

        elif (sub == '5'):
            crud_produto.read_all_produtos()
            nome = input("Nome a ser deletado: ")
            crud_produto.delete_produtos(nome)  

    elif (key == '4'):
        print("Menu do Compras") 
        print("1-Create Compras")
        print("2-Read Compras")
        print("3-Read Todas as Compras")
        print("4-Delete Compras")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            print("Create compra")
            crud_usuario.read_all_usuario()
            crud_vendedor.read_all_vendedor()
            crud_compras.create_compras()
            
        elif (sub == '2'):
            nome = input("Read compra, deseja algum nome de um cliente especifico? ")
            crud_compras.read_compras(nome)

        elif (sub == '3'):
            crud_compras.read_all_compras()

        elif (sub == '4'):
            print("delete compra")
            nome_usuario = input("Nome do usuario que realizou a compra deletado: ")
            crud_compras.delete_compras(nome_usuario)       

    elif (key == '5'):
        print("Menu dos favoritos") 
        print("1-Create favoritos")
        print("2-Read favoritos")
        print("3-Read Todos os favoritos")
        print("4-Update favoritos")
        print("5-Delete favoritos")
        sub = input("Digite a opção desejada? (V para voltar) ")
        if (sub == '1'):
            print("Create favoritos")
            crud_usuario.read_all_usuario()
            crud_produto.read_all_produtos()
            crud_favoritos.create_favoritos()
            
        elif (sub == '2'):
            cpf = input("Read favoritos, deseja algum cpf especifico? ")
            crud_favoritos.read_favoritos(cpf)

        elif (sub == '3'):
            crud_favoritos.read_all_favoritos()
        
        elif (sub == '4'):
            crud_favoritos.update_favoritos()

        elif (sub == '5'):
            print("delete favorito")
            crud_favoritos.delete_favoritos()  

print("Tchau :)")