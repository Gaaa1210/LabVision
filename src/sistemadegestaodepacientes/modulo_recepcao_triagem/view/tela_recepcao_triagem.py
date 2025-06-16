import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.theme import Theme

from ..controller.triagem_controller import TriagemController
from ...model.prioridade_cor import PrioridadeCor
from ...model.paciente import Paciente

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
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_header(title: str):
    clear_screen()
    console.print(Panel(Text(title, justify="center", style="header"), border_style="blue"))
    console.print("\n")

class TelaRecepcaoTriagem:
    def __init__(self):
        self.controller = TriagemController()

    def exibir_menu(self):
        while True:
            draw_header("MÓDULO: RECEPÇÃO E TRIAGEM")

            menu_table = Table(box=None, show_header=False)
            menu_table.add_column()
            menu_table.add_row(Text("1. Cadastrar/Triar Paciente", style="menu_option"))
            menu_table.add_row(Text("2. Visualizar Fila de Atendimento Médico", style="menu_option"))
            menu_table.add_row(Text("0. Sair", style="error"))
            console.print(menu_table)

            console.print("-" * 50, style="blue")

            opcao = Prompt.ask(Text("Escolha uma opção", style="prompt"), choices=['0', '1', '2'])

            if opcao == '1':
                self._cadastrar_triar_paciente()
            elif opcao == '2':
                self._visualizar_fila_atendimento()
            elif opcao == '0':
                console.print("\n[yellow]Saindo do Módulo de Recepção e Triagem. Até mais![/yellow]")
                break
            else:
                console.print("[red]Opção inválida. Tente novamente.[/red]")

            Confirm.ask(Text("\nPressione ENTER para continuar...", style="info"))

    def _cadastrar_triar_paciente(self):
        draw_header("CADASTRO/TRIAGEM DE PACIENTE")

        nome = Prompt.ask(Text("Nome do Paciente", style="input"))
        data_nascimento_str = Prompt.ask(Text("Data de Nascimento (DD/MM/AAAA)", style="input"))
        cpf = Prompt.ask(Text("CPF (apenas números)", style="input"))
        sexo = Prompt.ask(Text("Sexo (M/F/Outro)", style="input"))
        problemas_saude_str = Prompt.ask(Text("Problemas de Saúde (separados por vírgula, ex: 'asma, diabetes')", style="input"), default="")
        alergias_medicamentos_str = Prompt.ask(Text("Alergias a Medicamentos (separadas por vírgula)", style="input"), default="")

        console.print("\n[bold]--- Classificação de Prioridade (Pulseira) ---[/bold]")
        prioridade_options = []
        for i, cor_enum in enumerate(PrioridadeCor, 1):
            cor_style = cor_enum.name.lower()
            prioridade_options.append(str(i))
            console.print(f"[{cor_style}]{i}. {cor_enum.value}[/{cor_style}]")

        while True:
            try:
                opcao_cor_num = Prompt.ask(Text(f"Escolha a cor da pulseira (1-{len(PrioridadeCor)})", style="input"), choices=prioridade_options)
                opcao_cor_index = int(opcao_cor_num) - 1
                if 0 <= opcao_cor_index < len(PrioridadeCor):
                    cor_prioridade_selecionada = list(PrioridadeCor)[opcao_cor_index]
                    break
                else:
                    console.print("[red]Opção inválida. Digite um número entre 1 e {}.[/red]".format(len(PrioridadeCor)))
            except ValueError:
                console.print("[red]Entrada inválida. Digite um número.[/red]")

        paciente, mensagem = self.controller.verificar_ou_cadastrar_paciente_e_adicionar_a_fila(
            nome=nome,
            data_nascimento_str=data_nascimento_str,
            cpf=cpf,
            sexo=sexo,
            problemas_saude_str=problemas_saude_str,
            alergias_medicamentos_str=alergias_medicamentos_str,
            cor_prioridade_opcao=cor_prioridade_selecionada.name
        )

        if paciente:
            console.print(Panel(Text(f"SUCESSO: {mensagem}", style="bold green"), border_style="green"))
            console.print(Text("Dados do Paciente:", style="info"))
            console.print(f"[bold]{paciente}[/bold]")
        else:
            console.print(Panel(Text(f"FALHA: {mensagem}", style="bold red"), border_style="red"))

    def _visualizar_fila_atendimento(self):
        draw_header("FILA DE ATENDIMENTO MÉDICO")

        fila = self.controller.listar_fila_atendimento_medico()

        if not fila:
            console.print("[yellow]A fila de atendimento médico está vazia no momento.[/yellow]")
            return

        table = Table(
            title=Text("Pacientes em Espera", style="bold magenta"),
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
