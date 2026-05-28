# DevOps na Prática — Fase 1: Configuração e Automação Inicial

[![CI](https://github.com/GuiSampaio91/devops-na-pratica/actions/workflows/ci.yml/badge.svg)](https://github.com/GuiSampaio91/devops-na-pratica/actions/workflows/ci.yml)

Repositório referente à **Fase 1** do projeto da disciplina **DevOps na Prática**
do curso de Sistemas de Informação (PUCRS Online).

A aplicação utilizada como objeto do projeto é uma **API REST de Lista de
Tarefas** escrita em Python/Flask, cujo ciclo de vida (build, teste, validação
de infra e empacotamento) é totalmente automatizado por meio de
**GitHub Actions** e **Terraform**.

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
├── .github/workflows/    # Pipeline de Integração Contínua
│   └── ci.yml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Executando localmente

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pytest                              # roda todos os testes
flask --app app.main run            # sobe a API em http://localhost:5000
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

## Pipeline de CI

O workflow `.github/workflows/ci.yml` é disparado em todo `push` e `pull_request`
para a branch `main`, executando quatro jobs em sequência:

1. **lint** — análise estática com `flake8`.
2. **test** — testes unitários com `pytest` exigindo cobertura mínima de 80%.
3. **terraform-validate** — `terraform fmt`, `init` e `validate` dos scripts de IaC.
4. **build** — empacota a aplicação e publica o artefato `.tar.gz`.

## Infraestrutura como Código

Os scripts em `infra/` provisionam uma EC2 `t2.micro` na AWS, com Security
Group apropriado, e fazem o bootstrap da aplicação via `user_data.sh`.
Detalhes em [`infra/README.md`](infra/README.md).

## Autor

**Guilherme Sampaio** — Sistemas de Informação, PUCRS Online.
