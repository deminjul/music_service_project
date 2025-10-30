from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from database import engine, get_session
from models import *

app = FastAPI(
    title="Music Service API",
    description="API для музыкального сервиса",
    version="1.0.0"
)

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

# Корневой эндпоинт
@app.get("/")
def read_root():
    return {"message": "Music Service API", "version": "1.0.0"}

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)