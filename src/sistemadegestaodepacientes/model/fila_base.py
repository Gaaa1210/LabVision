# src/sistemadegestaodepacientes/core/fila_base.py

from abc import ABC, abstractmethod
from sistemadegestaodepacientes.model.paciente import Paciente

class FilaBase(ABC):
    def __init__(self):
        self.fila = []

    def adicionar_paciente(self, paciente: Paciente):
        if paciente not in self.fila:
            self.fila.append(paciente)

    def remover_paciente(self, paciente: Paciente):
        if paciente in self.fila:
            self.fila.remove(paciente)

    def esta_vazia(self) -> bool:
        return len(self.fila) == 0

    def listar_pacientes(self) -> list:
        return self.fila

    @abstractmethod
    def proximo_paciente(self) -> Paciente:
        """
        Deve ser implementado nas subclasses para definir
        o critério de prioridade da fila (ex: idade, cor etc).
        """
        pass
