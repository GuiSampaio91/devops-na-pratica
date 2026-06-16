# DevOps na Prática — API de Tarefas

[![CI/CD](https://github.com/GuiSampaio91/devops-na-pratica/actions/workflows/ci.yml/badge.svg)](https://github.com/GuiSampaio91/devops-na-pratica/actions/workflows/ci.yml)

Projeto da disciplina **DevOps na Prática** (Sistemas de Informação — PUCRS Online).

A aplicação é uma **API REST de Lista de Tarefas** em Python/Flask, usada como
objeto para automatizar todo o ciclo de vida do software: integração contínua
(lint, testes, validação de IaC), análise de segurança, containerização com
Docker e entrega contínua da imagem para o GitHub Container Registry.

---

## Estrutura do repositório

```
devops-na-pratica/
├── app/                  # Código-fonte da API Flask
│   └── main.py
├── tests/                # Testes automatizados (pytest)
│   └── test_main.py
├── infra/                # Infraestrutura como Código (Terraform)
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── user_data.sh
├── deploy/               # Deploy com containers
│   ├── docker-compose.prod.yml
│   └── deploy.sh
├── .github/workflows/    # Pipeline de CI/CD (GitHub Actions)
│   └── ci.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Executando localmente

Com Python:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pytest                              # roda todos os testes
flask --app app.main run            # sobe a API em http://localhost:5000
```

Com Docker:

```bash
docker compose up --build          # sobe a API em http://localhost:5000
```

## Endpoints

| Método | Rota              | Descrição                       |
|--------|-------------------|---------------------------------|
| GET    | `/health`         | Health-check                    |
| GET    | `/tasks`          | Lista todas as tarefas          |
| POST   | `/tasks`          | Cria uma nova tarefa            |
| GET    | `/tasks/{id}`     | Detalha uma tarefa específica   |
| PUT    | `/tasks/{id}`     | Atualiza título / status        |
| DELETE | `/tasks/{id}`     | Remove a tarefa                 |

## Pipeline de CI/CD

O workflow `.github/workflows/ci.yml` roda em todo `push` e `pull_request` para a
branch `main` (e manualmente via `workflow_dispatch`):

| Job | Descrição |
|-----|-----------|
| `lint` | Análise estática com `flake8`. |
| `test` | Testes com `pytest` e cobertura mínima de 80% (depende do `lint`). |
| `terraform-validate` | `fmt`, `init` e `validate` dos scripts de IaC (paralelo ao `lint`). |
| `security` | Build da imagem e scan de vulnerabilidades com **Trivy** (depende do `lint`). |
| `build` | Empacota o artefato `.tar.gz` (depende de `test` e `terraform-validate`). |
| `docker` | **Entrega Contínua**: build e push da imagem para o `ghcr.io`, só em push na `main` (depende de `test` e `terraform-validate`). |

## Containerização

A aplicação é empacotada por um [`Dockerfile`](Dockerfile) baseado em
`python:3.11-slim`, rodando com gunicorn sob um usuário sem privilégios e com
`HEALTHCHECK` apontando para `/health`. A cada push na `main`, o pipeline publica
a imagem em:

```
ghcr.io/guisampaio91/devops-na-pratica:latest
```

## Deploy

Os scripts em [`deploy/`](deploy/) sobem o container a partir da imagem publicada
(sem build local):

```bash
cd deploy
./deploy.sh                  # usa a tag 'latest'
./deploy.sh <sha-do-commit>  # usa uma tag específica
```

## Infraestrutura como Código

Os scripts em `infra/` provisionam uma EC2 `t2.micro` na AWS, com Security Group
apropriado, e fazem o bootstrap da aplicação via `user_data.sh`. Detalhes em
[`infra/README.md`](infra/README.md).

## Autor

**Guilherme Sampaio** — Sistemas de Informação, PUCRS Online.
