import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.api.routes import get_model
import json

@pytest.mark.asyncio
async def test_analyze_comments():

    class MockModel:
        def predict(self, text):
            if "Плохо" in text:
                return {"label": "NEGATIVE", "score": 0.99}
            return {"label": "POSITIVE", "score": 0.99}

    def mock_get_model():
        return MockModel()

    app.dependency_overrides[get_model] = mock_get_model

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/analyze", json={"comments": ["Отличный сервис!", "Плохо работает"]})

    assert response.status_code == 200
    data = response.json()
    assert "positive" in data
    assert "negative" in data
    assert isinstance(data["results"], list)
    assert all("text" in r for r in data["results"])
    
    app.dependency_overrides.clear()
    
@pytest.mark.asyncio
async def test_analyze_comments_file_json(tmp_path):
    class MockModel:
        def predict(self, text):
            return {"label": "NEGATIVE", "score": 0.99}

    def mock_get_model():
        return MockModel()

    app.dependency_overrides[get_model] = mock_get_model

    json_file = tmp_path / "comments.json"
    json_file.write_text(json.dumps({"comments": ["Кошмарный сервис", "Ужасно"]}), encoding="utf-8")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        with open(json_file, "rb") as f:
            response = await ac.post(
                "/api/analyze/file",
                files={"file": ("comments.json", f, "application/json")}
            )
    
    assert response.status_code == 200
    data = response.json()
    assert "negative" in data
    assert data["negative"] == 2
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_analyze_comments_file_text(tmp_path):
    class MockModel:
        def predict(self, text):
            return {"label": "POSITIVE", "score": 0.99}

    def mock_get_model():
        return MockModel()

    app.dependency_overrides[get_model] = mock_get_model

    txt_file = tmp_path / "comments.txt"
    txt_file.write_text("Отлично!\nПотрясающе!\n", encoding="utf-8")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        with open(txt_file, "rb") as f:
            response = await ac.post(
                "/api/analyze/file",
                files={"file": ("comments.txt", f, "text/plain")}
            )

    assert response.status_code == 200
    data = response.json()
    assert "positive" in data
    assert data["positive"] == 2
    
    app.dependency_overrides.clear()