#Quais são as necessidades de um exame? Eu tenho que apenas especificar o nome do exame?
# src/sistemadegestaodepacientes/model/exame.py
from datetime import datetime
# Importações relativas dentro do pacote 'model'
from .paciente import Paciente
from .tipo_exame import TipoExame

class Exame:
    """
    Representa um exame realizado, incluindo os resultados e informações observadas.
    """
    def __init__(self, paciente: Paciente, tipo_exame: TipoExame,
                 largura: float = None, altura: float = None, comprimento: float = None,
                 informacoes_observadas: str = None, exame_realizado: bool = False):
        self.paciente = paciente
        self.tipo_exame = tipo_exame
        self.largura = largura
        self.altura = altura
        self.comprimento = comprimento
        self.informacoes_observadas = informacoes_observadas if informacoes_observadas is not None else ""
        self.exame_realizado = exame_realizado # Campo de confirmação
        self.data_realizacao = datetime.now() if exame_realizado else None # Data de registro do exame

    def __str__(self):
        status = "Realizado" if self.exame_realizado else "Pendente"
        medidas = ""
        if self.largura is not None or self.altura is not None or self.comprimento is not None:
            medidas = f", Medidas: L={self.largura or 'N/A'}, A={self.altura or 'N/A'}, C={self.comprimento or 'N/A'}"

        return (f"Exame de {self.tipo_exame.value} para {self.paciente.nome} (CPF: {self.paciente.cpf})\n"
                f"  Status: {status}\n"
                f"  Data Realização: {self.data_realizacao.strftime('%d/%m/%Y %H:%M:%S') if self.data_realizacao else 'N/A'}\n"
                f"  Observações do Exame: {self.informacoes_observadas}{medidas}")