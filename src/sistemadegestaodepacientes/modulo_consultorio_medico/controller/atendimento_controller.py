


from ...model.paciente import Paciente
from ...model.tipo_exame import TipoExame
from ...model.atendimento_medico import AtendimentoMedico
from ...service.atendimento_service import AtendimentoService
from ...service.fila_service import FilaService
from ...service.exame_service import ExameService 

class AtendimentoController:
    """
    Controla as interações do consultório médico.
    """
    def __init__(self):
        self.atendimento_service = AtendimentoService()
        self.fila_service = FilaService()
        self.exame_service = ExameService()

    def obter_proximo_paciente_fila_atendimento(self) -> Paciente | None:
        fila = self.fila_service.listar_fila_atendimento()
        return fila[0] if fila else None

    def processar_atendimento_medico(self, paciente: Paciente, observacoes: str,
                                     necessita_exames: bool, tipo_exame_opcao: str = None) -> tuple[AtendimentoMedico | None, str]:
        tipo_exame_obj = None
        if necessita_exames:
            try:
                tipo_exame_obj = TipoExame[tipo_exame_opcao.upper()]
            except KeyError:
                return None, "Erro: Tipo de exame inválido."

        atendimento, mensagem = self.atendimento_service.registrar_atendimento_medico(
            paciente=paciente,
            observacoes=observacoes,
            necessita_exames=necessita_exames,
            tipo_exame_solicitado=tipo_exame_obj
        )

        
        if atendimento and necessita_exames:
            self.exame_service.adicionar_paciente_exame(paciente)

        return atendimento, mensagem

    def listar_fila_atendimento(self) -> list[Paciente]:
        return self.fila_service.listar_fila_atendimento()
