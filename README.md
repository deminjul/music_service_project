# Music Service API

API для музыкального сервиса с использованием FastAPI, SQLModel и PostgreSQL.

##  Быстрый старт

### Предварительные требования
- Python 3.8+
- PostgreSQL 12+

### Установка и запуск

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/deminjul/music-service-api.git
cd music-service-api

##  Основные запросы API (Endpoints)

### Пользователи
- `GET /users/` - Получить список всех пользователей
- `GET /users/{id}` - Получить пользователя по ID

### Артисты
- `GET /artists/` - Получить список всех артистов
- `GET /artists/{id}` - Получить артиста по ID
- `GET /artists/{id}/albums` - Получить альбомы артиста

### Альбомы  
- `GET /albums/` - Получить список всех альбомов
- `GET /albums/{id}` - Получить альбом по ID
- `GET /albums/{id}/tracks` - Получить треки альбома

### Треки
- `GET /tracks/` - Получить список всех треков
- `GET /tracks/{id}` - Получить трек по ID

### Избранное
- `GET /users/{id}/favorites` - Получить избранные треки пользователя