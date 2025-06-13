from sistemadegestaodepacientes.service.fila_service import FilaService
from sistemadegestaodepacientes.repository.paciente_repository import PacienteRepository


class AtendiemntoController:

    def __init__(self):
        self.fila_service = FilaService()
        self.paciente_repository = PacienteRepository()

    def chamar_proximo_paciente(self):
        paciente = self.fila_service.get_proximo_paciente_atendimento()
        if paciente:
            print(f"Próximo paciente: {paciente.nome} - Prioridade: {paciente.prioridade_cor}")
            return paciente

        else:
            print("Não há pacientes na fila.")
            return None
        

    def registar_atendimento(self, paciente_id, observacoes, tem_exames, tipo_exame=None, paciente_atendido=False):
           
        paciente = self.paciente_repository.buscar_por_id(paciente_id)

        if not  paciente:
            print('paciente não encontrado')
            return
           
        paciente.observacoes = observacoes
        paciente.tem_exames = tem_exames
        paciente.tipo_exame = tipo_exame
            



        if paciente_atendido:
            self.fila_service.remover_paciente_fila_atendimento(paciente)
            print(f"Paciente {paciente.nome} marcado como atendido e removido da fila.")


        elif tem_exames:
            self.fila_service.mover_para_fila_exames(paciente)
            print(f"Paciente {paciente.nome} precisa fazer exames, movido para fila de exames.")

        else:
             print("Atualização do paciente realizada, paciente permanece na fila.")


        self.paciente_repository.atualizar(paciente)