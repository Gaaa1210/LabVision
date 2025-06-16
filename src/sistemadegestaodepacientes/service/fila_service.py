from datetime import datetime
from ..model.paciente import Paciente
from ..model.prioridade_cor import PrioridadeCor
from ..repository.fila_atendimento_medico_repository import FilaAtendimentoMedicoRepository
from ..repository.fila_exames_repository import FilaExamesRepository

class FilaService:
    def __init__(self):
        self.fila_atendimento_repo = FilaAtendimentoMedicoRepository()
        self.fila_exames_repo = FilaExamesRepository()

    def _calcular_prioridade(self, paciente: Paciente) -> tuple:
        if paciente.cor_prioridade == PrioridadeCor.VERMELHA:
            peso_cor = 0
        elif paciente.cor_prioridade == PrioridadeCor.AMARELA:
            peso_cor = 1
        elif paciente.cor_prioridade == PrioridadeCor.VERDE:
            peso_cor = 2
        else:
            peso_cor = 3

        peso_idade = 0
        if paciente.idade >= 60:
            peso_idade = -2
        elif paciente.idade <= 6:
            peso_idade = -1

        peso_chegada = paciente.data_chegada.timestamp()

        return (peso_cor, peso_idade, peso_chegada)

    def _get_insertion_index(self, fila: list[Paciente], novo_paciente: Paciente) -> int:
        novo_peso = self._calcular_prioridade(novo_paciente)
        low = 0
        high = len(fila)

        while low < high:
            mid = (low + high) // 2
            mid_paciente = fila[mid]
            mid_peso = self._calcular_prioridade(mid_paciente)

            if novo_peso < mid_peso:
                high = mid
            else:
                low = mid + 1
        return low

    def adicionar_paciente_fila_atendimento(self, paciente: Paciente) -> None:
        idx = self._get_insertion_index(self.fila_atendimento_repo.get_fila(), paciente)
        self.fila_atendimento_repo.adicionar_paciente_no_indice(paciente, idx)

    def remover_paciente_fila_atendimento(self, paciente: Paciente) -> bool:
        return self.fila_atendimento_repo.remover_paciente(paciente)

    def listar_fila_atendimento(self) -> list[Paciente]:
        return self.fila_atendimento_repo.get_fila()

    def adicionar_paciente_fila_exames(self, paciente: Paciente) -> None:
        idx = self._get_insertion_index(self.fila_exames_repo.get_fila(), paciente)
        self.fila_exames_repo.adicionar_paciente_no_indice(paciente, idx)

    def remover_paciente_fila_exames(self, paciente: Paciente) -> bool:
        return self.fila_exames_repo.remover_paciente(paciente)

    def listar_fila_exames(self) -> list[Paciente]:
        return self.fila_exames_repo.get_fila()
