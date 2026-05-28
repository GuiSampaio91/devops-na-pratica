"""Testes automatizados da API de Tarefas.

Executados no pipeline de CI via pytest. Cobertura mínima esperada: 80%.
"""

import pytest

from app.main import create_app


@pytest.fixture()
def client():
    """Fixture que devolve um cliente Flask isolado para cada teste."""
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_health_endpoint_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_list_tasks_starts_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_task_returns_201_with_payload(client):
    response = client.post("/tasks", json={"title": "Estudar DevOps"})
    assert response.status_code == 201
    body = response.get_json()
    assert body["id"] == 1
    assert body["title"] == "Estudar DevOps"
    assert body["done"] is False


def test_create_task_without_title_returns_400(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400
    assert "obrigatório" in response.get_json()["error"]


def test_get_task_returns_404_when_missing(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_update_task_marks_as_done(client):
    created = client.post("/tasks", json={"title": "Configurar CI"}).get_json()
    response = client.put(f"/tasks/{created['id']}", json={"done": True})
    assert response.status_code == 200
    assert response.get_json()["done"] is True


def test_delete_task_returns_204_and_removes_resource(client):
    created = client.post("/tasks", json={"title": "Provisionar EC2"}).get_json()
    delete_response = client.delete(f"/tasks/{created['id']}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{created['id']}")
    assert get_response.status_code == 404


def test_full_crud_flow(client):
    """Fluxo ponta-a-ponta para validar a integração entre as rotas."""
    # cria
    created = client.post("/tasks", json={"title": "  Aplicar Terraform  "})
    assert created.status_code == 201
    task = created.get_json()
    assert task["title"] == "Aplicar Terraform"  # strip aplicado

    # lista
    listed = client.get("/tasks").get_json()
    assert len(listed) == 1

    # atualiza título e status
    updated = client.put(
        f"/tasks/{task['id']}", json={"title": "Aplicar IaC", "done": True}
    ).get_json()
    assert updated["title"] == "Aplicar IaC"
    assert updated["done"] is True

    # remove
    assert client.delete(f"/tasks/{task['id']}").status_code == 204
    assert client.get("/tasks").get_json() == []
