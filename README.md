# Controle de Academia

!!! 100% do codigo foi feito por IA (codex) !!!

Aplicativo para ajudar no controle da academia, com funcoes de:

- consulta de status das maquinas
- registro e remocao de anotacoes ou defeitos
- atualizacao de status, manutencao e observacoes do equipamento
- cadastro e remocao de maquinas do catalogo
- consulta de mensalidade por matricula
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
