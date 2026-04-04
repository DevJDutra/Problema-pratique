# Controle de Academia

Aplicativo simples para controle de maquinas e consulta simulada de mensalidades.
Agora tambem inclui contagem persistente de pessoas presentes na academia.
Tambem permite registrar anotacoes e defeitos das maquinas com persistencia em banco.

## Requisitos

- Python 3.10 ou superior

## Como executar

```bash
py app.py
```

Depois, abra `http://127.0.0.1:8000`.

## Funcionalidades

- Consulta do status de maquinas da academia
- Registro de anotacoes e denuncias de defeitos por maquina
- Atualizacao de status, data de manutencao e observacao do equipamento
- Cadastro e remocao de maquinas do catalogo
- Consulta de mensalidade por numero de matricula
- Contagem de pessoas presentes com persistencia em banco SQLite
- API simulada para facilitar futuras integracoes

## Matriculas de exemplo

- `1001`
- `1002`
- `1003`
- `1004`
