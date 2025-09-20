"""
Pydantic схемы для API предсказаний NER.
"""

from pydantic import BaseModel, Field
from typing import List


class PredictRequest(BaseModel):
    """Схема запроса для предсказания NER."""
    
    input: str = Field(
        ..., 
        min_length=1, 
        max_length=1000,
        description="Текстовый запрос для анализа сущностей",
        example="молоко 2.5% 1л Домик в деревне"
    )


class Entity(BaseModel):
    """Схема сущности, найденной в тексте."""
    
    start_index: int = Field(
        ..., 
        ge=0,
        description="Начальная позиция сущности в тексте"
    )
    
    end_index: int = Field(
        ..., 
        ge=0,
        description="Конечная позиция сущности в тексте"
    )
    
    entity: str = Field(
        ...,
        description="Тип сущности (TYPE, BRAND, VOLUME, PERCENT, etc.)"
    )


class PredictResponse(BaseModel):
    """Схема ответа с найденными сущностями."""
    
    entities: List[Entity] = Field(
        ...,
        description="Список найденных сущностей в тексте"
    )
    
    input_text: str = Field(
        ...,
        description="Исходный текст запроса"
    )
    
    total_entities: int = Field(
        ...,
        description="Общее количество найденных сущностей"
    )


class ErrorResponse(BaseModel):
    """Схема ответа об ошибке."""
    
    error: str = Field(
        ...,
        description="Описание ошибки"
    )
    
    detail: str = Field(
        ...,
        description="Детали ошибки"
    )
