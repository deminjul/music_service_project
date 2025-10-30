from sqlmodel import SQLModel, create_engine, Session

# ЗАМЕНИТЕ 'your_password' на реальный пароль!
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "music_service"
DB_USER = "postgres"
DB_PASSWORD = "pr23pr24pr25"  # ⬅️ ЗДЕСЬ ВАШ ПАРОЛЬ

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    print("✅ Таблицы созданы успешно!")

def get_session():
    with Session(engine) as session:
        yield session