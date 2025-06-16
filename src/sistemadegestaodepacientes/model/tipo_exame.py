
from enum import Enum

class TipoExame(Enum):
    """
    Define os tipos de exames que podem ser solicitados.
    """
    ANALISE_CLINICA = "Análise Clínica" 

    def __str__(self):
        return self.value