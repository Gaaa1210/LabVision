from sistemadegestaodepacientes.model.paciente import Paciente
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
            if idade <= 12 or idade >= 60:
                return 0  
            return 1  

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

        pacientes_ordenados = sorted(pacientes, key=chave_prioridade)
        return pacientes_ordenados

    def registrar_exame(self, paciente: Paciente, tipo_amostra, largura, altura, comprimento, info_observadas, exame_realizado):
        paciente.tipo_amostra = tipo_amostra
        paciente.largura = largura
        paciente.altura = altura
        paciente.comprimento = comprimento
        paciente.info_observadas = info_observadas
        paciente.exame_realizado = exame_realizado

        if exame_realizado:
            
            if paciente in self.fila_exames:
                self.fila_exames.remove(paciente)

        return True
