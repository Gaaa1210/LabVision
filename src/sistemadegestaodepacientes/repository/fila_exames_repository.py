from typing import List
from ..model.paciente import Paciente

class FilaExamesRepository:
    _instance = None
    _fila: List[Paciente] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FilaExamesRepository, cls).__new__(cls)
            cls._instance._fila = []
        return cls._instance

    def adicionar_paciente_no_indice(self, paciente: Paciente, index: int) -> None:
        self._fila.insert(index, paciente)

    def remover_paciente(self, paciente: Paciente) -> bool:
        try:
            self._fila.remove(paciente)
            return True
        except ValueError:
            return False

    def get_fila(self) -> List[Paciente]:
        return self._fila

    def _clear_fila(self):
        self._fila = []
