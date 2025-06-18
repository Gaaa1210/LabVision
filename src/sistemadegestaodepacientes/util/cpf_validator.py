def is_valid_cpf(cpf: str) -> bool:
    """
    Valida um número de CPF.
    Retorna True se o CPF for válido, False caso contrário.
    Esta é uma implementação simplificada para fins de exemplo acadêmico.
    Para uma validação completa, incluir os dígitos verificadores é essencial.
    """
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False
    
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    digito1 = 11 - (soma % 11)
    if digito1 > 9:
        digito1 = 0

    if int(cpf[9]) != digito1:
        return False

    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    digito2 = 11 - (soma % 11)
    if digito2 > 9:
        digito2 = 0
        
    if int(cpf[10]) != digito2:
        return False

    return True