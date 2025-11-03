# Примеры использования Music Service API


Базовая ссылка: `http://127.0.0.1:8000`

## 📋 Примеры запросов

### 1. Получить всех артистов
```http
GET /artists/
```
**Ответ:**
```json
[
  {
    "id": 1,
    "name": "Blur",
    "bio": "British rock band formed in London in 1988",
    "verified": true
  },
  {
    "id": 2, 
    "name": "Radiohead",
    "bio": "English rock band formed in Abingdon in 1985",
    "verified": true
  }
]
```

### 2. Получить альбомы артиста
```http
GET /albums/?artist_id=1
```
**Получите все альбомы Blur**

### 3. Получить треки альбома  
```http
GET /albums/1/tracks
```
**Получите все треки из альбома "The Magic Whip"**

### 4. Получить избранное пользователя
```http
GET /users/1/favorites
```
**Узнайте какие треки нравятся пользователю**

## 🛠 Примеры кода

### Использование с Python
```python
import requests

# Получить всех артистов
response = requests.get("http://127.0.0.1:8000/artists/")
artists = response.json()
print(f"Найдено артистов: {len(artists)}")

# Найти альбомы Blur
response = requests.get("http://127.0.0.1:8000/albums/?artist_id=1")
albums = response.json()
print(f"Альбомы Blur: {[album['title'] for album in albums]}")
```

### Использование с JavaScript
```javascript
// Получить все треки
fetch('http://127.0.0.1:8000/tracks/')
  .then(response => response.json())
  .then(tracks => {
    console.log('Все треки:', tracks);
  });
```

### Использование с curl
```bash
# Получить информацию о Radiohead
curl -X GET "http://127.0.0.1:8000/artists/2"

# Получить треки альбома OK Computer
curl -X GET "http://127.0.0.1:8000/albums/2/tracks"
```

## 💡 Сценарии использования

### Сценарий 1: Построение музыкального приложения
1. Показать список артистов (`GET /artists/`)
2. При выборе артиста показать его альбомы (`GET /artists/{id}/albums`)  
3. При выборе альбома показать треки (`GET /albums/{id}/tracks`)
4. Добавить трек в избранное (`POST /users/{id}/favorites/{track_id}`)

### Сценарий 2: Аналитика прослушиваний
1. Получить историю прослушиваний пользователя
2. Анализировать популярные треки
3. Строить рекомендации на основе предпочтений


##  эндпоинты для пользователей

### Регистрация пользователя
```http
POST /users/
Content-Type: application/json

{
  "email": "newuser@example.com",
  "password_hash": "secure_password",
  "username": "new_user"
}
```

### Обновление профиля
```http
PUT /users/1
Content-Type: application/json

{
  "username": "updated_username",
  "country": "USA"
}
```

### Аутентификация
```http
POST /login/
```
*Используйте Basic Auth в Swagger UI*