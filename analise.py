import dados


exames_pacientes = dados.exames_pacientes

def verificar_exames_fora_padrao(exames_pacientes):
    
    limite_referencia = {
        'largura':(1.5, 3.0),
        'comprimento':(2.0, 6.0),
        'altura':(1.8, 3.5)
    }

    exames_fora_padrao = {}

    for exame, valor in exames_pacientes.items():
        minimo, maximo = limite_referencia[exame]
        if valor < minimo or valor > maximo:
            exames_fora_padrao[exame] = valor

    return exames_fora_padrao


for paciente, exames in exames_pacientes.items():

    fora_padrao = verificar_exames_fora_padrao(exames)

    if fora_padrao:
        print(f"Paciente {paciente} possui exames fora do padrão: {fora_padrao}")
    else:
        print(f"Paciente {paciente} está com todos os exames dentro do padrão.")