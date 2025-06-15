# src/sistemadegestaodepacientes/model/tipo_exame.py
from enum import Enum

class TipoExame(Enum):
    """
    Define os tipos de exames que podem ser solicitados.
    """
    ANALISE_CLINICA = "Análise Clínica" # Nome genérico para "apenas uma opção de exame"

    # Se quiser mostrar a extensibilidade futura, pode adicionar mais:
    # RAIO_X = "Raio-X"
    # ULTRASSOM = "Ultrassom"
    # ENDOSCOPIA = "Endoscopia"

    def __str__(self):
        return self.value