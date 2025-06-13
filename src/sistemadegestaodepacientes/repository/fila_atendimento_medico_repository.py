class FilaAtendimentoMedicoRepository:
    def __init__(self):
        self.fila = []


    def adicionar_paciente(self, paciente):
        self.fila.append(paciente)


    def remover_paciente(self, paciente):
        if paciente in self.fila:
            self.fila.remove(paciente)

            return True
        
        return False
    

    def get_fila(self):
        return self.fila.copy()