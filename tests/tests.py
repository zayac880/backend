from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


shift_task_data = {
    "СтатусЗакрытия": "True",
    "ПредставлениеЗаданияНаСмену": "string",
    "Рабочий центр": "string",
    "Смена": "string",
    "Бригада": "string",
    "НомерПартии": 0,
    "ДатаПартии": "2024-02-13",
    "Номенклатура": "string",
    "КодЕКН": "string",
    "ИдентификаторРЦ": "string",
    "ДатаВремяНачалаСмены": "2024-02-13T18:02:27.992Z",
    "ДатаВремяОкончанияСмены": "2024-02-13T18:02:27.992Z",
    "id": 20
}


def test_create_shift_task():
    response = client.post("/shift-tasks/create", json=shift_task_data)

    assert response.status_code == 200
    created_task = response.json()
    assert created_task


def test_get_shift_task_id():
    response_create = client.post("/shift-tasks/create", json=shift_task_data)
    assert response_create.status_code == 200
    created_task = response_create.json()
    task_id = created_task["id"]

    response_get = client.get(f"/shift-tasks/get-{task_id}")

    assert response_get.status_code == 200

    retrieved_task = response_get.json()
    assert retrieved_task["id"] == task_id
    assert str(retrieved_task["status"]) == shift_task_data["СтатусЗакрытия"]


def test_update_shift_task():
    response_create = client.post("/shift-tasks/create", json=shift_task_data)
    assert response_create.status_code == 200
    created_task = response_create.json()
    task_id = created_task["id"]

    updated_shift_task_data = {
        "workshop": "updated string",
        "task_description": "updated string",
    }
    response_update = client.put(f"/shift-tasks/update-{task_id}", json=updated_shift_task_data)
    assert response_update.status_code == 200

    updated_task = response_update.json()
    assert updated_task["id"] == task_id
    assert updated_task["workshop"] == updated_shift_task_data["workshop"]
    assert updated_task["task_description"] == updated_shift_task_data["task_description"]


def test_filter_get_shift_tasks():
    filters = {
        "status": "True"
    }

    response = client.get("/shift-tasks/filter", params=filters)

    assert response.status_code == 200

    shift_tasks = response.json()
    for task in shift_tasks:
        assert str(task["status"]) == filters["status"]

