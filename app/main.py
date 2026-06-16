"""
API REST de Lista de Tarefas (To-Do List).

Aplicação simples em Flask usada como objeto do projeto da disciplina
DevOps na Prática (Fase 1). Expõe endpoints CRUD em memória para que o
pipeline de CI possa exercitar lint, testes e build de forma reprodutível.
"""

from __future__ import annotations

from typing import Dict

from flask import Flask, jsonify, request


def create_app() -> Flask:
    """Application factory que facilita o uso em testes."""
    app = Flask(__name__)

    # Persistência em memória, suficiente para fins didáticos.
    tasks: Dict[int, Dict] = {}
    next_id: Dict[str, int] = {"value": 1}

    @app.get("/health")
    def health():
        """Endpoint de health-check usado pelo load balancer / CI."""
        return jsonify(status="ok"), 200

    @app.get("/tasks")
    def list_tasks():
        """Lista todas as tarefas cadastradas."""
        return jsonify(list(tasks.values())), 200

    @app.post("/tasks")
    def create_task():
        """Cria uma nova tarefa. Espera JSON com campo 'title'."""
        payload = request.get_json(silent=True) or {}
        title = payload.get("title")
        if not title or not isinstance(title, str):
            return jsonify(error="campo 'title' é obrigatório"), 400

        task_id = next_id["value"]
        next_id["value"] += 1
        task = {"id": task_id, "title": title.strip(), "done": False}
        tasks[task_id] = task
        return jsonify(task), 201

    @app.get("/tasks/<int:task_id>")
    def get_task(task_id: int):
        task = tasks.get(task_id)
        if not task:
            return jsonify(error="tarefa não encontrada"), 404
        return jsonify(task), 200

    @app.put("/tasks/<int:task_id>")
    def update_task(task_id: int):
        task = tasks.get(task_id)
        if not task:
            return jsonify(error="tarefa não encontrada"), 404

        payload = request.get_json(silent=True) or {}
        if "title" in payload and isinstance(payload["title"], str):
            task["title"] = payload["title"].strip()
        if "done" in payload and isinstance(payload["done"], bool):
            task["done"] = payload["done"]
        return jsonify(task), 200

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id: int):
        if task_id not in tasks:
            return jsonify(error="tarefa não encontrada"), 404
        del tasks[task_id]
        return "", 204

    return app


# Instância default, usada pelo gunicorn em produção (gunicorn app.main:app).
app = create_app()


if __name__ == "__main__":  # pragma: no cover
    app.run(host="0.0.0.0", port=5000, debug=False)
