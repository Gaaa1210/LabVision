
# Sistema de Gestão de Pacientes (Triage e Atendimento)

## Visão Geral do Projeto

Este projeto em Python visa otimizar o fluxo de pacientes em uma clínica ou laboratório, desde a chegada e triagem inicial até o atendimento médico e a realização de exames. O sistema gerencia informações de pacientes, prioridades de atendimento e o status de cada etapa do processo, tudo através de uma interface de terminal robusta e amigável, desenvolvida com a biblioteca rich.

O sistema é dividido em módulos lógicos, facilitando o desenvolvimento em equipe e a manutenção.

## Funcionalidades Principais

O sistema oferece as seguintes funcionalidades, organizadas por módulo:

### Módulo 1: Recepção e Triagem (Cadastro e Fila de Atendimento Médico)
* *Identificação do Paciente:* Verificação de cadastro por CPF.
* *Cadastro de Cliente:* Coleta e armazenamento de informações essenciais do paciente (Nome, Idade, CPF, Data de Nascimento, Sexo, Problemas de Saúde, Alergias a Medicamentos).
* *Classificação de Prioridade:* Permite classificar a cor da pulseira do paciente (Vermelha, Amarela, Verde, Azul).
* *Lógica de Prioridade e Fila de Atendimento:* Gera e gerencia uma fila de espera para atendimento médico com base em:
    * *Prioridade por Cor:* Vermelha tem prioridade máxima.
    * *Prioridade por Idade:* Níveis de idade preferenciais (ex: idosos, crianças pequenas) têm prioridade dentro de suas classificações de cor.
    * *Critério de Desempate:* Para mesma cor e nível de idade, a prioridade é pela data e hora de chegada/cadastro (o mais antigo primeiro).
    * *Implementação:* Utiliza *dicionários* para acesso rápido a pacientes por CPF e *busca binária* para inserção eficiente e manutenção da ordem nas filas de prioridade.

### Módulo 2: Consultório Médico (Atendimento e Requisição de Exames)
* *Lista de Prioridades:* Exibe ao médico a fila de pacientes organizada por prioridade.
* *Atendimento Médico:* Permite ao médico registrar observações do exame clínico.
* *Requisição de Exames:* O médico pode indicar a necessidade de exames e especificar o tipo (atualmente uma opção genérica, mas expansível).
* *Gestão de Status do Paciente:* Remove o paciente da fila de atendimento médico quando "Atendido" ou o move para a "Fila de Realização de Exames" se exames forem solicitados.

### Módulo 3: Exames (Gestão e Realização) - A ser implementado
* *Puxar Pendências:* O sistema puxará pacientes encaminhados para exames.
* *Lista de Prioridades para Exames:* Exibirá uma fila de exames seguindo a mesma lógica de prioridade.
* *Registro de Exames:* Formulário para registrar resultados (Tipo de Amostra, Largura, Altura, Comprimento da peça medida, Informações Observadas).
* *Geração de Laudo:* Gerará um laudo final com os dados registrados.
* *Gestão de Status:* O paciente será removido da fila de exames após a confirmação de "Exame realizado?".

## Estrutura do Projeto

O projeto segue uma arquitetura modular baseada em camadas, facilitando a organização e o desenvolvimento em equipe.


## Como Configurar e Rodar o Projeto

### Pré-requisitos

* Python 3.8+ instalado.
* pip (gerenciador de pacotes do Python).

### Instalação das Dependências

1.  Navegue até a raiz do projeto (a pasta que contém src/, docs/, requirements.txt, etc.).
2.  Instale as bibliotecas necessárias usando pip:
    bash
    pip install -r requirements.txt
    
    (Certifique-se de que requirements.txt contém rich e qualquer outra biblioteca que você venha a usar.)

    Conteúdo sugerido para requirements.txt:
    
    rich>=13.0.0
    

### Executando o Sistema

Para rodar o sistema, você deve executá-lo como um módulo Python a partir da raiz do projeto (LabVision).

1.  Abra o terminal e navegue até a raiz do seu projeto (ex: cd /caminho/para/Dynamic\ Programming\ 02/LabVision).
2.  Execute o comando:
    bash
    python3 -m src.sistemadegestaodepacientes.main
    

    * *Importante:* Se você encontrar erros de ModuleNotFoundError mesmo após corrigir as importações e usar python3 -m, tente limpar o cache do Python:
        bash
        find . -name "__pycache__" -type d -exec rm -rf {} +
        find . -name "*.pyc" -exec rm {} +
        
        E tente novamente.

## Contribuição (Se for um Projeto em Grupo)

1.  Clone o repositório.
2.  Crie uma nova branch para suas funcionalidades: git checkout -b minha-nova-feature.
3.  Implemente suas mudanças, focando no módulo de sua responsabilidade.
4.  Certifique-se de que todas as importações dentro do pacote sistemadegestaodepacientes sejam *relativas* (ex: from ..model.Paciente import Paciente).
5.  Execute os testes unitários (quando criados) e teste o fluxo completo do seu módulo.
6.  Faça commit das suas mudanças e envie para o repositório.
7.  Abra um Pull Request para revisão.




## Organização das pastas

├───src/
│   ├───sistemadegestaodepacientes/
│   │   ├───_init_.py
│   │   │
│   │   ├───model/                   # Classes que representam as entidades de dados (Paciente, Exame, etc.)
│   │   │   ├───_init_.py
│   │   │   ├───paciente.py
│   │   │   ├───prioridade_cor.py
│   │   │   ├───tipo_exame.py        # Módulo 2/3
│   │   │   ├───atendimento_medico.py# Módulo 2
│   │   │   ├───exame.py             # Módulo 2/3
│   │   │   ├───resultado_exame.py   # Futuro/Opcional (se não integrado em Exame)
│   │   │   └───fila_base.py         # Futuro/Opcional (base para abstração de filas)
│   │   │
│   │   ├───service/                 # Lógica de negócio, validações, cálculos de prioridade e coordenação
│   │   │   ├───_init_.py
│   │   │   ├───paciente_service.py
│   │   │   ├───fila_service.py      # Lógica central de prioridade das filas
│   │   │   ├───atendimento_service.py # Módulo 2
│   │   │   └───exame_service.py     # Módulo 3
│   │   │
│   │   ├───repository/              # Camada de acesso a dados (simulada em memória com dicionários/listas)
│   │   │   ├───_init_.py
│   │   │   ├───paciente_repository.py
│   │   │   ├───fila_atendimento_medico_repository.py
│   │   │   ├───fila_exames_repository.py
│   │   │   ├───atendimento_medico_repository.py # Módulo 2
│   │   │   └───exame_repository.py  # Módulo 3
│   │   │
│   │   ├───util/                    # Funções e classes utilitárias gerais (validação de CPF, formatação de datas)
│   │   │   ├───_init_.py
│   │   │   ├───cpf_validator.py
│   │   │   └───date_util.py
│   │   │
│   │   ├───modulo_recepcao_triagem/   # Módulo 1: Recepção e Triagem (seu módulo principal)
│   │   │   ├───_init_.py
│   │   │   ├───controller/
│   │   │   │   ├───_init_.py
│   │   │   │   └───triagem_controller.py
│   │   │   ├───view/
│   │   │   │   ├───_init_.py
│   │   │   │   └───tela_recepcao_triagem.py
│   │   │
│   │   ├───modulo_consultorio_medico/ # Módulo 2: Consultório Médico
│   │   │   ├───_init_.py
│   │   │   ├───controller/
│   │   │   │   ├───_init_.py
│   │   │   │   └───atendimento_controller.py
│   │   │   ├───view/
│   │   │   │   ├───_init_.py
│   │   │   │   └───tela_consultorio_medico.py
│   │   │
│   │   ├───modulo_exames/           # Módulo 3: Exames
│   │   │   ├───_init_.py
│   │   │   ├───controller/
│   │   │   │   ├───_init_.py
│   │   │   │   └───exame_controller.py
│   │   │   ├───view/
│   │   │   │   ├───_init_.py
│   │   │   │   └───tela_exames.py
│   │   │
│   │   └───main.py                  # Ponto de entrada principal da aplicação
│   │
├───data/                            # Futura pasta para dados persistentes (JSON, SQLite)
├───docs/                            # Documentação do projeto (diagramas, especificações)
├───tests/                           # Testes unitários e de integração
├───.gitignore                       # Arquivo para controle de versão (Git)
├───README.md                        # Este arquivo!
└───requirements.txt                 # Dependências do projeto


## Licença

Gabriel Caetano Cordeiro Wanderley - RM 557582
gabrielccwanderley1@gmail.com
—————————————————
Jefferson Junior Alvarez Urbina - RM 558497
jeffersonjunior1645@gmail.com
—————————————————
Gabriel Barros Mazzariol - RM 555410
gabrielbmazzariol@gmail.com
—————————————————
Ygor Vieira Pontes - RM 555686
ygorvieirapontes7009@gmail.com
—————————————————
Augusto Barcelos Barros - RM 565065
augustobb@live.com
—————————————————


