class PacienteRepository:
    def __init__(self):
        self.pacientes = []  # Lista que armazena todos os pacientes

    def adicionar_paciente(self, paciente):
        self.pacientes.append(paciente)

    def buscar_por_id(self, paciente_id):
        for paciente in self.pacientes:
            if paciente.id == paciente_id:
                return paciente
        return None

    def atualizar(self, paciente_atualizado):
        for idx, paciente in enumerate(self.pacientes):
            if paciente.id == paciente_atualizado.id:
                self.pacientes[idx] = paciente_atualizado
                return True
        return False
