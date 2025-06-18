from datetime import datetime
from ..model.paciente import Paciente
from ..model.exame import Exame
from ..model.tipo_exame import TipoExame 
from ..repository.exame_repository import ExameRepository 
from ..service.fila_service import FilaService 

class ExameService:
    """
    Gerencia a lógica de negócio para a realização de exames.
    """
    def __init__(self):
        self.exame_repo = ExameRepository()
        self.fila_service = FilaService()

    def registrar_realizacao_exame(self, paciente: Paciente, tipo_exame: TipoExame,
                                  largura: float = None, altura: float = None,
                                  comprimento: float = None, informacoes_observadas: str = None) -> tuple[Exame, str]:
        """
        Registra a realização de um exame e os seus resultados.
        Remove o paciente da fila de exames após a conclusão.
        """
        exame_registrado = Exame(
            paciente=paciente,
            tipo_exame=tipo_exame,
            largura=largura,
            altura=altura,
            comprimento=comprimento,
            informacoes_observadas=informacoes_observadas,
            exame_realizado=True 
        )

        self.exame_repo.registrar_exame(exame_registrado)

        self.fila_service.remover_paciente_fila_exames(paciente)
        print(f"DEBUG: Paciente '{paciente.nome}' removido da fila de exames.")

        return exame_registrado, "Exame registrado com sucesso e paciente removido da fila de exames."

    def listar_fila_exames(self) -> list[Paciente]:
        """
        Retorna a lista de pacientes na fila de exames,
        para que o técnico possa visualizar quem realizar exames.
        """
        return self.fila_service.listar_fila_exames()

    def gerar_laudo_final(self, exame: Exame) -> str:
        """
        Gera o texto do laudo final para um exame.
        """
        laudo = f"--- LAUDO FINAL DE EXAME ---\n"
        laudo += f"Paciente: {exame.paciente.nome} (CPF: {exame.paciente.cpf})\n"
        laudo += f"Tipo de Exame: {exame.tipo_exame.value}\n"
        laudo += f"Data de Realização: {exame.data_realizacao.strftime('%d/%m/%Y %H:%M:%S')}\n"
        laudo += f"Status: {'Concluído' if exame.exame_realizado else 'Pendente'}\n"

        if exame.largura is not None or exame.altura is not None or exame.comprimento is not None:
            laudo += f"Medidas:\n"
            if exame.largura is not None: laudo += f"  Largura: {exame.largura}\n"
            if exame.altura is not None: laudo += f"  Altura: {exame.altura}\n"
            if exame.comprimento is not None: laudo += f"  Comprimento: {exame.comprimento}\n"

        if exame.informacoes_observadas:
            laudo += f"Informações Observadas: {exame.informacoes_observadas}\n"

        laudo += "---------------------------\n"
        return laudo

    def buscar_exames_por_cpf(self, cpf: str) -> list[Exame]:
        """Busca exames de um paciente pelo CPF."""
        return self.exame_repo.buscar_exames_por_cpf(cpf)