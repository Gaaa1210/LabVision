
clientes ={
    'joao de farias':{
        'nome': "João de farias",
        'cpf' : 123456789,
        'idade': 63,

    }
}

exames = {
    'joao de farias' : {
        'exame_1':{
            'valor_1': 1,
            'valor_2': 2,
            'result': 'possitivo' 
        } 
    }
}


def cadastrarCliente():
    global exames, clientes
    
    nome = input("Nome do paciente: ").strip().lower()
    cpf = input("CPF (apenas números): ").strip()
    idade = input("idade: ").strip()

    if nome in clientes:
        print("cliente já possui cadastro")

        return
    
    if not cpf.isdigit() or not idade.isdigit():
        print("CPF e idade teve conter apenas números.")
        return
    


    clientes[nome] = {
        'nome': nome.title(),
        'cpf': int(cpf),
        'idade': int(idade)
    }


    exames[nome] = {}

    print("cliente cadastrado com sucesso!!!")
    

def cadastrarExame():
    global exames

    nome = input("Nome do paciente: ").strip().lower()

    if nome  not in clientes:
        print("Cliente não encontrado")
        return

    nome_exame = input("nome do exame: ").strip().lower()
    valor_1 = input("valor 1: ").strip()
    valor_2 = input("valor 2: ").strip()
    result = input("result: ").strip().lower()


    if not valor.replace('.','', 1).isdigit() or not result.replace(',','', 1).isdigit():
        print("valores invalidos. Use apenas números")
        return


    exames[nome][nome_exame] = {
        'valor_1': float(valor_1),
        'valor_2': float(valor_2),
        'result': str(result)
    }

    print("Exame criado com sucesso!")
    



def buscarExames():
    global exames
    nome = input("Digite o nome do cliente: ").strip().lower()

    if nome not in exames:

        print("Paciente não encontrado")
        return
    
    if not exames[nome]:
        print("Este cliente não possui exames cadastrados.")
        return 

    print(f"\nExames do cliente {clientes[nome]['nome']}:\n")

    for exames, dados in exames[nome].items():
        print(f"- {exames}:")
        print(f"   Valor_1: {dados['valor_1']}")
        print(f"   Valor_2: {dados['valor_2']}")
        print(f"   result: {dados['result']}\n")




buscarExames()

print(f'clientes = {clientes}')
print(f'exames = {exames} ')
