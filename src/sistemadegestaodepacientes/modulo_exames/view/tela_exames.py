from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
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
            self.console.print("[bold cyan]0.[/bold cyan] Voltar ao menu principal")

            opcao = Prompt.ask("\n[green]Escolha uma opção[/green]", choices=["1", "2", "0"])

            if opcao == "1":
                self.chamar_proximo_paciente()
            elif opcao == "2":
                self.registrar_resultado()
            elif opcao == "0":
                break

    def chamar_proximo_paciente(self):
        paciente = self.controller.chamar_proximo_paciente()
        if paciente:
            self.console.print(Panel(f"""
👤 Nome: [bold]{paciente.nome}[/bold]
🎂 Idade: {paciente.idade}
🏷️ CPF: {paciente.cpf}
🔴 Prioridade: {paciente.prioridade_cor}
📅 Chegada: {paciente.data_chegada}
""", title="Próximo Paciente", style="bold green"))
        else:
            self.console.print("[red]Nenhum paciente na fila de exames.[/red]")

    def registrar_resultado(self):
        cpf = Prompt.ask("Digite o CPF do paciente")
        tipo_amostra = Prompt.ask("Tipo de amostra")
        largura = float(Prompt.ask("Largura da amostra (cm)"))
        altura = float(Prompt.ask("Altura da amostra (cm)"))
        comprimento = float(Prompt.ask("Comprimento da amostra (cm)"))
        info_observadas = Prompt.ask("Informações observadas")
        exame_realizado = Confirm.ask("O exame foi realizado?")

        sucesso = self.controller.registrar_resultado_exame(
            cpf,
            tipo_amostra,
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
