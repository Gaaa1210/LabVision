class FilaService:

    def __init__(self):
        self.fila_atendimento = []
        self.fila_exames = []


    def get_proximo_paciente_atendimento(self):

        if not self.fila_atendimento:

            return None
        
        self.fila_atendimento.sort(key=lambda p: (
            self._cor_prioridade_valor(p.prioridade_cor),
            self._idade_prioridade_valor(p.idade),
            p.data_hora_chegada
        ))
        return self.fila_atendimento[0]
    
    def remover_paciente_da_fila_atendimento(self, paciente):
        if paciente in self.fila_atendimento:
            self.fila_atendimento.remove(paciente)

        
    def mover_para_fila_exames(self, paciente):
        if paciente in self.fila_atendimento:
            self.fila_atendimento.remove(paciente)

        self.fila_exames.append(paciente)


    def _cor_prioridade_valor(self, cor):
        cores = {'vermelho': 0, 'amarelo': 1, 'verde': 2, 'azul': 3}
        return cores.get(cor.lower(), 99)
    

    def _idade_prioridade_valor(self, idade):

        if idade < 5:

            return 0
        
        elif idade >= 65:

            return 1 
        
        else:
            return 2 
        