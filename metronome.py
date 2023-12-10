import tkinter as tk
from tkinter import messagebox
from pygame import mixer
import time
import threading
import sys
import os
import create_beat

ONE_MINUTE = 60
WINDOW_SIZE = "300x150"
BEAT_FILE = "beat.wav"
BEAT_HZ = 440
HEAD_BEAT_FILE = "head_beat.wav"
HEAD_BEAT_HZ = 880


class Metronome:
    def __init__(self):
        mixer.init()
        self.beat = mixer.Sound(self._beat_file_check(BEAT_HZ, BEAT_FILE))
        self.head_beat = mixer.Sound(
            self._beat_file_check(HEAD_BEAT_HZ, HEAD_BEAT_FILE)
        )
        self.is_playing = False

    def _beat_file_check(self, frequency, file_name):
        if getattr(sys, "frozen", False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        beat_path = os.path.join(application_path, file_name)

        if not os.path.exists(beat_path):
            create_beat.create_beat(frequency, beat_path)
        return beat_path

    def _start_metronome(self, bpm, beats):
        self.is_playing = True
        beat_duration = ONE_MINUTE / bpm

        while True:
            if not self.is_playing:
                break
            for beat in range(beats):
                if not self.is_playing:
                    break
                if beat == 0:
                    self.head_beat.play()
                else:
                    self.beat.play()
                time.sleep(beat_duration)

    def start_metronome(self, bpm, beats):
        if self.is_playing:
            self.stop_metronome()

        self.thread = threading.Thread(target=self._start_metronome, args=(bpm, beats))
        self.thread.start()

    def stop_metronome(self):
        self.is_playing = False
        if self.thread is not None:
            self.thread.join()
            self.thread = None


class MetronomeGUI:
    def __init__(self):
        self.metronome = Metronome()

        self.root = tk.Tk()
        self.root.geometry(WINDOW_SIZE)
        self.root.title("Metronome")

        tk.Label(self.root, text="BPM:").pack()
        self.bpm_entry = tk.Entry(self.root)
        self.bpm_entry.pack()

        tk.Label(self.root, text="Beats per measure:").pack()
        self.beats_entry = tk.Entry(self.root)
        self.beats_entry.pack()

        self.play_button = tk.Button(
            self.root, text="Play", command=self._start_metronome
        )
        self.play_button.pack()

        self.stop_button = tk.Button(
            self.root, text="Stop", command=self._stop_metronome
        )
        self.stop_button.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.delete_window)

    def _start_metronome(self):
        try:
            bpm = int(self.bpm_entry.get())
            beats = int(self.beats_entry.get())
            if (bpm <= 0) or (beats <= 0):
                raise ValueError("input error")

            self.metronome.start_metronome(bpm, beats)
        except Exception as e:
            messagebox.showwarning(f"{type(e).__name__}", f"{str(e)}")

    def _stop_metronome(self):
        self.metronome.stop_metronome()

    def start(self):
        self.root.mainloop()

    def delete_window(self):
        self._stop_metronome()
        self.root.destroy()


if __name__ == "__main__":
    app = MetronomeGUI()
    app.start()
