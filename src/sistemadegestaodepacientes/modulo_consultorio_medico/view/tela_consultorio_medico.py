from sistemadegestaodepacientes.modulo_consultorio_medico.controller.atendimento_controller import AtendimentoController

class TelaConsutorioMedico:

    def __init__(self):
        self.controller = AtendimentoController()

    def exibir_menu(self):
        while True:
            print("\n=== CONSULTÓRIO MÉDICO ===")
            print("1. Chamar próximo paciente")
            print("2. Registrar atendimento")
            print("0. Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                self.chamar_proximo_pacienete()

            elif opcao =='2':
                self.registar_atendimento()

            elif opcao == '0':
                break

            else:
                print('opção invalida')


    def chamar_proximo_paciente(self):
        paciente = self.controller.chamar_proximo_paciente
        if paciente:
            print(f"\n👨‍⚕️ Atendendo: {paciente.nome}")
            print(f"Idade: {paciente.idade}")
            print(f"Cor de prioridade: {paciente.prioridade_cor}")
            print(f"Data de chegada: {paciente.data_chegada}")
        else:
            print("Nenhum paciente na fila.")
        
    def registrar_atendimento(self):

        try:
            paciente_id = int(input('ID do paciente:'))
            observacoes = input('observaçõees clínicas: ')
            tem_exames  = input("Paciente precisa de exames? (s/n): ").strip().lower() == "s"

            tipo_exame = None 

            if tem_exames:

                tipo_exame = input("Tipo de exame: ")

            paciente_atendido = input("Finalizar atendimento do paciente? (s/n): ").strip().lower() == "s"

            self.controller.registrar_atendimento(
                paciente_id=paciente_id,
                observacoes=observacoes,
                tem_exames=tem_exames,
                tipo_exame=tipo_exame,
                paciente_atendido=paciente_atendido
            )

        except ValueError:
            print('ID inválido. Tente novamente.')



