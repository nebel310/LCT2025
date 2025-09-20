import uvicorn
import logging
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from router.auth import router as auth_router
from router.predict import router as predict_router
from model import ner_model




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Пропускаем БД для тестирования NER
    logger.info('Режим тестирования NER - БД отключена')
    
    # Загрузка NER модели
    try:
        await ner_model.load_model()
        logger.info('NER модель загружена успешно')
    except Exception as e:
        logger.error(f'Ошибка загрузки NER модели: {e}')
        # Не останавливаем приложение, если модель не загрузилась
    
    yield
    
    logger.info('Выключение приложения')


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Пятёрочка NER API",
        version="1.0.0",
        description="API для поиска товаров с использованием NER (Named Entity Recognition). Включает авторизацию JWT и анализ сущностей в текстовых запросах.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    secured_paths = {
        #Авторизация
        "/auth/me": {"method": "get", "security": [{"Bearer": []}]},
        "/auth/logout": {"method": "post", "security": [{"Bearer": []}]},
    }
    
    for path, config in secured_paths.items():
        if path in openapi_schema["paths"]:
            openapi_schema["paths"][path][config["method"]]["security"] = config["security"]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(lifespan=lifespan)
app.openapi = custom_openapi

# Подключение роутеров
# app.include_router(auth_router)  # Отключено для тестирования NER
app.include_router(predict_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники для локальной разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#Раскоментить, когда будешь писать докер.
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        host='0.0.0.0',
        port=3001
    )