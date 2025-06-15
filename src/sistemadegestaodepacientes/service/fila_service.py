# src/sistemadegestaodepacientes/service/fila_service.py
import bisect # Módulo para busca binária e inserção em listas ordenadas (opcional se vc fez na mão)
from datetime import datetime # Importação padrão de módulos embutidos

# IMPORTAÇÕES CORRIGIDAS PARA O CAMINHO RELATIVO
# '.' refere-se ao pacote atual (service).
# '..' refere-se ao pacote pai (sistemadegestaodepacientes).

# Para importar de model: do service, suba um nível (..) e entre em 'model'
from ..model.paciente import Paciente
from ..model.prioridade_cor import PrioridadeCor
# Para importar de repository: do service, suba um nível (..) e entre em 'repository'
from ..repository.fila_atendimento_medico_repository import FilaAtendimentoMedicoRepository
from ..repository.fila_exames_repository import FilaExamesRepository

class FilaService:
    """
    Gerencia as filas de prioridade para atendimento médico e realização de exames.
    Aplica a lógica de prioridade (cor, idade, data/hora) usando busca binária
    para manter as filas sempre ordenadas.
    """
    def __init__(self):
        self.fila_atendimento_repo = FilaAtendimentoMedicoRepository()
        self.fila_exames_repo = FilaExamesRepository()

    # ------------------------------------------------ Lógica de Prioridade Compartilhada ------------------------------------------------------
    def _calcular_prioridade(self, paciente: Paciente) -> tuple:
        """
        Calcula um "peso" de prioridade para o paciente.
        Quanto menor o número, maior a prioridade.
        A tupla permite ordenar por múltiplos critérios.
        """

        # Para ordenação (menor valor = maior prioridade):
        # 0: Vermelha, 1: Amarela, 2: Verde, 3: Azul
        # Corrigindo o erro de enum: deve ser PrioridadeCor.VERMELHA, não PrioridadeCor.VERMELHO
        if paciente.cor_prioridade == PrioridadeCor.VERMELHA:
            peso_cor = 0
        elif paciente.cor_prioridade == PrioridadeCor.AMARELA:
            peso_cor = 1
        elif paciente.cor_prioridade == PrioridadeCor.VERDE:
            peso_cor = 2
        else: # Azul ou não definida
            peso_cor = 3

        # Prioridade por Idade: Idosos (>60) e Crianças (<6) têm maior prioridade
        # Um peso menor significa maior prioridade.
        peso_idade = 0 # Padrão para não-preferencial

        # Ajuste a faixa etária preferencial conforme a definição do projeto
        # Ex: idosos (>60) e crianças pequenas (<6)
        if paciente.idade >= 60:
            peso_idade = -2 # Maior prioridade que crianças, ou ajuste conforme necessidade
        elif paciente.idade <= 6:
            peso_idade = -1

        # Critério de Desempate: Data/Hora de Chegada (quanto mais antigo, maior prioridade)
        # datetime.timestamp() retorna um float, quanto menor, mais antigo.
        # Usamos o negativo para que a ordem crescente do timestamp (mais antigo = menor valor)
        # reflita a prioridade (menor valor = maior prioridade)
        peso_chegada = paciente.data_chegada.timestamp()

        return (peso_cor, peso_idade, peso_chegada)
#busca binária

    def _get_insertion_index(self, fila: list[Paciente], novo_paciente: Paciente) -> int:
        """
        Usa lógica de busca binária para encontrar o índice de inserção
        de um novo paciente em uma fila já ordenada por prioridade.
        """
        novo_peso = self._calcular_prioridade(novo_paciente)
        low = 0 # Renomeado para low para consistência
        high = len(fila) # Renomeado para high para consistência

        while low < high:
            mid = (low + high) // 2
            mid_paciente = fila[mid]
            mid_peso = self._calcular_prioridade(mid_paciente)

            # Se o novo paciente tem MAIOR prioridade (peso_novo < peso_mid)
            if novo_peso < mid_peso:
                high = mid
            # Se o novo paciente tem MENOR ou IGUAL prioridade (peso_novo >= peso_mid)
            else:
                low = mid + 1
        return low


    # --------------------------------------------- Métodos para Fila de Atendimento Médico --------------------------------------------------
    def adicionar_paciente_fila_atendimento(self, paciente: Paciente) -> None:
        """Adiciona um paciente à fila de atendimento médico, mantendo a ordem por prioridade."""
        idx = self._get_insertion_index(self.fila_atendimento_repo.get_fila(), paciente)
        self.fila_atendimento_repo.adicionar_paciente_no_indice(paciente, idx)
        print(f"DEBUG: Paciente '{paciente.nome}' adicionado à fila de atendimento na posição {idx}.")


    def remover_paciente_fila_atendimento(self, paciente: Paciente) -> bool:
        """Remove um paciente da fila de atendimento médico."""
        removido = self.fila_atendimento_repo.remover_paciente(paciente)
        if removido:
            print(f"DEBUG: Paciente '{paciente.nome}' removido da fila de atendimento.")
        else:
            print(f"DEBUG: Paciente '{paciente.nome}' não encontrado na fila de atendimento para remoção.")
        return removido

    def listar_fila_atendimento(self) -> list[Paciente]:
        """Retorna a fila de atendimento médico, já ordenada por prioridade."""
        return self.fila_atendimento_repo.get_fila()

    # ----------------------------------------------------- Métodos para Fila de Realização de Exames -------------------------------------------------------------
    def adicionar_paciente_fila_exames(self, paciente: Paciente) -> None:
        """Adiciona um paciente à fila de exames, mantendo a ordem por prioridade."""
        idx = self._get_insertion_index(self.fila_exames_repo.get_fila(), paciente)
        self.fila_exames_repo.adicionar_paciente_no_indice(paciente, idx)
        print(f"DEBUG: Paciente '{paciente.nome}' adicionado à fila de exames na posição {idx}.")


    def remover_paciente_fila_exames(self, paciente: Paciente) -> bool:
        """Remove um paciente da fila de exames."""
        removido = self.fila_exames_repo.remover_paciente(paciente)
        if removido:
            print(f"DEBUG: Paciente '{paciente.nome}' removido da fila de exames.")
        else:
            print(f"DEBUG: Paciente '{paciente.nome}' não encontrado na fila de exames para remoção.")
        return removido

    def listar_fila_exames(self) -> list[Paciente]:
        """Retorna a fila de exames, já ordenada por prioridade."""
        return self.fila_exames_repo.get_fila()