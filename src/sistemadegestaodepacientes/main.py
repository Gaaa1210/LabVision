# src/sistemadegestaodepacientes/main.py
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.text import Text
import os

# IMPORTAÇÕES CORRIGIDAS PARA O CAMINHO RELATIVO
from .modulo_recepcao_triagem.view.tela_recepcao_triagem import TelaRecepcaoTriagem
from .modulo_consultorio_medico.view.tela_consultorio_medico import TelaConsultorioMedico

console = Console()

def clear_screen():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Função principal para iniciar a aplicação."""
    clear_screen()
    console.print(Text("Bem-vindo ao Sistema de Gestão de Pacientes!", style="bold green", justify="center"))
    console.print(Text("Otimizando o fluxo desde a chegada até o atendimento.", style="cyan", justify="center"))
    console.print("-" * 60, style="blue")
    
    tela_recepcao = TelaRecepcaoTriagem()
    tela_consultorio = TelaConsultorioMedico()

    while True:
        clear_screen()
        console.print(Text("MENU PRINCIPAL DO SISTEMA", style="bold blue", justify="center"))
        console.print("-" * 60, style="blue")
        console.print(Text("1. Módulo de Recepção e Triagem", style="cyan"))
        console.print(Text("2. Módulo de Consultório Médico", style="cyan"))
        console.print(Text("0. Sair do Sistema", style="error"))
        console.print("-" * 60, style="blue")

        opcao = Prompt.ask(Text("Escolha o módulo para acessar", style="bright_green"), choices=['0', '1', '2'])

        if opcao == '1':
            tela_recepcao.exibir_menu()
        elif opcao == '2':
            tela_consultorio.exibir_menu()
        elif opcao == '0':
            console.print("\n[yellow]Encerrando Sistema de Gestão de Pacientes. Até mais![/yellow]")
            break
        else:
            console.print("[red]Opção inválida. Tente novamente.[/red]")
        
        if opcao != '0': # Não pede para continuar se for sair
            Confirm.ask(Text("\nPressione ENTER para voltar ao Menu Principal...", style="info"))

if __name__ == "__main__":
    main()