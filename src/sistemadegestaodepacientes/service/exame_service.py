# src/sistemadegestaodepacientes/service/exame_service.py

from sistemadegestaodepacientes.model.paciente import Paciente
from sistemadegestaodepacientes.model.tipo_exame import TipoExame
from sistemadegestaodepacientes.model.resultado_exame import ResultadoExame
from datetime import datetime

class ExameService:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ExameService, cls).__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self):
        if not self._inicializado:
            self.fila_exames = []
            self.resultados_exames = []  # Armazena ResultadoExame
            self._inicializado = True

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
            cor = paciente.cor_prioridade.name.lower() if paciente.cor_prioridade else "branco"
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

    def registrar_exame(self, paciente: Paciente, tipo_exame: TipoExame,
                        largura: float, altura: float, comprimento: float,
                        info_observadas: str, exame_realizado: bool) -> bool:
        resultado = ResultadoExame(
            paciente=paciente,
            tipo_exame=tipo_exame,
            largura=largura,
            altura=altura,
            comprimento=comprimento,
            informacoes_observadas=info_observadas,
            exame_realizado=exame_realizado
        )

        self.resultados_exames.append(resultado)

        if exame_realizado and paciente in self.fila_exames:
            self.fila_exames.remove(paciente)

        return True

    def get_todos_exames(self) -> list[ResultadoExame]:
        return self.resultados_exames
