# src/sistemadegestaodepacientes/modulo_consultorio_medico/controller/atendimento_controller.py
# IMPORTAÇÕES CORRIGIDAS PARA O CAMINHO RELATIVO:
from ...model.paciente import Paciente
from ...model.tipo_exame import TipoExame
from ...model.atendimento_medico import AtendimentoMedico
from ...service.atendimento_service import AtendimentoService
from ...service.fila_service import FilaService

class AtendimentoController:
    """
    Controla as interações do consultório médico.
    """
    def __init__(self):
        self.atendimento_service = AtendimentoService() # Instancia o AtendimentoService
        self.fila_service = FilaService() # Instancia o FilaService para listar a fila

    def obter_proximo_paciente_fila_atendimento(self) -> Paciente | None:
        """
        Retorna o paciente com a maior prioridade na fila de atendimento médico.
        """
        # Chama o serviço de fila para obter a lista já ordenada
        fila = self.fila_service.listar_fila_atendimento()
        return fila[0] if fila else None # O primeiro elemento é o de maior prioridade

    def processar_atendimento_medico(self, paciente: Paciente, observacoes: str,
                                     necessita_exames: bool, tipo_exame_opcao: str = None) -> tuple[AtendimentoMedico | None, str]:
        """
        Processa o atendimento do médico, registrando observações
        e decidindo o próximo passo (atendido ou exames).
        """
        tipo_exame_obj = None
        if necessita_exames:
            try:
                tipo_exame_obj = TipoExame[tipo_exame_opcao.upper()]
            except KeyError:
                return None, "Erro: Tipo de exame inválido."

        # Delega a lógica de registro e movimentação de fila ao AtendimentoService
        return self.atendimento_service.registrar_atendimento_medico(
            paciente=paciente,
            observacoes=observacoes,
            necessita_exames=necessita_exames,
            tipo_exame_solicitado=tipo_exame_obj
        )

    def listar_fila_atendimento(self) -> list[Paciente]:
        """Retorna a fila de atendimento médico para exibição."""
        return self.fila_service.listar_fila_atendimento()