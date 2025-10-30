from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal

# Базовые модели
class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    username: Optional[str] = Field(default=None, unique=True)
    birth_date: Optional[date] = Field(default=None)
    country: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    subscription_status: bool = Field(default=False)
    subscription_expires_at: Optional[datetime] = Field(default=None)
    last_login_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    playlists: List["Playlist"] = Relationship(back_populates="user")
    favorites: List["Favorite"] = Relationship(back_populates="user")
    listening_history: List["ListeningHistory"] = Relationship(back_populates="user")
    payments: List["Payment"] = Relationship(back_populates="user")
    recommendations: List["Recommendation"] = Relationship(back_populates="user")


class Artist(SQLModel, table=True):
    __tablename__ = "artists"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    bio: Optional[str] = Field(default=None)
    photo_url: Optional[str] = Field(default=None)
    verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships
    albums: List["Album"] = Relationship(back_populates="artist")
    tracks: List["Track"] = Relationship(back_populates="artist")


class Album(SQLModel, table=True):
    __tablename__ = "albums"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    artist_id: int = Field(foreign_key="artists.id", nullable=False)
    release_year: Optional[int] = Field(default=None)
    cover_url: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships
    artist: Artist = Relationship(back_populates="albums")
    tracks: List["Track"] = Relationship(back_populates="album")


class Track(SQLModel, table=True):
    __tablename__ = "tracks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    album_id: int = Field(foreign_key="albums.id", nullable=False)
    artist_id: int = Field(foreign_key="artists.id", nullable=False)
    duration: int = Field(nullable=False)  # в секундах
    file_url: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    track_number: Optional[int] = Field(default=None)
    
    # Relationships
    album: Album = Relationship(back_populates="tracks")
    artist: Artist = Relationship(back_populates="tracks")
    playlist_tracks: List["PlaylistTrack"] = Relationship(back_populates="track")
    favorites: List["Favorite"] = Relationship(back_populates="track")
    listening_history: List["ListeningHistory"] = Relationship(back_populates="track")
    recommendations: List["Recommendation"] = Relationship(back_populates="track")


class Playlist(SQLModel, table=True):
    __tablename__ = "playlists"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    cover_url: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships
    user: User = Relationship(back_populates="playlists")
    playlist_tracks: List["PlaylistTrack"] = Relationship(back_populates="playlist")


class PlaylistTrack(SQLModel, table=True):
    __tablename__ = "playlist_tracks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    playlist_id: int = Field(foreign_key="playlists.id", nullable=False)
    track_id: int = Field(foreign_key="tracks.id", nullable=False)
    added_at: datetime = Field(default_factory=datetime.now)
    added_by: int = Field(foreign_key="users.id", nullable=False)
    position: Optional[int] = Field(default=None)
    
    # Relationships
    playlist: Playlist = Relationship(back_populates="playlist_tracks")
    track: Track = Relationship(back_populates="playlist_tracks")


class Favorite(SQLModel, table=True):
    __tablename__ = "favorites"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    track_id: int = Field(foreign_key="tracks.id", nullable=False)
    added_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships
    user: User = Relationship(back_populates="favorites")
    track: Track = Relationship(back_populates="favorites")


class ListeningHistory(SQLModel, table=True):
    __tablename__ = "listening_history"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    track_id: int = Field(foreign_key="tracks.id", nullable=False)
    listened_at: datetime = Field(default_factory=datetime.now)
    listen_duration: int  # в секундах
    
    # Relationships
    user: User = Relationship(back_populates="listening_history")
    track: Track = Relationship(back_populates="listening_history")


class Payment(SQLModel, table=True):
    __tablename__ = "payments"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    amount: Decimal = Field(nullable=False)
    currency: str = Field(default="RUB")
    status: str = Field(nullable=False)  # 'pending', 'completed', 'failed', 'refunded'
    payment_system_id: Optional[str] = Field(default=None)
    subscription_type: str  # 'monthly', 'yearly', 'premium'
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships
    user: User = Relationship(back_populates="payments")


class Recommendation(SQLModel, table=True):
    __tablename__ = "recommendations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    track_id: int = Field(foreign_key="tracks.id", nullable=False)
    reason: str  # 'similar_artists', 'popular', 'based_on_history'
    score: Decimal  # вес рекомендации (0-1)
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships
    user: User = Relationship(back_populates="recommendations")
    track: Track = Relationship(back_populates="recommendations")