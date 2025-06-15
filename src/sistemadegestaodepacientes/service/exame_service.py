from sistemadegestaodepacientes.model.paciente import Paciente
from sistemadegestaodepacientes.model.exame import Exame
from sistemadegestaodepacientes.model.tipo_exame import TipoExame
from datetime import datetime

class ExameService:
    def __init__(self):
        self.fila_exames = []

    def adicionar_paciente_exame(self, paciente: Paciente):
        if paciente not in self.fila_exames:
            self.fila_exames.append(paciente)

    def get_proximo_paciente_exame(self):
        if not self.fila_exames:
            return None
        
        pacientes_ordenados = self.ordenar_por_prioridade(self.fila_exames)
        return pacientes_ordenados[0] if pacientes_ordenados else None

    def ordenar_por_prioridade(self, pacientes):
        prioridade_cores = {
            "vermelho": 1,
            "amarelo": 2,
            "verde": 3,
            "azul": 4,
            "branco": 5
        }

        def idade_preferencial(idade):
            return 0 if (idade <= 12 or idade >= 60) else 1

        def chave_prioridade(paciente):
            cor = paciente.prioridade_cor.lower() if paciente.prioridade_cor else "branco"
            prioridade_cor = prioridade_cores.get(cor, 5)
            prioridade_idade = idade_preferencial(paciente.idade)
            data_chegada = paciente.data_chegada
            if isinstance(data_chegada, str):
                try:
                    data_chegada = datetime.fromisoformat(data_chegada)
                except Exception:
                    data_chegada = datetime.min
            return (prioridade_cor, prioridade_idade, data_chegada)

        return sorted(pacientes, key=chave_prioridade)

    def registrar_exame(self, paciente: Paciente, tipo_exame: TipoExame, largura: float, altura: float,
                        comprimento: float, info_observadas: str, exame_realizado: bool):
        if not hasattr(paciente, "exames"):
            paciente.exames = []

        exame = Exame(
            paciente=paciente,
            tipo_exame=tipo_exame,
            largura=largura,
            altura=altura,
            comprimento=comprimento,
            informacoes_observadas=info_observadas,
            exame_realizado=exame_realizado
        )

        paciente.exames.append(exame)

        if exame_realizado and paciente in self.fila_exames:
            self.fila_exames.remove(paciente)

        return True
