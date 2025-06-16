# src/sistemadegestaodepacientes/modulo_consultorio_medico/service/atendimento_service.py

# IMPORTAÇÕES CORRIGIDAS PARA O CAMINHO RELATIVO
from ..model.paciente import Paciente
from ..model.atendimento_medico import AtendimentoMedico
from ..model.tipo_exame import TipoExame
from ..repository.atendimento_medico_repository import AtendimentoMedicoRepository
from .fila_service import FilaService
from ..service.exame_service import ExameService

class AtendimentoService:
    def __init__(self):
        self.atendimento_repo = AtendimentoMedicoRepository()  # Corrigido aqui
        self.fila_service = FilaService()

    def registrar_atendimento_medico(self, paciente: Paciente, observacoes: str,
                                     necessita_exames: bool, tipo_exame_solicitado: TipoExame = None) -> tuple[AtendimentoMedico | None, str]:
        """
        Registra um atendimento médico para um paciente.
        Move o paciente para a fila de exames se necessário.
        """
        if necessita_exames and not tipo_exame_solicitado:
            return None, "Erro: Tipo de exame deve ser especificado se exames são necessários."

        # Cria o objeto AtendimentoMedico
        novo_atendimento = AtendimentoMedico(
            paciente=paciente,
            observacoes=observacoes,
            necessita_exames=necessita_exames,
            tipo_exame_solicitado=tipo_exame_solicitado
        )

        # 1. Registra o atendimento no repositório de atendimentos
        self.atendimento_repo.registrar_atendimento(novo_atendimento)

        # 2. Remove o paciente da fila de atendimento
        self.fila_service.remover_paciente_fila_atendimento(paciente)
        print(f"DEBUG: Paciente '{paciente.nome}' removido da fila de atendimento médico.")

        # 3. Se necessita exames, adiciona o paciente à fila de exames
        if necessita_exames:
            exame_service = ExameService()
            exame_service.adicionar_paciente_exame(paciente)
            return novo_atendimento, "Atendimento registrado. Paciente movido para a fila de exames."
        else:
            return novo_atendimento, "Atendimento registrado. Paciente finalizou o fluxo médico."
