# src/sistemadegestaodepacientes/repository/paciente_repository.py
from typing import Dict, List

# IMPORTAÇÃO CORRIGIDA PARA O CAMINHO RELATIVO
# '.' refere-se ao pacote atual (repository).
# '..' refere-se ao pacote pai (sistemadegestaodepacientes).

# Para importar de model: do repository, suba um nível (..) e entre em 'model'
from ..model.paciente import Paciente

class PacienteRepository:
    """
    Gerencia o armazenamento e a recuperação de objetos Paciente.
    Utiliza um dicionário em memória para simular o banco de dados,
    usando o CPF como chave para acesso rápido.
    """
    _instance = None
    _pacientes: Dict[str, Paciente]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PacienteRepository, cls).__new__(cls)
            cls._instance._pacientes = {}
        return cls._instance

    def salvar_paciente(self, paciente: Paciente) -> None:
        """
        Salva ou atualiza um paciente no repositório.
        """
        self._pacientes[paciente.cpf] = paciente
        print(f"DEBUG: Paciente '{paciente.nome}' ({paciente.cpf}) salvo/atualizado no repositório.")

    def buscar_paciente_por_cpf(self, cpf: str) -> Paciente | None:
        """
        Busca um paciente pelo CPF.
        Retorna o objeto Paciente se encontrado, ou None caso contrário.
        """
        return self._pacientes.get(cpf)

    def listar_todos_pacientes(self) -> List[Paciente]:
        """
        Retorna uma lista com todos os pacientes armazenados.
        """
        return list(self._pacientes.values())

    def remover_paciente_por_cpf(self, cpf: str) -> bool:
        """
        Remove um paciente do repositório pelo CPF.
        Retorna True se o paciente foi removido, False se não foi encontrado.
        """
        if cpf in self._pacientes:
            del self._pacientes[cpf]
            print(f"DEBUG: Paciente com CPF '{cpf}' removido do repositório.")
            return True
        print(f"DEBUG: Paciente com CPF '{cpf}' não encontrado para remoção.")
        return False

    def _clear_all_patients(self):
        """Limpa todos os pacientes do repositório. Use com cautela!"""
        self._pacientes = {}
        print("DEBUG: Repositório de pacientes limpo.")