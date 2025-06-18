import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.theme import Theme
from ..controller.exame_controller import ExameController
from ...model.paciente import Paciente
from ...model.exame import Exame
from ...model.tipo_exame import TipoExame
from ...model.prioridade_cor import PrioridadeCor

console = Console()
custom_theme = Theme({
    "vermelha": "bold white on red",
    "amarela": "bold black on yellow",
    "verde": "bold white on green",
    "azul": "bold white on blue",
    "info": "cyan",
    "input": "green",
    "error": "bold red",
    "header": "bold blue",
    "menu_option": "cyan",
    "prompt": "bright_green",
    "table_header": "bold magenta",
})
console = Console(theme=custom_theme)

def clear_screen():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_header(title: str):
    """Desenha um cabeçalho formatado para as telas do terminal usando Rich."""
    clear_screen()
    console.print(Panel(Text(title, justify="center", style="header"), border_style="blue"))
    console.print("\n")


class TelaExames:
    """
    Gerencia a interface de usuário para o Módulo de Exames no terminal.
    """
    def __init__(self):
        self.controller = ExameController()

    def exibir_menu(self):
        """Exibe o menu principal do Módulo de Exames."""
        while True:
            draw_header("MÓDULO: GESTÃO DE EXAMES")

            menu_table = Table(box=None, show_header=False)
            menu_table.add_column()
            menu_table.add_row(Text("1. Realizar Próximo Exame", style="menu_option"))
            menu_table.add_row(Text("2. Visualizar Fila de Exames Pendentes", style="menu_option"))
            menu_table.add_row(Text("3. Visualizar Exames Concluídos (por CPF)", style="menu_option"))
            menu_table.add_row(Text("0. Sair", style="error"))
            console.print(menu_table)

            console.print("-" * 50, style="blue")

            opcao = Prompt.ask(Text("Escolha uma opção", style="prompt"), choices=['0', '1', '2', '3'])

            if opcao == '1':
                self._realizar_proximo_exame()
            elif opcao == '2':
                self._visualizar_fila_exames_pendentes()
            elif opcao == '3':
                self._visualizar_exames_concluidos_por_cpf()
            elif opcao == '0':
                console.print("\n[yellow]Saindo do Módulo de Exames. Até mais![/yellow]")
                break
            else:
                console.print("[red]Opção inválida. Tente novamente.[/red]")

            Confirm.ask(Text("\nPressione ENTER para continuar...", style="info"))

    def _realizar_proximo_exame(self):
        """Puxa o próximo paciente para exame e registra os resultados."""
        draw_header("REALIZAR PRÓXIMO EXAME")

        paciente_atual = self.controller.obter_proximo_paciente_fila_exames()

        if not paciente_atual:
            console.print("[yellow]Não há pacientes na fila de exames no momento.[/yellow]")
            return

        console.print(Panel(Text(f"Próximo Exame para: [bold]{paciente_atual.nome}[/bold] (CPF: {paciente_atual.cpf}) - Prioridade: [{paciente_atual.cor_prioridade.name.lower()}]{paciente_atual.cor_prioridade.value}[/{paciente_atual.cor_prioridade.name.lower()}]",
                                  justify="center"),
                            border_style="magenta"))
        console.print(f"\n[info]Detalhes do Paciente:[/info] [bold]{paciente_atual}[/bold]")

        console.print("\n[bold]--- Detalhes do Exame ---[/bold]")
        exame_options = []
        for i, tipo_exame_enum in enumerate(TipoExame, 1):
            exame_options.append(str(i))
            console.print(f"[{'cyan'}]{i}. {tipo_exame_enum.value}[/{'cyan'}]")

        tipo_exame_selecionado = None
        while True:
            try:
                opcao_exame_num = Prompt.ask(Text(f"Confirme o tipo de exame (1-{len(TipoExame)})", style="input"), choices=exame_options)
                opcao_exame_index = int(opcao_exame_num) - 1
                if 0 <= opcao_exame_index < len(TipoExame):
                    tipo_exame_selecionado = list(TipoExame)[opcao_exame_index]
                    break
                else:
                    console.print(f"[red]Opção inválida. Digite um número entre 1 e {len(TipoExame)}.[/red]")
            except ValueError:
                console.print("[red]Entrada inválida. Digite um número.[/red]")

        largura_str = Prompt.ask(Text("Largura da peça medida (opcional, digite N/A se não aplicável)", style="input"), default="N/A").replace(',', '.')
        largura = float(largura_str) if largura_str.upper() != 'N/A' else None

        altura_str = Prompt.ask(Text("Altura da peça medida (opcional, digite N/A se não aplicável)", style="input"), default="N/A").replace(',', '.')
        altura = float(altura_str) if altura_str.upper() != 'N/A' else None

        comprimento_str = Prompt.ask(Text("Comprimento da peça medida (opcional, digite N/A se não aplicável)", style="input"), default="N/A").replace(',', '.')
        comprimento = float(comprimento_str) if comprimento_str.upper() != 'N/A' else None

        informacoes_observadas = Prompt.ask(Text("Informações Observadas (campo livre)", style="input"), default="")

        exame_concluido, mensagem = self.controller.registrar_realizacao_exame(
            paciente=paciente_atual,
            tipo_exame_opcao=tipo_exame_selecionado.name,
            largura=largura,
            altura=altura,
            comprimento=comprimento,
            informacoes_observadas=informacoes_observadas
        )

        if exame_concluido:
            console.print(Panel(Text(f"SUCESSO: {mensagem}", style="bold green"), border_style="green"))

            laudo = self.controller.generar_laudo(exame_concluido) 
            console.print(Panel(laudo, title="LAUDO FINAL", border_style="yellow"))
        else:
            console.print(Panel(Text(f"FALHA: {mensagem}", style="bold red"), border_style="red"))

    def _visualizar_fila_exames_pendentes(self):
        """Exibe a fila de pacientes aguardando exames."""
        draw_header("FILA DE EXAMES PENDENTES")

        fila = self.controller.listar_fila_exames()

        if not fila:
            console.print("[yellow]A fila de exames pendentes está vazia no momento.[/yellow]")
            return

        table = Table(
            title=Text("Pacientes Aguardando Exames", style="bold magenta"),
            show_footer=False,
            box=None,
            header_style="table_header"
        )
        table.add_column("POS", justify="right", style="cyan", width=5)
        table.add_column("NOME", justify="left", style="cyan", width=25)
        table.add_column("CPF", justify="left", style="cyan", width=15)
        table.add_column("IDADE", justify="center", style="cyan", width=8)
        table.add_column("PRIORIDADE", justify="left", style="cyan", width=15)
        table.add_column("CHEGADA", justify="left", style="cyan", width=12)

        for i, paciente in enumerate(fila):
            cor_style = paciente.cor_prioridade.name.lower() if paciente.cor_prioridade else "info"
            table.add_row(
                str(i + 1),
                Text(paciente.nome, style=cor_style),
                Text(paciente.cpf, style=cor_style),
                Text(str(paciente.idade), style=cor_style),
                Text(str(paciente.cor_prioridade), style=cor_style),
                Text(paciente.data_chegada.strftime('%H:%M:%S'), style=cor_style)
            )

        console.print(table)
        console.print("\n" + "[bold blue]=" * 50 + "[/bold blue]")

    def _visualizar_exames_concluidos_por_cpf(self):
        """Permite visualizar exames concluídos de um paciente específico."""
        draw_header("EXAMES CONCLUÍDOS POR CPF")

        cpf = Prompt.ask(Text("Digite o CPF do paciente (apenas números) para buscar exames", style="input")).strip()

        exames_concluidos = self.controller.exame_service.buscar_exames_por_cpf(cpf)

        if not exames_concluidos:
            console.print(f"[yellow]Nenhum exame concluído encontrado para o CPF: {cpf}.[/yellow]")
            return

        console.print(f"\n[bold green]Exames Concluídos para CPF: {cpf}[/bold green]")
        for exame in exames_concluidos:
            console.print(Panel(self.controller.gerar_laudo(exame), title=f"Laudo - {exame.tipo_exame.value}", border_style="yellow"))
            console.print("-" * 50)