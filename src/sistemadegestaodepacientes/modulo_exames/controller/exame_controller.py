from sistemadegestaodepacientes.service.exame_service import ExameService
from sistemadegestaodepacientes.repository.paciente_repository import PacienteRepository
from sistemadegestaodepacientes.model.tipo_exame import TipoExame

class ExameController:
    def __init__(self):
        self.exame_service = ExameService()
        self.paciente_repository = PacienteRepository()

    def chamar_proximo_paciente(self):
        paciente = self.exame_service.get_proximo_paciente_exame()

        if paciente:
            print(f"👩‍⚕️ Próximo paciente para exame: {paciente.nome} - Prioridade: {paciente.cor_prioridade}")
            return paciente
        else:
            print("📭 Não há pacientes na fila de exames.")
            return None

    def registrar_resultado_exame(self, cpf, tipo_exame_str, largura, altura, comprimento, info_observadas, exame_realizado):
        paciente = self.paciente_repository.buscar_paciente_por_cpf(cpf)

        if not paciente:
            print(f"❌ Paciente com CPF {cpf} não encontrado.")
            return False

        tipo_exame = TipoExame(tipo=tipo_exame_str)

        sucesso = self.exame_service.registrar_exame(
            paciente=paciente,
            tipo_exame=tipo_exame,
            largura=largura,
            altura=altura,
            comprimento=comprimento,
            info_observadas=info_observadas,
            exame_realizado=exame_realizado
        )

        if sucesso:
            print("✅ Resultado do exame registrado com sucesso.")
            return True
        else:
            print("⚠️ Falha ao registrar o exame.")
            return False

    def listar_resultados_exames(self):
        return self.exame_service.get_todos_exames()
