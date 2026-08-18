# ============================================================
# SISTEMA BANCÁRIO
# Projeto desenvolvido em Python
# ============================================================

menu = """
=============================
       SISTEMA BANCÁRIO
=============================

[d] Depositar
[s] Sacar
[e] Extrato
[u] Criar usuário
[c] Criar conta
[l] Listar contas
[q] Sair

=> """


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"\nDepósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("\nOperação falhou! O valor informado é inválido.")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor <= 0:
        print("\nOperação falhou! O valor informado é inválido.")

    elif valor > saldo:
        print("\nOperação falhou! Você não possui saldo suficiente.")

    elif valor > limite:
        print("\nOperação falhou! O valor do saque excede o limite.")

    elif numero_saques >= limite_saques:
        print("\nOperação falhou! Número máximo de saques atingido.")

    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

        print(f"\nSaque de R$ {valor:.2f} realizado com sucesso!")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n=============================")
    print("           EXTRATO")
    print("=============================")

    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        print(extrato)

    print(f"Saldo: R$ {saldo:.2f}")
    print("=============================")


def criar_usuario(usuarios):
    print("\n=============================")
    print("       CRIAR USUÁRIO")
    print("=============================")

    cpf = input("CPF (somente números): ").strip()

    if any(usuario["cpf"] == cpf for usuario in usuarios):
        print("\nOperação falhou! Já existe um usuário com esse CPF.")
        return

    nome = input("Nome completo: ").strip()
    data_nascimento = input("Data de nascimento: ").strip()
    endereco = input("Endereço: ").strip()

    usuario = {
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
    }

    usuarios.append(usuario)

    print("\nUsuário criado com sucesso!")


def criar_conta(agencia, numero_conta, usuarios, contas):
    print("\n=============================")
    print("        CRIAR CONTA")
    print("=============================")

    cpf = input("Informe o CPF do usuário: ").strip()

    usuario = next(
        (usuario for usuario in usuarios if usuario["cpf"] == cpf),
        None
    )

    if usuario is None:
        print("\nOperação falhou! Usuário não encontrado.")
        return numero_conta

    conta = {
        "agencia": agencia,
        "numero": numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "limite": 500,
        "numero_saques": 0,
        "extrato": "",
    }

    contas.append(conta)

    print("\nConta criada com sucesso!")
    print(f"Agência: {agencia}")
    print(f"Número da conta: {numero_conta}")
    print(f"Titular: {usuario['nome']}")

    return numero_conta + 1


def listar_contas(contas):
    print("\n=============================")
    print("        CONTAS CADASTRADAS")
    print("=============================")

    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    for conta in contas:
        print(f"""
Agência: {conta['agencia']}
Conta: {conta['numero']}
Titular: {conta['usuario']['nome']}
CPF: {conta['usuario']['cpf']}
Saldo: R$ {conta['saldo']:.2f}
-----------------------------""")


def selecionar_conta(contas):
    if not contas:
        print("\nNenhuma conta cadastrada.")
        return None

    cpf = input("Informe o CPF do titular: ").strip()

    contas_usuario = [
        conta
        for conta in contas
        if conta["usuario"]["cpf"] == cpf
    ]

    if not contas_usuario:
        print("\nNenhuma conta encontrada para esse CPF.")
        return None

    if len(contas_usuario) == 1:
        return contas_usuario[0]

    print("\nContas encontradas:")

    for indice, conta in enumerate(contas_usuario, start=1):
        print(
            f"{indice} - Agência: {conta['agencia']} "
            f"| Conta: {conta['numero']}"
        )

    try:
        opcao = int(input("Escolha a conta: "))

        if 1 <= opcao <= len(contas_usuario):
            return contas_usuario[opcao - 1]

    except ValueError:
        pass

    print("\nOpção inválida.")
    return None


def main():
    LIMITE_SAQUES = 3
    LIMITE = 500
    AGENCIA = "0001"

    usuarios = []
    contas = []
    numero_conta = 1

    while True:
        opcao = input(menu).lower().strip()

        if opcao == "d":
            conta = selecionar_conta(contas)

            if conta:
                try:
                    valor = float(
                        input("Informe o valor do depósito: R$ ")
                    )

                    conta["saldo"], conta["extrato"] = depositar(
                        conta["saldo"],
                        valor,
                        conta["extrato"],
                    )

                except ValueError:
                    print("\nValor inválido.")

        elif opcao == "s":
            conta = selecionar_conta(contas)

            if conta:
                try:
                    valor = float(
                        input("Informe o valor do saque: R$ ")
                    )

                    (
                        conta["saldo"],
                        conta["extrato"],
                        conta["numero_saques"],
                    ) = sacar(
                        saldo=conta["saldo"],
                        valor=valor,
                        extrato=conta["extrato"],
                        limite=conta["limite"],
                        numero_saques=conta["numero_saques"],
                        limite_saques=LIMITE_SAQUES,
                    )

                except ValueError:
                    print("\nValor inválido.")

        elif opcao == "e":
            conta = selecionar_conta(contas)

            if conta:
                exibir_extrato(
                    conta["saldo"],
                    extrato=conta["extrato"],
                )

        elif opcao == "u":
            criar_usuario(usuarios)

        elif opcao == "c":
            numero_conta = criar_conta(
                AGENCIA,
                numero_conta,
                usuarios,
                contas,
            )

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            print("\nObrigado por utilizar o Sistema Bancário!")
            break

        else:
            print("\nOperação inválida. Por favor, selecione uma opção válida.")


if __name__ == "__main__":
    main()
