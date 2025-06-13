class FilaExamesRepository:

    def __init__(self):
        self.fila = []

    def adicionar_paciente(self, paciente):

        self.fila.append(paciente)


    def get_fila(self):
        return self.fila.copy()