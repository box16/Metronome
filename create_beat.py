import numpy as np
from scipy.io import wavfile


def create_beat(frequency, file_name, duration=0.1, sample_rate=44100, amplitude=32767):
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = amplitude * np.sin(2 * np.pi * frequency * t)

    wavfile.write(file_name, sample_rate, wave.astype(np.int16))
