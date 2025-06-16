from typing import Dict, List
from ..model.paciente import Paciente

class PacienteRepository:
    _instance = None
    _pacientes: Dict[str, Paciente]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PacienteRepository, cls).__new__(cls)
            cls._instance._pacientes = {}
        return cls._instance

    def salvar_paciente(self, paciente: Paciente) -> None:
        self._pacientes[paciente.cpf] = paciente
        print(f"DEBUG: Paciente '{paciente.nome}' ({paciente.cpf}) salvo/atualizado no repositório.")

    def buscar_paciente_por_cpf(self, cpf: str) -> Paciente | None:
        return self._pacientes.get(cpf)

    def listar_todos_pacientes(self) -> List[Paciente]:
        return list(self._pacientes.values())

    def remover_paciente_por_cpf(self, cpf: str) -> bool:
        if cpf in self._pacientes:
            del self._pacientes[cpf]
            print(f"DEBUG: Paciente com CPF '{cpf}' removido do repositório.")
            return True
        print(f"DEBUG: Paciente com CPF '{cpf}' não encontrado para remoção.")
        return False

    def _clear_all_patients(self):
        self._pacientes = {}
        print("DEBUG: Repositório de pacientes limpo.")
