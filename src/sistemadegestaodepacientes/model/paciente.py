
from datetime import date, datetime
from .prioridade_cor import PrioridadeCor

class Paciente:
    def __init__(self, nome: str, data_nascimento: date, cpf:str, sexo: str,
        problemas_saude: list = None, 
        alergias_medicamentos: list = None,
        cor_prioridade: PrioridadeCor = None):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.sexo = sexo
        self.problemas_saude = problemas_saude if problemas_saude is not None else [] # <--- E AQUI
        self.alergias_medicamentos = alergias_medicamentos if alergias_medicamentos is not None else []
        self.cor_prioridade = cor_prioridade
        self.data_chegada = datetime.now() 

    @property
    def idade(self) -> int:
        """Calcula a idade do paciente com base na data de nascimento."""
        today = date.today() 
        return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))

    def __str__(self) -> str:
        """Retorna uma representacao em string do paciente para facil visualizacao."""
        prioridade_str = str(self.cor_prioridade) if self.cor_prioridade else "Não definida"
        return (f"Nome: {self.nome}, " 
                f"CPF: {self.cpf}, "
                f"Idade: {self.idade}, "
                f"Prioridade: {prioridade_str}, "
                f"Chegada: {self.data_chegada.strftime('%d/%m/%Y %H:%M:%S')}") 

    def __eq__(self, other):
        """Compara pacientes com base no CPF para garantir unicidade."""
        if not isinstance(other, Paciente):
            return NotImplemented
        return self.cpf == other.cpf

    def __hash__(self) -> int:
        """Define o hash do paciente com base no CPF, útil para dicionários ou conjuntos."""
        return hash(self.cpf)