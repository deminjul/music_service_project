from models import *
from database import create_db_and_tables

def main():
    # Создаем таблицы в базе данных
    create_db_and_tables()
    print("✅ Таблицы созданы успешно!")
    
    # Здесь будет код для наполнения данными (этап 5)

if __name__ == "__main__":
    main()