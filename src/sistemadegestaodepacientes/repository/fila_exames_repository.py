# src/sistemadegestaodepacientes/repository/fila_exames_repository.py
from typing import List

# IMPORTAÇÃO CORRIGIDA PARA O CAMINHO RELATIVO
# '.' refere-se ao pacote atual (repository).
# '..' refere-se ao pacote pai (sistemadegestaodepacientes).

# Para importar de model: do repository, suba um nível (..) e entre em 'model'
from ..model.paciente import Paciente

class FilaExamesRepository:
    """
    Gerencia a lista de pacientes na fila de exames em memória.
    Implementa o padrão Singleton.
    """
    _instance = None
    _fila: List[Paciente] = [] # Esta linha já estava correta para anotação de classe

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FilaExamesRepository, cls).__new__(cls)
            cls._instance._fila = [] # Esta linha já estava correta para inicialização
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