import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.theme import Theme



from ..controller.atendimento_controller import AtendimentoController
from ...model.paciente import Paciente 
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


class TelaConsultorioMedico:
    """
    Gerencia a interface de usuário para o Módulo de Consultório Médico no terminal.
    """
    def __init__(self):
        self.controller = AtendimentoController()

    def exibir_menu(self):
        """Exibe o menu principal do Consultório Médico."""
        while True:
            draw_header("MÓDULO: CONSULTÓRIO MÉDICO")

            menu_table = Table(box=None, show_header=False)
            menu_table.add_column()
            menu_table.add_row(Text("1. Chamar Próximo Paciente", style="menu_option"))
            menu_table.add_row(Text("2. Visualizar Fila de Atendimento", style="menu_option"))
            menu_table.add_row(Text("0. Sair", style="error"))
            console.print(menu_table)

            console.print("-" * 50, style="blue")

            opcao = Prompt.ask(Text("Escolha uma opção", style="prompt"), choices=['0', '1', '2'])

            if opcao == '1':
                self._chamar_proximo_paciente()
            elif opcao == '2':
                self._visualizar_fila_atendimento()
            elif opcao == '0':
                console.print("\n[yellow]Saindo do Módulo de Consultório Médico. Até mais![/yellow]")
                break
            else:
                console.print("[red]Opção inválida. Tente novamente.[/red]")

            Confirm.ask(Text("\nPressione ENTER para continuar...", style="info"))


    def _chamar_proximo_paciente(self):
        """Chama o próximo paciente da fila e inicia o atendimento."""
        draw_header("CHAMAR PRÓXIMO PACIENTE")

        paciente_atual = self.controller.obter_proximo_paciente_fila_atendimento()

        if not paciente_atual:
            console.print("[yellow]Não há pacientes na fila de atendimento no momento.[/yellow]")
            return

        console.print(Panel(Text(f"Próximo Paciente: [bold]{paciente_atual.nome}[/bold] (CPF: {paciente_atual.cpf}) - Prioridade: [{paciente_atual.cor_prioridade.name.lower()}]{paciente_atual.cor_prioridade.value}[/{paciente_atual.cor_prioridade.name.lower()}]",
                                  justify="center"),
                            border_style="magenta"))
        console.print(f"\n[info]Detalhes do Paciente:[/info] [bold]{paciente_atual}[/bold]")

        observacoes = Prompt.ask(Text("\nObservações do atendimento clínico", style="input"))
        
        necessita_exames_str = Prompt.ask(Text("O paciente necessita de exames? (s/n)", style="input"), choices=['s', 'n']).lower()
        necessita_exames = necessita_exames_str == 's'

        tipo_exame_selecionado = None
        if necessita_exames:
            console.print("\n[bold]--- Tipo de Exame ---[/bold]")
            exame_options = []
            for i, tipo_exame_enum in enumerate(TipoExame, 1):
                exame_options.append(str(i))
                console.print(f"[{'cyan'}]{i}. {tipo_exame_enum.value}[/{'cyan'}]") # Cor fixa para exames
            
            while True:
                try:
                    opcao_exame_num = Prompt.ask(Text(f"Escolha o tipo de exame (1-{len(TipoExame)})", style="input"), choices=exame_options)
                    opcao_exame_index = int(opcao_exame_num) - 1
                    if 0 <= opcao_exame_index < len(TipoExame):
                        tipo_exame_selecionado = list(TipoExame)[opcao_exame_index]
                        break
                    else:
                        console.print(f"[red]Opção inválida. Digite um número entre 1 e {len(TipoExame)}.[/red]")
                except ValueError:
                    console.print("[red]Entrada inválida. Digite um número.[/red]")

        
        atendimento_registrado, mensagem = self.controller.processar_atendimento_medico(
            paciente=paciente_atual,
            observacoes=observacoes,
            necessita_exames=necessita_exames,
            tipo_exame_opcao=tipo_exame_selecionado.name if tipo_exame_selecionado else None
        )

        if atendimento_registrado:
            console.print(Panel(Text(f"SUCESSO: {mensagem}", style="bold green"), border_style="green"))
        else:
            console.print(Panel(Text(f"FALHA: {mensagem}", style="bold red"), border_style="red"))

    def _visualizar_fila_atendimento(self):
        """Exibe a fila de atendimento médico."""
        draw_header("FILA DE ATENDIMENTO MÉDICO (MÉDICO)")

        fila = self.controller.listar_fila_atendimento()

        if not fila:
            console.print("[yellow]A fila de atendimento médico está vazia no momento.[/yellow]")
            return

        table = Table(
            title=Text("Pacientes Aguardando Atendimento", style="bold magenta"),
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