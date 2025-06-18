# src/sistemadegestaodepacientes/service/atendimento_service.py
from datetime import datetime

# IMPORTAÇÕES CORRIGIDAS PARA O CAMINHO RELATIVO
from ..model.paciente import Paciente
from ..model.atendimento_medico import AtendimentoMedico
from ..model.tipo_exame import TipoExame
from ..repository.atendimento_medico_repository import AtendimentoMedicoRepository
from .fila_service import FilaService # Importa FilaService para interagir com as filas

class AtendimentoService:
    """
    Gerencia a lógica de negócio do atendimento médico.
    Responsável por registrar atendimentos e interagir com as filas.
    """
    def __init__(self):
        self.atendimento_repo = AtendimentoMedicoRepository()
        self.fila_service = FilaService() 

    def registrar_atendimento_medico(self, paciente: Paciente, observacoes: str,
                                    necessita_exames: bool, tipo_exame_solicitado: TipoExame = None) -> tuple[AtendimentoMedico, str]:
        """
        Registra um atendimento médico para um paciente.
        Move o paciente para a fila de exames se necessário.
        """
        if necessita_exames and not tipo_exame_solicitado:
            return None, "Erro: Tipo de exame deve ser especificado se exames são necessários."

        novo_atendimento = AtendimentoMedico(
            paciente=paciente,
            observacoes=observacoes,
            necessita_exames=necessita_exames,
            tipo_exame_solicitado=tipo_exame_solicitado
        )

        self.atendimento_repo.registrar_atendimento(novo_atendimento)

        self.fila_service.remover_paciente_fila_atendimento(paciente)
        print(f"DEBUG: Paciente '{paciente.nome}' removido da fila de atendimento médico.")

    
        if necessita_exames:
            self.fila_service.adicionar_paciente_fila_exames(paciente) 
            return novo_atendimento, "Atendimento registrado. Paciente movido para a fila de exames."
        else:
            return novo_atendimento, "Atendimento registrado. Paciente finalizou o fluxo médico."

    def listar_fila_atendimento_para_medico(self) -> list[Paciente]:
        """
        Retorna a lista de pacientes na fila de atendimento médico,
        para que o médico possa visualizar quem atender.
        """
        return self.fila_service.listar_fila_atendimento()

    def buscar_atendimento_por_cpf(self, cpf: str) -> AtendimentoMedico | None:
        """Busca o último atendimento de um paciente pelo CPF."""
        return self.atendimento_repo.buscar_atendimento_por_cpf(cpf)