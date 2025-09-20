"""
Тесты для API предсказаний NER.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)


class TestPredictAPI:
    """Тесты для эндпоинта /api/predict."""
    
    def test_predict_success(self):
        """Тест успешного предсказания сущностей."""
        # Мокаем модель
        mock_entities = [
            {"start": 0, "end": 6, "label": "B-TYPE"},
            {"start": 7, "end": 11, "label": "I-TYPE"},
            {"start": 12, "end": 16, "label": "B-PERCENT"},
            {"start": 17, "end": 19, "label": "B-VOLUME"},
            {"start": 20, "end": 25, "label": "B-BRAND"}
        ]
        
        with patch('model.ner_model.is_loaded', True), \
             patch('model.ner_model.predict', return_value=mock_entities):
            
            response = client.post(
                "/api/predict",
                json={"input": "молоко 2.5% 1л Домик"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert "entities" in data
            assert "input_text" in data
            assert "total_entities" in data
            assert data["input_text"] == "молоко 2.5% 1л Домик"
            assert data["total_entities"] == 5
            assert len(data["entities"]) == 5
            
            # Проверяем первую сущность
            first_entity = data["entities"][0]
            assert first_entity["start_index"] == 0
            assert first_entity["end_index"] == 6
            assert first_entity["entity"] == "B-TYPE"
    
    def test_predict_model_not_loaded(self):
        """Тест когда модель не загружена."""
        with patch('model.ner_model.is_loaded', False):
            response = client.post(
                "/api/predict",
                json={"input": "молоко"}
            )
            
            assert response.status_code == 503
            data = response.json()
            assert "detail" in data
            assert "не загружена" in data["detail"]
    
    def test_predict_empty_input(self):
        """Тест с пустым входом."""
        response = client.post(
            "/api/predict",
            json={"input": ""}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_predict_long_input(self):
        """Тест с очень длинным входом."""
        long_input = "молоко " * 200  # Превышает лимит в 1000 символов
        
        response = client.post(
            "/api/predict",
            json={"input": long_input}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_predict_model_error(self):
        """Тест ошибки модели."""
        with patch('model.ner_model.is_loaded', True), \
             patch('model.ner_model.predict', side_effect=Exception("Model error")):
            
            response = client.post(
                "/api/predict",
                json={"input": "молоко"}
            )
            
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
            assert "Model error" in data["detail"]
    
    def test_predict_health_check(self):
        """Тест проверки состояния модели."""
        with patch('model.ner_model.get_model_info', return_value={
            "model_name": "urchade/gliner_base",
            "is_loaded": True,
            "model_type": "GLiNER"
        }):
            response = client.get("/api/predict/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ready"
            assert data["model_info"]["is_loaded"] is True
    
    def test_predict_health_check_not_loaded(self):
        """Тест проверки состояния когда модель не загружена."""
        with patch('model.ner_model.get_model_info', return_value={
            "model_name": "urchade/gliner_base",
            "is_loaded": False,
            "model_type": "GLiNER"
        }):
            response = client.get("/api/predict/health")
            
            assert response.status_code == 503
            data = response.json()
            assert data["status"] == "unavailable"
            assert data["model_info"]["is_loaded"] is False


class TestPredictValidation:
    """Тесты валидации входных данных."""
    
    def test_missing_input_field(self):
        """Тест отсутствующего поля input."""
        response = client.post(
            "/api/predict",
            json={}
        )
        
        assert response.status_code == 422
    
    def test_invalid_input_type(self):
        """Тест неверного типа поля input."""
        response = client.post(
            "/api/predict",
            json={"input": 123}
        )
        
        assert response.status_code == 422
