"""
GLiNER модель для NER (Named Entity Recognition) в продуктовом поиске.
Модель: empathyai/gliner_large-v2.5-groceries
"""

import logging
import os
from typing import Optional, List, Dict, Any
from gliner import GLiNER
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class NERModel:
    """Класс для работы с GLiNER моделью NER."""
    
    def __init__(self):
        self.model: Optional[GLiNER] = None
        self.model_name = "urchade/gliner_base"
        self.is_loaded = False
    
    async def load_model(self) -> None:
        """Загружает GLiNER модель."""
        try:
            logger.info(f"Загрузка модели {self.model_name}...")
            
            # Получаем токен из переменных окружения
            token = os.getenv("HUGGINGFACE_HUB_TOKEN")
            
            if token:
                logger.info("Используется токен Hugging Face")
                self.model = GLiNER.from_pretrained(self.model_name, token=token)
            else:
                logger.warning("Токен Hugging Face не найден. Попытка загрузки без токена...")
                self.model = GLiNER.from_pretrained(self.model_name)
            
            self.is_loaded = True
            logger.info("Модель успешно загружена")
        except Exception as e:
            logger.error(f"Ошибка загрузки модели: {e}")
            logger.error("Убедитесь, что у вас есть доступ к модели и установлен токен HUGGINGFACE_HUB_TOKEN")
            raise e
    
    def predict(self, text: str) -> List[Dict[str, Any]]:
        """
        Выполняет NER предсказание на тексте.
        
        Args:
            text: Входной текст для анализа
            
        Returns:
            Список словарей с сущностями: [{"start": int, "end": int, "label": str}, ...]
        """
        if not self.is_loaded or self.model is None:
            raise RuntimeError("Модель не загружена")
        
        try:
            # Определяем метки для поиска в соответствии с задачей
            labels = ["TYPE", "BRAND", "VOLUME", "PERCENT"]
            
            # GLiNER возвращает список словарей с ключами: start, end, label
            entities = self.model.predict_entities(text, labels, threshold=0.5)
            logger.info(f"Найдено {len(entities)} сущностей в тексте: '{text[:50]}...'")
            return entities
        except Exception as e:
            logger.error(f"Ошибка предсказания: {e}")
            raise e
    
    def get_model_info(self) -> Dict[str, Any]:
        """Возвращает информацию о модели."""
        return {
            "model_name": self.model_name,
            "is_loaded": self.is_loaded,
            "model_type": "GLiNER"
        }

# Глобальный экземпляр модели
ner_model = NERModel()
