from typing import Dict, List
from datetime import datetime 
from ..model.exame import Exame 
from ..model.paciente import Paciente

class ExameRepository:
    """
    Gerencia o armazenamento de objetos Exame em memória.
    Implementa o padrão Singleton.
    """
    _instance = None

    _exames_por_paciente: Dict[str, List[Exame]]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExameRepository, cls).__new__(cls)
            cls._instance._exames_por_paciente = {}
        return cls._instance

    def registrar_exame(self, exame: Exame) -> None:
        """
        Registra um exame. Se o paciente já tiver exames, adiciona à lista.
        """
        cpf = exame.paciente.cpf
        if cpf not in self._exames_por_paciente:
            self._exames_por_paciente[cpf] = []
        self._exames_por_paciente[cpf].append(exame)
        print(f"DEBUG: Exame de {exame.tipo_exame.value} para '{exame.paciente.nome}' registrado.")

    def buscar_exames_por_cpf(self, cpf: str) -> List[Exame]:
        """
        Retorna todos os exames registrados para um dado CPF.
        """
        return self._exames_por_paciente.get(cpf, [])

    def listar_todos_exames(self) -> List[Exame]:
        """
        Retorna uma lista de todos os exames registrados no sistema.
        """
        todos_exames = []
        for lista_exames in self._exames_por_paciente.values():
            todos_exames.extend(lista_exames)
        return todos_exames

    def atualizar_status_exame(self, exame_para_atualizar: Exame, exame_realizado: bool,
                               largura: float = None, altura: float = None, comprimento: float = None,
                               informacoes_observadas: str = None) -> bool:
        """
        Atualiza o status e os detalhes de um exame.
        Busca o exame pelo objeto e o atualiza.
        """
        cpf = exame_para_atualizar.paciente.cpf
        if cpf in self._exames_por_paciente:
            for i, exame in enumerate(self._exames_por_paciente[cpf]):

                if exame == exame_para_atualizar:
                    exame.exame_realizado = exame_realizado
                    exame.largura = largura
                    exame.altura = altura
                    exame.comprimento = comprimento
                    exame.informacoes_observadas = informacoes_observadas
                    if exame_realizado:
                        exame.data_realizacao = datetime.now() 
                    print(f"DEBUG: Status do exame de {exame.tipo_exame.value} para '{exame.paciente.nome}' atualizado.")
                    return True
        print(f"DEBUG: Exame para '{exame_para_atualizar.paciente.nome}' não encontrado para atualização.")
        return False

    def _clear_all_exames(self):
        """Limpa todos os exames do repositório (para debug/teste)."""
        self._exames_por_paciente = {}
        print("DEBUG: Repositório de exames limpo.")