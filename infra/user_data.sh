#!/bin/bash
###############################################################################
# user_data.sh
# Script de bootstrap executado pela EC2 no primeiro boot.
# Instala Python 3 + pip, baixa o código da aplicação a partir do repositório
# e sobe a API com gunicorn como serviço systemd.
###############################################################################
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

# 1. Atualiza pacotes e instala dependências do sistema
apt-get update -y
apt-get install -y python3 python3-pip python3-venv git

# 2. Cria usuário de aplicação
useradd --create-home --shell /bin/bash app || true

# 3. Clona o código (ajuste a URL após criar o repositório no GitHub)
sudo -u app -H git clone https://github.com/GuiSampaio91/devops-na-pratica.git /home/app/devops-na-pratica || true

# 4. Cria virtualenv e instala dependências
sudo -u app -H bash -lc "
  cd /home/app/devops-na-pratica &&
  python3 -m venv .venv &&
  .venv/bin/pip install --upgrade pip &&
  .venv/bin/pip install -r requirements.txt
"

# 5. Configura serviço systemd para a API
cat > /etc/systemd/system/todo-api.service <<'UNIT'
[Unit]
Description=API de Tarefas - DevOps na Pratica
After=network.target

[Service]
User=app
WorkingDirectory=/home/app/devops-na-pratica
ExecStart=/home/app/devops-na-pratica/.venv/bin/gunicorn -b 0.0.0.0:5000 app.main:app
Restart=always

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable --now todo-api.service
