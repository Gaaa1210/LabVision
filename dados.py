exames_pacientes = {
    'ygor': {'largura': 2.7, 'comprimento': 1.5, 'altura': 3.0},
    'gabriel': {'largura': 1.2, 'comprimento': 7.0, 'altura': 2.1},
    'jose': {'largura': 3.5, 'comprimento': 5.5, 'altura': 3.8},
    'luana': {'largura': 1.4, 'comprimento': 4.2, 'altura': 1.5},
    'ana': {'largura': 2.1, 'comprimento': 2.8, 'altura': 2.5},
    'augusto': {'largura': 1.9, 'comprimento': 6.5, 'altura': 3.2},
    'bruce': {'largura': 2.5, 'comprimento': 5.0, 'altura': 3.0},
    'hernandes': {'largura': 1.3, 'comprimento': 3.0, 'altura': 3.7},
    'junior': {'largura': 2.8, 'comprimento': 1.9, 'altura': 2.0},
    'izabela': {'largura': 2.0, 'comprimento': 4.5, 'altura': 3.6}
}



def preencher_formulario():
    print("===Cadastro de Cliente===")

    nome = input("Digite o nome do paciente: ")
    idade = int(input("Digite a idade do paciente: "))
    altura = float(input("Digite a altura do paciente (em metros): "))
    peso = float(input("Digite o peso do paciente (em kg): "))
    sexo = input("Digite o sexo do paciente (Masculino/Feminino): ")
    cidade = input("Digite a cidade do paciente: ")
    exame = input("Digite o tipo de exame: ")
    



#dados_cliente= {"Thalynne":{"id": 111111, "idade": 20, "altura": 1.70, "peso": 60.0, "sexo": "Feminino", "cidade": "São Paulo" "exame":"laparoscopia"}}