from enum import Enum

class PrioridadeCor(Enum):
    VERMELHA = "Vermelho"
    AMARELA = "Amarela"
    VERDE = "Verde"
    AZUL = "Azul"

    def __str__(self):
        return self.value