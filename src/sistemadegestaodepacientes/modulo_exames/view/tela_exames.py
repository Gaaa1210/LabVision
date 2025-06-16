from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from sistemadegestaodepacientes.modulo_exames.controller.exame_controller import ExameController

class TelaExames:
    def __init__(self):
        self.controller = ExameController()
        self.console = Console()

    def exibir_menu(self):
        while True:
            self.console.print(Panel("📋 [bold blue]MENU DE EXAMES[/bold blue]", expand=False))
            self.console.print("[bold cyan]1.[/bold cyan] Chamar próximo paciente para exame")
            self.console.print("[bold cyan]2.[/bold cyan] Registrar resultado de exame")
            self.console.print("[bold cyan]3.[/bold cyan] Listar exames realizados")
            self.console.print("[bold cyan]0.[/bold cyan] Voltar ao menu principal")

            opcao = Prompt.ask("\n[green]Escolha uma opção[/green]", choices=["1", "2", "3", "0"])

            if opcao == "1":
                self.chamar_proximo_paciente()
            elif opcao == "2":
                self.registrar_resultado()
            elif opcao == "3":
                self.listar_exames_realizados()
            elif opcao == "0":
                break

    def chamar_proximo_paciente(self):
        paciente = self.controller.chamar_proximo_paciente()
        if paciente:
            cor_prioridade_str = (
                paciente.cor_prioridade.name if hasattr(paciente.cor_prioridade, 'name') 
                else str(paciente.cor_prioridade)
            )
            self.console.print(Panel(f"""
👤 Nome: [bold]{paciente.nome}[/bold]
🎂 Idade: {paciente.idade}
🏷️ CPF: {paciente.cpf}
🔴 Prioridade: {cor_prioridade_str}
📅 Chegada: {paciente.data_chegada}
""", title="Próximo Paciente", style="bold green"))
        else:
            self.console.print("[red]Nenhum paciente na fila de exames.[/red]")

    def registrar_resultado(self):
        cpf = Prompt.ask("Digite o CPF do paciente")
        tipo_exame = Prompt.ask("Tipo de exame")
        largura = float(Prompt.ask("Largura da amostra (cm)"))
        altura = float(Prompt.ask("Altura da amostra (cm)"))
        comprimento = float(Prompt.ask("Comprimento da amostra (cm)"))
        info_observadas = Prompt.ask("Informações observadas")
        exame_realizado = Confirm.ask("O exame foi realizado?")

        sucesso = self.controller.registrar_resultado_exame(
            cpf,
            tipo_exame,
            largura,
            altura,
            comprimento,
            info_observadas,
            exame_realizado
        )

        if sucesso:
            self.console.print("[bold green]✅ Exame registrado com sucesso![/bold green]")
        else:
            self.console.print("[bold red]❌ Falha ao registrar o exame.[/bold red]")

    def listar_exames_realizados(self):
        exames = self.controller.listar_resultados_exames()

        if not exames:
            self.console.print("[yellow]⚠️ Nenhum exame registrado até o momento.[/yellow]")
            return

        tabela = Table(title="📄 Exames Realizados")

        tabela.add_column("Paciente", style="cyan")
        tabela.add_column("Tipo de Exame", style="magenta")
        tabela.add_column("Largura (cm)", justify="right")
        tabela.add_column("Altura (cm)", justify="right")
        tabela.add_column("Comprimento (cm)", justify="right")
        tabela.add_column("Realizado", style="green")
        tabela.add_column("Observações", style="white")

        for exame in exames:
            tabela.add_row(
                exame.paciente.nome,
                exame.tipo_exame.tipo,  # Agora exame.tipo_exame é um objeto
                f"{exame.largura:.1f}",
                f"{exame.altura:.1f}",
                f"{exame.comprimento:.1f}",
                "Sim" if exame.exame_realizado else "Não",
                exame.informacoes_observadas
            )

        self.console.print(tabela)
