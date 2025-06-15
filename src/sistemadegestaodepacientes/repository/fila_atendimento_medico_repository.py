# src/sistemadegestaodepacientes/repository/fila_atendimento_medico_repository.py
from typing import List
from ..model.paciente import Paciente # Importação relativa corrigida

class FilaAtendimentoMedicoRepository:
    """
    Gerencia a lista de pacientes na fila de atendimento médico em memória.
    Implementa o padrão Singleton.
    """
    _instance = None
    _fila: List[Paciente] # Declaração de tipo para o atributo de instância

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FilaAtendimentoMedicoRepository, cls).__new__(cls)
            cls._instance._fila = [] # Inicializa a lista _fila para a instância
        return cls._instance

    def adicionar_paciente_no_indice(self, paciente: Paciente, index: int) -> None:
        """Adiciona um paciente na fila em um índice específico."""
        self._fila.insert(index, paciente)

    def remover_paciente(self, paciente: Paciente) -> bool:
        """Remove um paciente da fila. Retorna True se removido, False caso contrário."""
        try:
            self._fila.remove(paciente)
            return True
        except ValueError:
            return False

    def get_fila(self) -> List[Paciente]:
        """Retorna a fila atual."""
        return self._fila

    def _clear_fila(self):
        """Limpa a fila. (Apenas para debug/teste)"""
        self._fila = []