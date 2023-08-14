
def menu_principal():
    menu = """

[u] Criar usuário
[a] Acessar usuário
[q] Sair

=> """

    opcao = input(menu)
    return opcao

def menu_secundario():
    menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[c] Criar conta
[l] Listar contas
[v] Voltar
[q] Sair

=> """

    opcao = input(menu)
    return opcao

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\nSaldo: R$ {saldo:.2f}\n"
        print("\n=== Depósito realizado com sucesso ===")

    else:
        print("\n<><><> Operação falhou! O valor informado é inválido. <><><>")

    return saldo, extrato

def sacar(*, valor, saldo, limite, extrato, numero_saques, limite_saques): 
    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n<><><> Operação falhou! Você não tem saldo suficiente. <><><>")

    elif excedeu_limite:
        print("\n<><><> Operação falhou! O valor do saque excede o limite. <><><>")

    elif excedeu_saques:
        print("\n<><><> Operação falhou! Número máximo de saques excedido. <><><>")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\nSaldo: R$ {saldo:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso ===")

    else:
        print("<><><> Operação falhou! O valor informado é inválido. <><><>")

    return saldo, extrato, numero_saques

def tirar_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe seu CPF (apenas números): ")
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print("\n<><><> Já existe usuário com esse CPF. <><><>")
        return

    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe seu endereço (logradouro, nº - bairro - cidade/sigla do estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("\n=== Cadastro de usuário realizado com sucesso ===")

def acessar_usuario(usuarios):
    cpf = input("Informe seu CPF (apenas números): ")
    usuario = filtrar_usuarios(cpf, usuarios)

    if not usuario:
        print("\n<><><> Não existe usuário com esse CPF. Crie um usuário. <><><>")
        return   

    print(f"\n=== Seja bem-vindo(a), {usuario['nome']}! ===")
    return usuario

def filtrar_usuarios(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe seu CPF (apenas números): ")
    usuario = filtrar_usuarios(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n<><><> Usuário não encontrado. É necessário criar um usuário primeiro. <><><>")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(linha)

def usuario_menu(usuarios):
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    contas = []

    while True:
        opcao = menu_secundario()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                valor=valor, 
                saldo=saldo, 
                limite=limite, 
                extrato=extrato, 
                numero_saques=numero_saques, 
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            tirar_extrato(saldo, extrato=extrato)

        elif opcao == "v":
            principal()
            break

        elif opcao == "c":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "q":
            break

        elif opcao == "l":
            if contas:
                listar_contas(contas)
            else:
                print("\n<><><> Você ainda não tem conta corrente. <><><>")
        else:
            print("\n<><><> Operação inválida, por favor selecione novamente a operação desejada. <><><>")

def principal(): 
    usuarios = []

    while True:
        opcao = menu_principal()

        if opcao == "u":
            criar_usuario(usuarios)

        elif opcao == "a":
            usuario = acessar_usuario(usuarios)
            if usuario:
                usuario_menu(usuarios)
                break
            

        elif opcao == "q":
            break
            
        else:
            print("\n<><><> Operação inválida, por favor selecione novamente a operação desejada. <><><>")

principal()