
from dataclasses import dataclass
from sistemadegestaodepacientes.model.paciente import Paciente
from sistemadegestaodepacientes.model.tipo_exame import TipoExame

@dataclass
class ResultadoExame:
    paciente: Paciente
    tipo_exame: TipoExame
    largura: float
    altura: float
    comprimento: float
    informacoes_observadas: str
    exame_realizado: bool

    def __str__(self):
        status = "Realizado" if self.exame_realizado else "Pendente"
        return (
            f"Paciente: {self.paciente.nome} | Exame: {self.tipo_exame.nome} | "
            f"Dimensões: {self.largura}x{self.altura}x{self.comprimento} | "
            f"Observações: {self.informacoes_observadas} | Status: {status}"
        )
