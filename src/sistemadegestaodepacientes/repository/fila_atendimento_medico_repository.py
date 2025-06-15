# src/sistemadegestaodepacientes/repository/atendimento_medico_repository.py
from typing import Dict, List
# Importação relativa
from ..model.atendimento_medico import AtendimentoMedico
from ..model.paciente import Paciente # Para tipagem e busca por paciente, se precisar do tipo Paciente

class FilaAtendimentoMedicoRepository:
    """
    Gerencia o armazenamento de objetos AtendimentoMedico em memória.
    Implementa o padrão Singleton.
    """
    _instance = None
    _atendimentos: Dict[str, AtendimentoMedico] # <--- Dicionário para armazenar atendimentos

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AtendimentoMedicoRepository, cls).__new__(cls)
            # Dicionário onde a chave é o CPF do paciente e o valor é o objeto AtendimentoMedico
            cls._instance._atendimentos = {}
        return cls._instance

    def registrar_atendimento(self, atendimento: AtendimentoMedico) -> None:
        """
        Registra um novo atendimento médico para um paciente.
        Atualiza o registro se já houver um para o mesmo paciente (CPF).
        """
        self._atendimentos[atendimento.paciente.cpf] = atendimento
        print(f"DEBUG: Atendimento para '{atendimento.paciente.nome}' registrado/atualizado.")

    def buscar_atendimento_por_cpf(self, cpf: str) -> AtendimentoMedico | None:
        """
        Busca o último atendimento registrado para um paciente pelo CPF.
        """
        return self._atendimentos.get(cpf)

    def listar_todos_atendimentos(self) -> List[AtendimentoMedico]:
        """
        Retorna uma lista de todos os atendimentos registrados.
        """
        return list(self._atendimentos.values())

    def _clear_all_atendimentos(self):
        """Limpa todos os atendimentos do repositório (para debug/teste)."""
        self._atendimentos = {}
        print("DEBUG: Repositório de atendimentos médicos limpo.")