#Define o que é um paciente (com atributos como nome, CPF, idade, etc.)
from datetime import datetime
from sistemadegestaodepacientes.model.prioridade_cor import PrioridadeCor 

class Paciente:
    
    def __init__(self, nome: str, data_nascimento: date, cpf:str, sexo: str, problema_saude: list = None, alergias_medicamentos: list = None, cor_prioridade: PrioridadeCor = None):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.sexo = sexo
        self.problema_saude = problema_saude if problema_saude is not None else []
        self.alergias_medicamentos = alergias_medicamentos if alergias_medicamentos is not None else []
        self.cor_prioridade = cor_prioridade
        self.data_cadastro = datetime.now()

    @property
    def idade(self) -> int:
        """Calcular a idade do paciente com base na data de nascimento."""
        today = datetime.now()
        return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
    
    def __str__(self) -> str:
        """Retornar uma representacao em string do paciente para facil visualizacao."""
        prioridade_str = str(self.cor_prioridade) if self.cor_prioridade else "Não definida"
        return (f"Nome{self.nome}," 
                f"CPF: {self.cpf}," 
                f"Idade: {self.idade}," 
                f"Prioridade: {prioridade_str}," 
                f"Chegada: {self.data_cadastro.strftime('%d/%m/%Y %H:%M:%S')}, ")

    def __eq__(self, other):
        """Comprar pacientes com base no CPF para garantir unicidade."""
        if not isinstance(other, Paciente):
            return NotImplemented
        return self.cpf == other.cpf
    
    def __hash__(self) -> int:
        """Definir um hash do paciente com base no CPF, util para dicionários ou conjuntos."""
        return hash(self.cpf)
    
