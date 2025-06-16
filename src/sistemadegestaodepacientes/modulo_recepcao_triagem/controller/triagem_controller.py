from datetime import date

from ...model.prioridade_cor import PrioridadeCor
from ...model.paciente import Paciente
from ...service.paciente_service import PacienteService
from ...service.fila_service import FilaService
from ...util.date_util import parse_date_string

class TriagemController:
    def __init__(self):
        self.paciente_service = PacienteService()
        self.fila_service = FilaService()

    def verificar_ou_cadastrar_paciente_e_adicionar_a_fila(
        self,
        nome: str,
        data_nascimento_str: str,
        cpf: str,
        sexo: str,
        problemas_saude_str: str,
        alergias_medicamentos_str: str,
        cor_prioridade_opcao: str 
    ) -> tuple[Paciente | None, str]:
        try:
            cor_prioridade = PrioridadeCor[cor_prioridade_opcao.upper()]
        except KeyError:
            return None, "Erro: Cor de prioridade inválida. Use Vermelha, Amarela, Verde, Azul."

        paciente, mensagem_paciente = self.paciente_service.verificar_ou_cadastrar_paciente(
            nome_str=nome,
            data_nascimento_str=data_nascimento_str,
            cpf=cpf,
            sexo=sexo,
            problemas_saude_str=problemas_saude_str,
            alergias_medicamentos_str=alergias_medicamentos_str,
            cor_prioridade=cor_prioridade
        )

        if paciente:
            self.fila_service.adicionar_paciente_fila_atendimento(paciente)
            return paciente, f"{mensagem_paciente} Paciente adicionado à fila de atendimento."
        else:
            return None, mensagem_paciente

    def listar_fila_atendimento_medico(self) -> list[Paciente]:
        return self.fila_service.listar_fila_atendimento()
