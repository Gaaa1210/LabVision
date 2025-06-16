from ..model.paciente import Paciente
from ..model.atendimento_medico import AtendimentoMedico
from ..model.tipo_exame import TipoExame
from ..repository.atendimento_medico_repository import AtendimentoMedicoRepository
from .fila_service import FilaService
from ..service.exame_service import ExameService

class AtendimentoService:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(AtendimentoService, cls).__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self):
        if not self._inicializado:
            self.atendimento_repo = AtendimentoMedicoRepository()
            self.fila_service = FilaService()
            self._inicializado = True

    def registrar_atendimento_medico(self, paciente: Paciente, observacoes: str,
                                     necessita_exames: bool, tipo_exame_solicitado: TipoExame = None) -> tuple[AtendimentoMedico | None, str]:
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
            exame_service = ExameService()
            exame_service.adicionar_paciente_exame(paciente)
            print(f"DEBUG paciente enviado: {paciente.nome}, idade: {paciente.idade}, cor: {paciente.cor_prioridade}, chegada: {paciente.data_chegada}")
            return novo_atendimento, "Atendimento registrado. Paciente movido para a fila de exames."
        else:
            return novo_atendimento, "Atendimento registrado. Paciente finalizou o fluxo médico."
