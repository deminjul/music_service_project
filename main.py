from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from database import engine, get_session
from models import *
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime, timedelta

app = FastAPI(
    title="Music Service API",
    description="API для музыкального сервиса",
    version="1.0.0"
)

security = HTTPBasic()

# Базовые эндпоинты для артистов
@app.get("/artists/", response_model=List[Artist])
def get_artists(
    skip: int = 0, 
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Получить список всех артистов"""
    statement = select(Artist).offset(skip).limit(limit)
    artists = session.exec(statement).all()
    return artists

@app.get("/artists/{artist_id}", response_model=Artist)
def get_artist(artist_id: int, session: Session = Depends(get_session)):
    """Получить артиста по ID"""
    artist = session.get(Artist, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Артист не найден")
    return artist

# Эндпоинты для альбомов
@app.get("/albums/", response_model=List[Album])
def get_albums(
    skip: int = 0,
    limit: int = 100,
    artist_id: Optional[int] = Query(None, description="Фильтр по ID артиста"),
    session: Session = Depends(get_session)
):
    """Получить список альбомов"""
    statement = select(Album)
    if artist_id:
        statement = statement.where(Album.artist_id == artist_id)
    statement = statement.offset(skip).limit(limit)
    albums = session.exec(statement).all()
    return albums

@app.get("/albums/{album_id}", response_model=Album)
def get_album(album_id: int, session: Session = Depends(get_session)):
    """Получить альбом по ID"""
    album = session.get(Album, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Альбом не найден")
    return album

# Эндпоинты для треков
@app.get("/tracks/", response_model=List[Track])
def get_tracks(
    skip: int = 0,
    limit: int = 100,
    album_id: Optional[int] = Query(None, description="Фильтр по ID альбома"),
    artist_id: Optional[int] = Query(None, description="Фильтр по ID артиста"),
    session: Session = Depends(get_session)
):
    """Получить список треков"""
    statement = select(Track)
    if album_id:
        statement = statement.where(Track.album_id == album_id)
    if artist_id:
        statement = statement.where(Track.artist_id == artist_id)
    statement = statement.offset(skip).limit(limit)
    tracks = session.exec(statement).all()
    return tracks

@app.get("/tracks/{track_id}", response_model=Track)
def get_track(track_id: int, session: Session = Depends(get_session)):
    """Получить трек по ID"""
    track = session.get(Track, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Трек не найден")
    return track

# Эндпоинты для пользователей
@app.get("/users/", response_model=List[User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Получить список пользователей"""
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    """Получить пользователя по ID"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

# ЭНДПОИНТЫ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ
@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    """Создать нового пользователя (регистрация)"""
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: User, session: Session = Depends(get_session)):
    """Обновить данные пользователя"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Обновляем только переданные поля
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    
    session.commit()
    session.refresh(user)
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    """Удалить пользователя"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    session.delete(user)
    session.commit()
    return {"message": "Пользователь удален"}

@app.post("/login/")
def login(credentials: HTTPBasicCredentials = Depends(security), session: Session = Depends(get_session)):
    """Аутентификация пользователя"""
    user = session.exec(select(User).where(User.email == credentials.username)).first()
    if not user or user.password_hash != credentials.password:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    
    return {
        "message": "Успешный вход",
        "user_id": user.id,
        "username": user.username
    }

@app.post("/users/{user_id}/subscribe")
def subscribe_user(user_id: int, subscription_type: str = "monthly", session: Session = Depends(get_session)):
    """Активировать подписку пользователя"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    user.subscription_status = True
    user.subscription_expires_at = datetime.now() + timedelta(days=30)
    
    session.commit()
    return {"message": "Подписка активирована", "user_id": user_id, "subscription_type": subscription_type}

# Специальные эндпоинты
@app.get("/artists/{artist_id}/albums")
def get_artist_albums(artist_id: int, session: Session = Depends(get_session)):
    """Получить все альбомы артиста"""
    artist = session.get(Artist, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Артист не найден")
    
    statement = select(Album).where(Album.artist_id == artist_id)
    albums = session.exec(statement).all()
    return albums

@app.get("/albums/{album_id}/tracks")
def get_album_tracks(album_id: int, session: Session = Depends(get_session)):
    """Получить все треки альбома"""
    album = session.get(Album, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Альбом не найден")
    
    statement = select(Track).where(Track.album_id == album_id)
    tracks = session.exec(statement).all()
    return tracks

@app.get("/users/{user_id}/favorites")
def get_user_favorites(user_id: int, session: Session = Depends(get_session)):
    """Получить избранные треки пользователя"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    statement = select(Favorite).where(Favorite.user_id == user_id)
    favorites = session.exec(statement).all()
    
    # Получаем информацию о треках
    favorite_tracks = []
    for fav in favorites:
        track = session.get(Track, fav.track_id)
        if track:
            favorite_tracks.append(track)
    
    return favorite_tracks

# Корневой эндпоинт
@app.get("/")
def read_root():
    return {"message": "Music Service API", "version": "1.0.0"}

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)