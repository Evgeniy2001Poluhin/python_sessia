from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from . import crud, models, schemas
from .database import engine, init_db, get_db

# Инициализируем таблицы базы данных при запуске приложения
init_db()

app = FastAPI(
    title="Lottery API",
    description="Простое API для управления лотерейными тиражами и билетами.",
    version="1.0.0"
)

# Эндпоинт для создания нового тиража
@app.post("/draws", response_model=schemas.DrawCreateResponse, status_code=status.HTTP_201_CREATED,
          summary="Создать новый лотерейный тираж",
          description="Создает новый активный лотерейный тираж. Может быть только один активный тираж.")
def create_new_draw(db: Session = Depends(get_db)):
    db_draw = crud.create_draw(db)
    if db_draw is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Уже есть активный тираж.")
    return db_draw

# Эндпоинт для покупки билета
@app.post("/tickets", response_model=schemas.TicketResponse, status_code=status.HTTP_201_CREATED,
          summary="Купить лотерейный билет",
          description="Позволяет купить лотерейный билет для активного тиража. Билет должен содержать 5 уникальных чисел от 1 до 36.")
def buy_lottery_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    db_ticket = crud.create_ticket(db, ticket=ticket)
    if db_ticket is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Тираж не найден или не активен.")
    return db_ticket

# Эндпоинт для завершения тиража
@app.post("/draws/{draw_id}/close", response_model=schemas.DrawResultResponse,
          summary="Завершить лотерейный тираж",
          description="Завершает активный тираж, генерирует выигрышные числа и определяет победителей.")
def close_lottery_draw(draw_id: int, db: Session = Depends(get_db)):
    db_draw = crud.close_draw(db, draw_id=draw_id)
    if db_draw is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тираж не найден или уже закрыт.")

    # Получаем билеты для отображения в результатах
    _, tickets = crud.get_draw_results(db, draw_id=draw_id)
    return schemas.DrawResultResponse(
        id=db_draw.id,
        status=db_draw.status,
        winning_numbers=[int(x) for x in db_draw.winning_numbers.split(',')] if db_draw.winning_numbers else [],
        tickets=tickets # Pydantic автоматически преобразует список моделей Ticket в TicketResponse
    )

# Эндпоинт для получения результатов тиража
@app.get("/draws/{draw_id}/results", response_model=schemas.DrawResultResponse,
         summary="Получить результаты лотерейного тиража",
         description="Возвращает выигрышные числа и все билеты, участвовавшие в данном тираже.")
def get_lottery_results(draw_id: int, db: Session = Depends(get_db)):
    db_draw, tickets = crud.get_draw_results(db, draw_id=draw_id)
    if db_draw is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тираж не найден.")

    # Используем schemas.DrawResultResponse для форматирования ответа
    # Pydantic автоматически обрабатывает преобразование numbers из строки в список и Ticket в TicketResponse
    return schemas.DrawResultResponse.model_validate(db_draw, context={"tickets": tickets})