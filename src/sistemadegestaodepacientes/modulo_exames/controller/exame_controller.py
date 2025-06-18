from ...model.paciente import Paciente
from ...model.exame import Exame
from ...model.tipo_exame import TipoExame
from ...service.exame_service import ExameService
from ...service.fila_service import FilaService 

class ExameController:
    """
    Controla as interações do módulo de exames.
    """
    def __init__(self):
        self.exame_service = ExameService()
        self.fila_service = FilaService()

    def obter_proximo_paciente_fila_exames(self) -> Paciente | None:
        """
        Retorna o paciente com a maior prioridade na fila de exames.
        """
        fila = self.fila_service.listar_fila_exames()
        return fila[0] if fila else None 

    def registrar_realizacao_exame(self, paciente: Paciente, tipo_exame_opcao: str,
                                  largura: float = None, altura: float = None,
                                  comprimento: float = None, informacoes_observadas: str = None) -> tuple[Exame | None, str]:
        """
        Processa o registro da realização de um exame, incluindo resultados e observações.
        """
        try:
            tipo_exame_obj = TipoExame[tipo_exame_opcao.upper()]
        except KeyError:
            return None, "Erro: Tipo de exame inválido."

        return self.exame_service.registrar_realizacao_exame(
            paciente=paciente,
            tipo_exame=tipo_exame_obj,
            largura=largura,
            altura=altura,
            comprimento=comprimento,
            informacoes_observadas=informacoes_observadas
        )

    def listar_fila_exames(self) -> list[Paciente]:
        """Retorna a fila de exames para exibição."""
        return self.fila_service.listar_fila_exames()

    def gerar_laudo(self, exame: Exame) -> str:
        """Gera o laudo final de um exame."""
        return self.exame_service.gerar_laudo_final(exame)