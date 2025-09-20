"""
Роутер для API предсказаний NER.
"""

import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List

from schemas.predict import PredictRequest, Entity, PredictResponse, ErrorResponse
from model import ner_model

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["NER Prediction"])


@router.post(
    "/predict",
    response_model=PredictResponse,
    responses={
        200: {
            "description": "Успешное предсказание сущностей",
            "content": {
                "application/json": {
                    "example": {
                        "entities": [
                            {"start_index": 0, "end_index": 6, "entity": "B-TYPE"},
                            {"start_index": 7, "end_index": 11, "entity": "I-TYPE"},
                            {"start_index": 12, "end_index": 16, "entity": "B-PERCENT"},
                            {"start_index": 17, "end_index": 19, "entity": "B-VOLUME"},
                            {"start_index": 20, "end_index": 25, "entity": "B-BRAND"}
                        ],
                        "input_text": "молоко 2.5% 1л Домик",
                        "total_entities": 5
                    }
                }
            }
        },
        503: {
            "description": "Модель не загружена",
            "model": ErrorResponse
        },
        500: {
            "description": "Внутренняя ошибка сервера",
            "model": ErrorResponse
        }
    }
)
async def predict_entities(request: PredictRequest) -> PredictResponse:
    """
    Предсказывает сущности в текстовом запросе.
    
    Принимает текстовый запрос и возвращает список найденных сущностей
    с их позициями и типами (TYPE, BRAND, VOLUME, PERCENT и т.д.).
    """
    try:
        # Проверяем, что модель загружена
        if not ner_model.is_loaded:
            logger.error("Модель не загружена")
            raise HTTPException(
                status_code=503, 
                detail="Модель NER не загружена. Попробуйте позже."
            )
        
        # Выполняем предсказание
        logger.info(f"Обработка запроса: '{request.input[:50]}...'")
        raw_entities = ner_model.predict(request.input)
        
        # Преобразуем результат в нужный формат
        entities = [
            Entity(
                start_index=item["start"],
                end_index=item["end"],
                entity=item["label"]
            )
            for item in raw_entities
        ]
        
        logger.info(f"Найдено {len(entities)} сущностей")
        
        return PredictResponse(
            entities=entities,
            input_text=request.input,
            total_entities=len(entities)
        )
        
    except HTTPException:
        # Перебрасываем HTTP исключения
        raise
    except Exception as e:
        logger.error(f"Ошибка при предсказании: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )


@router.get(
    "/predict/health",
    summary="Проверка состояния модели",
    description="Проверяет, загружена ли модель NER и готова ли к работе"
)
async def health_check():
    """Проверка состояния модели NER."""
    model_info = ner_model.get_model_info()
    
    if not model_info["is_loaded"]:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unavailable",
                "message": "Модель не загружена",
                "model_info": model_info
            }
        )
    
    return {
        "status": "ready",
        "message": "Модель готова к работе",
        "model_info": model_info
    }
