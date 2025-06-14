from sistemadegestaodepacientes.repository.fila_atendimento_medico_repository import FilaAtendimentoMedicoRepository

from sistemadegestaodepacientes.model.prioridade_cor import PriridadeCor

class FilaService:
    def __init__(self):
        self.fila_repository = FilaAtendimentoMedicoRepository()

    def get_proximo_paciente_atendimento(self):
        fila = self.fila_repository.get_fila()

        if not fila:
            return None
        
        def prioridade(paciente):
            cor_valor  = PriridadeCor.get_valor_prioridade(paciente.cor_prioridade)

            idade_valor = 0 if paciente >= 60 or paciente.idade <= 5 else 1

            return(cor_valor, idade_valor,paciente.data_chegada)
    
        fila_ordenada = sorted(fila, key=prioridade)

        return fila_ordenada[0]
    
    def remover_paciente_da_fila_atendimento(self, paciente):

        sucesso = self.fila_repository.remover_paciente(paciente)

        if not sucesso:

            raise ValueError("paciete não está na fila de atendimento")

        return sucesso 
    
    def mover_para_fila_exames(self, paciente):
        removido = self.remover_paciente_da_fila_atendimento(paciente)

        if removido:
            self.fila_exames_repository.adicionar_paciente(paciente)
            return True
    
        return False

