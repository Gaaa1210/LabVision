# src/sistemadegestaodepacientes/modulo_recepcao_triagem/controller/triagem_controller.py
from datetime import date # Este 'date' é do módulo datetime, não precisa de importação relativa

# IMPORTAÇÕES CORRIGIDAS PARA O CAMINHO RELATIVO
# '.' refere-se ao pacote atual (controller).
# '..' refere-se ao pacote pai (modulo_recepcao_triagem).
# '...' refere-se ao pacote avô (sistemadegestaodepacientes).

# Para importar de model: do controller, suba dois níveis (...) para 'sistemadegestaodepacientes' e entre em 'model'
from ...model.prioridade_cor import PrioridadeCor
from ...model.paciente import Paciente

# Para importar de service: do controller, suba dois níveis (...) para 'sistemadegestaodepacientes' e entre em 'service'
from ...service.paciente_service import PacienteService
from ...service.fila_service import FilaService

# Para importar de util: do controller, suba dois níveis (...) para 'sistemadegestaodepacientes' e entre em 'util'
from ...util.date_util import parse_date_string

class TriagemController:
    """
    Controla o fluxo de triagem e recepção de pacientes.
    Conecta a interface do usuário com os serviços de negócio.
    """
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
        cor_prioridade_opcao: str # Recebe a string da opção de cor
    ) -> tuple[Paciente | None, str]:
        """
        Lida com a verificação/cadastro de paciente e sua adição à fila de atendimento.
        Retorna o paciente (se sucesso) e uma mensagem de status.
        """
        # Converte a string da cor para o Enum PrioridadeCor
        try:
            cor_prioridade = PrioridadeCor[cor_prioridade_opcao.upper()] # Ex: "VERMELHA" -> PrioridadeCor.VERMELHA
        except KeyError:
            return None, "Erro: Cor de prioridade inválida. Use Vermelha, Amarela, Verde, Azul."

        # Chama o serviço para verificar/cadastrar o paciente
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
            # Se o paciente foi criado ou encontrado, adiciona ele à fila
            self.fila_service.adicionar_paciente_fila_atendimento(paciente)
            return paciente, f"{mensagem_paciente} Paciente adicionado à fila de atendimento."
        else:
            return None, mensagem_paciente # Retorna o erro do serviço de paciente

    def listar_fila_atendimento_medico(self) -> list[Paciente]:
        """Retorna a lista de pacientes na fila de atendimento médico."""
        return self.fila_service.listar_fila_atendimento()