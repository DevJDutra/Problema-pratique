## Solução-1 (Resumo)

Sistema de Gestão e Fluxo de Academias:

Proposta de Solução:

-- Otimização de Espaço e Agendamento Externo

Em cenários de academias com alta densidade de alunos, um dos maiores desafios não é apenas o número de usuários, mas a falta de coordenação entre alunos regulares e personal trainers externos. O uso simultâneo de múltiplos equipamentos por consultorias particulares, sem um controle de horários, gera gargalos que prejudicam a experiência de todos.

-- Inteligência na Escala de Profissionais

Esta proposta foca na organização logística como ferramenta de descompressão do ambiente. A hipótese central é que, ao monitorar e agendar a presença de profissionais externos, é possível redistribuir a carga de uso das máquinas de forma equilibrada ao longo do dia.
Os pilares desta solução incluem:

- Tabelas de Organização Dinâmica: Criação de um cronograma digital onde profissionais de fora devem registrar sua janela de atuação.
- Setorização por Agendamento: Controle de quais áreas da academia (ex: área de pesos livres, máquinas de perna ou racks de agachamento) estarão ocupadas em determinados horários, evitando sobrecarga em um único grupamento muscular.
- Gestão de Ocupação: Implementação de um sistema de "vagas" para personals externos durante os horários de pico, garantindo que o aluno da casa sempre tenha acesso ao maquinário essencial.

## Solução-2: Com prototipo

-- Aplicativo de gerenciamento
Um aplicativo para gerenciar:

- maquinas: As maquinas são fichadas, com status de funcionamento, ultima manutenção e anotações que alunos queiram deixar sobre o aparelho.
   
- matriculas: Uma janela de pesquisa de matricula, onde é possivel verificar se a matricula do aluno está ativa ou não.
   
- quantidade de pessoas presentes na academia no momento: Um contador de pessoas que funcione com base na identificação facial que libera a catraca, toda vez que entrar, adiciona 1, toda vez que alguem sair, remove 1 (não temos leitor facial a disposição, então há um botao no projeto para diminuir e aumentar a quantidade de pessoas)

 # Controle de Academia

!!! 100% do codigo foi feito por IA (codex) !!!

Aplicativo para ajudar no controle da academia, com funcoes de:

- consulta de status das maquinas
- registro e remocao de anotacoes ou defeitos
- atualizacao de status, manutencao e observacoes do equipamento
- cadastro e remocao de maquinas do catalogo
- consulta de mensalidade por matriculas
- contagem de pessoas presentes com persistencia em banco SQLite

## Requisitos

Voce precisa ter instalado:

- Python 3.10 ou superior

Se quiser conferir a versao instalada, abra o terminal e digite:

```bash
py --version
```

## Como executar

### Opcao 1: pelo terminal

1. Abra a pasta do projeto no computador.
2. Clique na barra de endereco da pasta e copie o caminho.
3. Abra o terminal do Windows:
   - pode ser o `Prompt de Comando`
   - ou o `PowerShell`
4. No terminal, digite o comando abaixo para entrar na pasta do projeto:

```bash
cd "{caminho-doprojeto}"
```

5. Depois, execute:

```bash
py app.py
```

6. Quando aparecer a mensagem informando o endereco do servidor, abra o navegador.
7. No navegador, acesse:

```text
http://127.0.0.1:8000
```

### Opcao 2: com duplo clique

1. Abra a pasta do projeto.
2. Localize o arquivo `app.py`.
3. De duplo clique em `app.py`.
4. Se o Python estiver associado corretamente no Windows, o servidor sera iniciado.
5. Depois, abra o navegador e acesse:

```text
http://127.0.0.1:8000
```

Observacao:

- Se o duplo clique abrir e fechar muito rapido, prefira a opcao pelo terminal, porque assim fica mais facil ver mensagens de erro.

## Como parar o sistema

Se voce iniciou pelo terminal:

1. Volte para a janela do terminal.
2. Pressione `Ctrl + C`.

## Funcionalidades

- Consultar o status atual de uma maquina
- Registrar anotacoes ou defeitos informados pelos alunos
- Remover anotacoes pelo botao `X`
- Atualizar status da maquina
- Atualizar data da manutencao
- Atualizar observacao do equipamento
- Catalogar novas maquinas
- Remover maquinas do catalogo
- Consultar mensalidade por numero de matricula
- Controlar a quantidade de pessoas presentes na academia

## Matriculas de exemplo

Voce pode testar a consulta de mensalidade usando:

- `1001`
- `1002`
- `1003`
- `1004`
