import random
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

# Получить активный тираж
def get_active_draw(db: Session):
    return db.query(models.Draw).filter(models.Draw.status == "active").first()

# Создать новый тираж
def create_draw(db: Session):
    active_draw = get_active_draw(db)
    if active_draw:
        return None # Разрешен только один активный тираж

    db_draw = models.Draw(status="active")
    db.add(db_draw)
    db.commit()
    db.refresh(db_draw)
    return db_draw

# Создать новый билет
def create_ticket(db: Session, ticket: schemas.TicketCreate):
    db_draw = db.query(models.Draw).filter(models.Draw.id == ticket.draw_id).first()
    if not db_draw or db_draw.status != "active":
        return None # Тираж не существует или не активен

    numbers_str = ",".join(map(str, ticket.numbers))
    db_ticket = models.Ticket(draw_id=ticket.draw_id, numbers=numbers_str)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

# Завершить тираж и определить победителей
def close_draw(db: Session, draw_id: int):
    db_draw = db.query(models.Draw).filter(models.Draw.id == draw_id).first()
    if not db_draw or db_draw.status != "active":
        return None # Тираж не существует или не активен

    # Генерируем 5 случайных выигрышных чисел
    winning_numbers = sorted(random.sample(range(1, 37), 5))
    winning_numbers_str = ",".join(map(str, winning_numbers))
    db_draw.winning_numbers = winning_numbers_str
    db_draw.status = "closed"

    # Определяем победителей
    tickets = db.query(models.Ticket).filter(models.Ticket.draw_id == draw_id).all()
    for ticket in tickets:
        # Преобразуем строку чисел билета в список и сортируем для сравнения
        ticket_numbers = sorted([int(x) for x in ticket.numbers.split(',')])
        if ticket_numbers == winning_numbers:
            ticket.is_winner = True

    db.commit()
    db.refresh(db_draw)
    return db_draw

# Получить результаты тиража
def get_draw_results(db: Session, draw_id: int):
    db_draw = db.query(models.Draw).filter(models.Draw.id == draw_id).first()
    if not db_draw:
        return None, None # Тираж не найден

    tickets = db.query(models.Ticket).filter(models.Ticket.draw_id == draw_id).all()
    return db_draw, tickets