from database import get_session
from models import *
from datetime import datetime, date, timedelta
from decimal import Decimal

def create_sample_data():
    with next(get_session()) as session:
        
        #  артисты
        blur = Artist(
            name="Blur", 
            bio="British rock band formed in London in 1988",
            verified=True,
            photo_url="https://example.com/blur.jpg"
        )
        
        radiohead = Artist(
            name="Radiohead", 
            bio="English rock band formed in Abingdon in 1985",
            verified=True,
            photo_url="https://example.com/radiohead.jpg"
        )
        
        session.add_all([blur, radiohead])
        session.commit()
        
        #  альбомы
        magic_whip = Album(
            title="The Magic Whip",
            artist_id=blur.id,
            release_year=2015,
            cover_url="https://example.com/magic_whip.jpg"
        )
        
        ok_computer = Album(
            title="OK Computer",
            artist_id=radiohead.id,
            release_year=1997,
            cover_url="https://example.com/ok_computer.jpg"
        )
        
        session.add_all([magic_whip, ok_computer])
        session.commit()
        
        # треки для Blur The Magic Whip
        go_out = Track(
            title="Go Out",
            album_id=magic_whip.id,
            artist_id=blur.id,
            duration=257,  # 4:17 в секундах
            file_url="https://example.com/music/blur_go_out.mp3",
            track_number=1
        )
        
        ghost_ship = Track(
            title="Ghost Ship",
            album_id=magic_whip.id,
            artist_id=blur.id,
            duration=289,  # 4:49 в секундах
            file_url="https://example.com/music/blur_ghost_ship.mp3",
            track_number=4
        )
        
        # треки для Radiohead - OK Computer
        let_down = Track(
            title="Let Down",
            album_id=ok_computer.id,
            artist_id=radiohead.id,
            duration=299,  # 4:59 в секундах
            file_url="https://example.com/music/radiohead_let_down.mp3",
            track_number=7
        )
        
        karma_police = Track(
            title="Karma Police",
            album_id=ok_computer.id,
            artist_id=radiohead.id,
            duration=262,  # 4:22 в секундах
            file_url="https://example.com/music/radiohead_karma_police.mp3",
            track_number=6
        )
        
        session.add_all([go_out, ghost_ship, let_down, karma_police])
        session.commit()
        
        # тестовый пользователь
        test_user = User(
            email="music.fan@example.com",
            password_hash="hashed_password_123",
            username="music_fan_95",
            birth_date=date(1995, 8, 20),
            country="Russia",
            subscription_status=True,
            subscription_expires_at=datetime.now() + timedelta(days=60),
            last_login_at=datetime.now()
        )
        
        session.add(test_user)
        session.commit()
        
        # добавляем треки в избранное
        favorite1 = Favorite(user_id=test_user.id, track_id=go_out.id)
        favorite2 = Favorite(user_id=test_user.id, track_id=karma_police.id)
        
        session.add_all([favorite1, favorite2])
        session.commit()
        
        # создаем плейлист
        playlist = Playlist(
            user_id=test_user.id,
            name="My Favorite Rock Songs",
            description="Best of Blur and Radiohead",
            cover_url="https://example.com/playlist_cover.jpg"
        )
        
        session.add(playlist)
        session.commit()
        
        # добавляем треки в плейлист
        playlist_track1 = PlaylistTrack(
            playlist_id=playlist.id,
            track_id=ghost_ship.id,
            added_by=test_user.id,
            position=1
        )
        
        playlist_track2 = PlaylistTrack(
            playlist_id=playlist.id,
            track_id=let_down.id,
            added_by=test_user.id,
            position=2
        )
        
        session.add_all([playlist_track1, playlist_track2])
        session.commit()
        
        # история прослушиваний
        history1 = ListeningHistory(
            user_id=test_user.id,
            track_id=go_out.id,
            listen_duration=200
        )
        
        history2 = ListeningHistory(
            user_id=test_user.id,
            track_id=karma_police.id,
            listen_duration=250
        )
        
        session.add_all([history1, history2])
        session.commit()
        
        # рекомендации
        recommendation = Recommendation(
            user_id=test_user.id,
            track_id=let_down.id,
            reason="based_on_history",
            score=Decimal('0.85')
        )
        
        session.add(recommendation)
        session.commit()
        

if __name__ == "__main__":
    create_sample_data()
