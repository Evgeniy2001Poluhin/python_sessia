import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./lottery.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    conn = sqlite3.connect("./lottery.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS draws (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT NOT NULL,
            winning_numbers TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            draw_id INTEGER NOT NULL,
            numbers TEXT NOT NULL,
            is_winner BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (draw_id) REFERENCES draws(id)
        );
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("База данных 'lottery.db' и таблицы созданы (если их не было).")