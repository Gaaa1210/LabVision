# src/sistemadegestaodepacientes/model/atendimento_medico.py
from datetime import datetime
# Importações relativas dentro do pacote 'model'
from .paciente import Paciente
from .tipo_exame import TipoExame

class AtendimentoMedico:
    """
    Representa o registro de um atendimento médico.
    """
    def __init__(self, paciente: Paciente, observacoes: str,
                 necessita_exames: bool, tipo_exame_solicitado: TipoExame = None):
        self.paciente = paciente
        self.observacoes = observacoes
        self.necessita_exames = necessita_exames
        self.tipo_exame_solicitado = tipo_exame_solicitado
        self.data_atendimento = datetime.now() # Data e hora do atendimento

    def __str__(self):
        exame_str = f", Exame Solicitado: {self.tipo_exame_solicitado.value}" if self.necessita_exames and self.tipo_exame_solicitado else ""
        return (f"Atendimento para {self.paciente.nome} (CPF: {self.paciente.cpf})\n"
                f"  Data: {self.data_atendimento.strftime('%d/%m/%Y %H:%M:%S')}\n"
                f"  Observações: {self.observacoes}\n"
                f"  Necessita Exames: {'Sim' if self.necessita_exames else 'Não'}{exame_str}")