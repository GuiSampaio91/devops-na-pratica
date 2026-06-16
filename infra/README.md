# Infraestrutura como Código (Terraform)

Este diretório contém os scripts Terraform que provisionam a infraestrutura
mínima para hospedar a API de Tarefas na AWS.

## Recursos provisionados

| Recurso | Descrição |
|---------|-----------|
| `aws_security_group.app` | Libera 22 (SSH), 80 (HTTP) e 5000 (Flask) |
| `aws_instance.app`       | EC2 `t2.micro` Ubuntu 22.04 LTS (free tier) |
| `user_data.sh`           | Script de bootstrap que instala Python, clona o repositório e sobe o serviço via `systemd` |

## Pré-requisitos

- Terraform >= 1.5
- AWS CLI configurado (`aws configure`) com credenciais válidas

## Uso

```bash
cd infra
terraform init
terraform plan
terraform apply -auto-approve
```

Ao final, o Terraform imprime a URL pública da aplicação no output `app_url`.

Para destruir tudo:

```bash
terraform destroy -auto-approve
```
