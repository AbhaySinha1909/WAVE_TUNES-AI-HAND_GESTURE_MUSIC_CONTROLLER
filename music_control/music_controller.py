import pygame
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import os

class MusicController:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()

        # Playlist: add your songs here or scan a folder
        music_folder = r"C:\Users\1909a\Desktop\Wave_Tunes\AI-Hand-Music-Controller\music"
        self.playlist = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith(".mp3")]
        if not self.playlist:
            raise ValueError("No MP3 files found in the music folder!")

        self.current_index = 0
        self.is_playing = False
        self.is_paused = False

        # PyCaw for volume control
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.is_muted = False

        print(f"🎵 Playlist loaded: {len(self.playlist)} songs")

    # Music controls
    def play_music(self):
        if not self.is_playing:
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            print(f"▶️ Playing: {os.path.basename(self.playlist[self.current_index])}")
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            print(f"▶️ Resumed: {os.path.basename(self.playlist[self.current_index])}")

    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        print("🛑 Music Stopped")

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        pygame.mixer.music.load(self.playlist[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False
        print(f"⏭️ Next Track: {os.path.basename(self.playlist[self.current_index])}")

    def prev_track(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        pygame.mixer.music.load(self.playlist[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False
        print(f"⏮️ Previous Track: {os.path.basename(self.playlist[self.current_index])}")

    def volume_up(self):
        current = self.volume.GetMasterVolumeLevelScalar()
        self.volume.SetMasterVolumeLevelScalar(min(current + 0.05, 1.0), None)
        print("🔊 Volume Up")

    def volume_down(self):
        current = self.volume.GetMasterVolumeLevelScalar()
        self.volume.SetMasterVolumeLevelScalar(max(current - 0.05, 0.0), None)
        print("🔉 Volume Down")

    def mute_music(self):
        self.is_muted = not self.is_muted
        self.volume.SetMute(self.is_muted, None)
        print("🔇 Muted" if self.is_muted else "🔊 Unmuted")


# Quick test block
if __name__ == "__main__":
    music = MusicController()
    music.play_music()
    music.volume_up()
    music.volume_down()
    music.next_track()
    music.prev_track()
    music.mute_music()
    music.stop_music()
