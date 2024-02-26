import vlc
import time

# VLC Media Player'ın başlatılması
instance = vlc.Instance("--no-xlib")  # veya instance = vlc.Instance() (gerekli duruma bağlı olarak)
player = instance.media_player_new()

# Oynatılacak video dosyasının belirtilmesi
media = instance.media_new("../video/acilisVideo.mp4")
player.set_media(media)

# Pencere oluşturma
win = vlc.MediaPlayer()

# Video penceresini oluşturma
win.set_media(media)

# Pencereyi görünür hale getirme
win.set_hwnd(int(video_frame_id))

# Videoyu oynatma
player.play()

player.stop()
