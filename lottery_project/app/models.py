from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Модель для лотерейного тиража
class Draw(Base):
    __tablename__ = "draws"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="active")  # "active", "closed"
    winning_numbers = Column(String, nullable=True) # Числа-победители в виде строки, разделенной запятыми

    # Отношение к билетам
    tickets = relationship("Ticket", back_populates="draw")

# Модель для лотерейного билета
class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    draw_id = Column(Integer, ForeignKey("draws.id"))
    numbers = Column(String) # 5 уникальных чисел в виде строки, разделенной запятыми
    is_winner = Column(Boolean, default=False)

    # Отношение к тиражу
    draw = relationship("Draw", back_populates="tickets")