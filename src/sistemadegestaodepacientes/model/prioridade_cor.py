from enum import Enum

class PrioridadeCor(Enum):
    VERMELHO = "Vermelho"
    AMARELAO = "Amarela"
    VERDE = "Verde"
    AZUL = "Azul"

    def __str__(self):
        return self.value