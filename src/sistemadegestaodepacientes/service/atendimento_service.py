# src/sistemadegestaodepacientes/service/atendimento_service.py
from datetime import datetime

# IMPORTAÇÕES CORRIGIDAS PARA O CAMINHO RELATIVO
# '.' refere-se ao pacote atual (service).
# '..' refere-se ao pacote pai (sistemadegestaodepacientes).

# Para importar de model: do service, suba um nível (..) e entre em 'model'
from ..model.paciente import Paciente
from ..model.atendimento_medico import AtendimentoMedico
from ..model.tipo_exame import TipoExame
# Para importar de repository: do service, suba um nível (..) e entre em 'repository'
from ..repository.atendimento_medico_repository import AtendimentoMedicoRepository
# Para importar de service (outro módulo dentro do mesmo pacote 'service'):
# Não precisa subir de nível, basta usar '.' para o mesmo pacote.
# No entanto, se FilaService estiver em um arquivo diferente dentro de 'service',
# a importação é mais simples ainda se estiver no mesmo subdiretório:
# Ex: from .fila_service import FilaService (se fila_service.py estiver na mesma pasta 'service')
# No nosso caso, ambos estão na pasta 'service', então é 'from .fila_service'.
from .fila_service import FilaService # CORRIGIDO: Era '..service.fila_service'

class AtendimentoService:
    """
    Gerencia a lógica de negócio do atendimento médico.
    Responsável por registrar atendimentos e interagir com as filas.
    """
    def __init__(self):
        self.atendimento_repo = AtendimentoMedicoRepository()
        self.fila_service = FilaService() # Instância do serviço de filas

    def registrar_atendimento_medico(self, paciente: Paciente, observacoes: str,
                                    necessita_exames: bool, tipo_exame_solicitado: TipoExame = None) -> tuple[AtendimentoMedico, str]:
        """
        Registra um atendimento médico para um paciente.
        Move o paciente para a fila de exames se necessário.
        """
        if necessita_exames and not tipo_exame_solicitado:
            return None, "Erro: Tipo de exame deve ser especificado se exames são necessários."

        # Cria o objeto AtendimentoMedico
        novo_atendimento = AtendimentoMedico(
            paciente=paciente,
            observacoes=observacoes,
            necessita_exames=necessita_exames,
            tipo_exame_solicitado=tipo_exame_solicitado
        )

        # 1. Registra o atendimento no repositório de atendimentos
        self.atendimento_repo.registrar_atendimento(novo_atendimento)

        # 2. Atualiza o status do paciente nas filas
        # O paciente é SEMPRE removido da fila de atendimento médico após ser atendido no consultório.
        self.fila_service.remover_paciente_fila_atendimento(paciente)
        print(f"DEBUG: Paciente '{paciente.nome}' removido da fila de atendimento médico.")

        # Se necessita exames, adiciona na fila de exames
        if necessita_exames:
            # O projeto não especifica se um novo objeto Exame é criado aqui.
            # Para fins de fila, basta o Paciente. O Exame em si será criado no Módulo 3.
            # No entanto, o paciente pode precisar "saber" que tipo de exame foi solicitado.
            # Por simplicidade, passamos o paciente para a fila de exames.
            self.fila_service.adicionar_paciente_fila_exames(paciente)
            return novo_atendimento, "Atendimento registrado. Paciente movido para a fila de exames."
        else:
            return novo_atendimento, "Atendimento registrado. Paciente finalizou o fluxo médico."

    def listar_fila_atendimento_para_medico(self) -> list[Paciente]:
        """
        Retorna a lista de pacientes na fila de atendimento médico,
        para que o médico possa visualizar quem atender.
        """
        return self.fila_service.listar_fila_atendimento()

    def buscar_atendimento_por_cpf(self, cpf: str) -> AtendimentoMedico | None:
        """Busca o último atendimento de um paciente pelo CPF."""
        return self.atendimento_repo.buscar_atendimento_por_cpf(cpf)