from datetime import date, datetime 
from ..model.paciente import Paciente
from ..model.prioridade_cor import PrioridadeCor
from ..repository.paciente_repository import PacienteRepository
from ..util.cpf_validator import is_valid_cpf
from ..util.date_util import parse_date_string

class PacienteService:
    """
    Gerencia a lógica de negócio relacionada aos pacientes,
    incluindo verificação, cadastro e atualização.
    """
    def __init__(self):
        self.paciente_repo = PacienteRepository() 

    def verificar_ou_cadastrar_paciente(self, nome_str: str, data_nascimento_str: str,
                                       cpf: str, sexo: str, problemas_saude_str: str,
                                       alergias_medicamentos_str: str,
                                       cor_prioridade: PrioridadeCor) -> tuple[Paciente | None, str]:
        """
        Verifica se um paciente existe pelo CPF.
        Se não existir, tenta cadastrá-lo.
        Retorna o objeto Paciente e uma mensagem de status.
        """
        
        if not is_valid_cpf(cpf):
            return None, "Erro: CPF inválido."

        
        paciente_existente = self.paciente_repo.buscar_paciente_por_cpf(cpf)
        if paciente_existente:
            if cor_prioridade: 
                paciente_existente.cor_prioridade = cor_prioridade
                paciente_existente.data_chegada = datetime.now()
                self.paciente_repo.salvar_paciente(paciente_existente)
                return paciente_existente, "Paciente já cadastrado e atualizado (retriagem)."
            return paciente_existente, "Paciente já cadastrado."

        data_nascimento_obj = parse_date_string(data_nascimento_str)
        if data_nascimento_obj is None:
            return None, "Erro: Formato de data de nascimento inválido (esperado DD/MM/AAAA)."

        problemas_saude = [p.strip() for p in problemas_saude_str.split(',') if p.strip()] if problemas_saude_str else []
        alergias_medicamentos = [a.strip() for a in alergias_medicamentos_str.split(',') if a.strip()] if alergias_medicamentos_str else []

        novo_paciente = Paciente(
            nome=nome_str,
            data_nascimento=data_nascimento_obj,
            cpf=cpf,
            sexo=sexo,
            problemas_saude=problemas_saude,
            alergias_medicamentos=alergias_medicamentos,
            cor_prioridade=cor_prioridade
        )
        self.paciente_repo.salvar_paciente(novo_paciente)
        return novo_paciente, "Paciente cadastrado com sucesso."

    def buscar_paciente_por_cpf(self, cpf: str) -> Paciente | None:
        """Busca um paciente no repositório pelo CPF."""
        return self.paciente_repo.buscar_paciente_por_cpf(cpf)

    def listar_todos_pacientes(self) -> list[Paciente]:
        """Lista todos os pacientes cadastrados."""
        return self.paciente_repo.listar_todos_pacientes()