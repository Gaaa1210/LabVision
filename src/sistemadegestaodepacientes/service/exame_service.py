from sistemadegestaodepacientes.model.paciente import Paciente
from sistemadegestaodepacientes.model.exame import Exame
from sistemadegestaodepacientes.model.tipo_exame import TipoExame
from datetime import datetime

class ExameService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.fila_exames = []
        return cls._instance

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
        cor = getattr(paciente, 'prioridade_cor', None)
        cor = cor.lower() if cor else "branco"
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