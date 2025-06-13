class PacienteRepository:

    def __init__(self):
        self.pacientes = []


    def buscar_por_id( self, paciente_id):
        for paciente in self.pacientes:

            if paciente.id == paciente:
                return paciente

        return None
    
    def atualizar(self, paciente_atualizado):

        for i, paciente in enumerate(self.pacientes):

            if paciente.id == paciente_atualizado.id:

                self.pacientes[i] = paciente_atualizado
                return
            
            