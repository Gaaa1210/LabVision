from typing import Dict, List
from ..model.atendimento_medico import AtendimentoMedico
from ..model.paciente import Paciente

class AtendimentoMedicoRepository:
    _instance = None
    _atendimentos: Dict[str, AtendimentoMedico]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AtendimentoMedicoRepository, cls).__new__(cls)
            cls._instance._atendimentos = {}
        return cls._instance

    def registrar_atendimento(self, atendimento: AtendimentoMedico) -> None:
        self._atendimentos[atendimento.paciente.cpf] = atendimento
        print(f"DEBUG: Atendimento para '{atendimento.paciente.nome}' registrado/atualizado.")

    def buscar_atendimento_por_cpf(self, cpf: str) -> AtendimentoMedico | None:
        return self._atendimentos.get(cpf)

    def listar_todos_atendimentos(self) -> List[AtendimentoMedico]:
        return list(self._atendimentos.values())

    def _clear_all_atendimentos(self):
        self._atendimentos = {}
        print("DEBUG: Repositório de atendimentos médicos limpo.")
