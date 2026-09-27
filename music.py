import pygame
import array
import math
import numpy as np

_sample_rate = 22050

NOTES = {
    'C3': 130.81, 'C#3': 138.59, 'D3': 146.83, 'D#3': 155.56, 'E3': 164.81,
    'F3': 174.61, 'F#3': 185.00, 'G3': 196.00, 'G#3': 207.65, 'A3': 220.00,
    'A#3': 233.08, 'B3': 246.94,
    'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13, 'E4': 329.63,
    'F4': 349.23, 'F#4': 369.99, 'G4': 392.00, 'G#4': 415.30, 'A4': 440.00,
    'A#4': 466.16, 'B4': 493.88,
    'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25, 'E5': 659.25,
    'F5': 698.46, 'F#5': 739.99, 'G5': 783.99, 'G#5': 830.61, 'A5': 880.00,
    'A#5': 932.33, 'B5': 987.77,
    'C6': 1046.50, 'C#6': 1108.73, 'D6': 1174.66, 'D#6': 1244.51, 'E6': 1318.51,
    'F6': 1396.91, 'F#6': 1479.98, 'G6': 1567.98, 'G#6': 1661.22, 'A6': 1760.00,
    'B6': 1975.53,
}


def _freq(name):
    return NOTES.get(name, 440.0)


def _generate_wave(freq, duration, volume=0.15, wave_type='sine'):
    n = int(_sample_rate * duration)
    if n == 0:
        return None
    samples = array.array('h', [0]) * n
    two_pi = 2 * math.pi
    for i in range(n):
        t = i / _sample_rate
        if wave_type == 'piano':
            val = (math.sin(two_pi * freq * t)
                   + 0.5 * math.sin(two_pi * freq * 2 * t)
                   + 0.25 * math.sin(two_pi * freq * 3 * t))
            attack = min(1.0, i / (n * 0.02 + 1))
            env = attack * math.exp(-5.0 * i / n)
        elif wave_type == 'bell':
            val = (math.sin(two_pi * freq * t)
                   + 0.4 * math.sin(two_pi * freq * 2.0 * t)
                   + 0.2 * math.sin(two_pi * freq * 3.0 * t))
            attack = min(1.0, i / (n * 0.05 + 1))
            env = attack * math.exp(-3.2 * i / n)
        elif wave_type == 'string':
            tri = 2 * abs(2 * (freq * t - math.floor(freq * t + 0.5))) - 1
            val = tri * 0.6 + math.sin(two_pi * freq * t) * 0.4
            attack = min(1.0, i / (n * 0.15 + 1))
            env = attack * (0.35 + 0.65 * math.exp(-2.4 * i / n))
        elif wave_type == 'soft':
            val = math.sin(two_pi * freq * t) * 0.7 + math.sin(two_pi * freq * 2 * t) * 0.3
            fade = 0.05
            if i < n * fade:
                env = i / (n * fade)
            elif i > n * (1 - fade):
                env = (n - i) / (n * fade)
            else:
                env = 1.0
        else:
            val = math.sin(two_pi * freq * t)
            fade = 0.05
            if i < n * fade:
                env = i / (n * fade)
            elif i > n * (1 - fade):
                env = (n - i) / (n * fade)
            else:
                env = 1.0
        sample_val = int(volume * 32767 * val * env)
        samples[i] = max(-32768, min(32767, sample_val))
    return samples


def _build_sound(track):
    wave = track.get('wave', 'soft')
    vol = track.get('volume', 0.12)
    tempo = track.get('tempo', 1.0)
    chord_vol = track.get('chord_volume', 0.04)
    notes = track['notes']
    chords = track['chords']

    buffer = None
    for note, dur in notes:
        d = dur * tempo
        if note == '-':
            rest = array.array('h', [0]) * int(_sample_rate * d)
            buffer = rest if buffer is None else buffer + rest
            continue
        w = _generate_wave(_freq(note), d, vol, wave)
        if w is None:
            continue
        buffer = w if buffer is None else buffer + w
    if buffer is None:
        buffer = array.array('h', [0]) * _sample_rate

    n_chords = len(chords)
    chord_len = len(buffer) // n_chords if n_chords else 0
    for ci in range(n_chords):
        start = ci * chord_len
        end = min(start + chord_len, len(buffer))
        if start >= end:
            break
        for cfreq_name in chords[ci]:
            cfreq = _freq(cfreq_name)
            for i in range(start, end):
                t = (i - start) / _sample_rate
                val = math.sin(2 * math.pi * cfreq * t) * chord_vol
                existing = buffer[i]
                buffer[i] = max(-32768, min(32767, existing + int(val * 32767)))

    stereo = np.array(buffer, dtype=np.int16).reshape(-1, 1)
    stereo = np.repeat(stereo, 2, axis=1)
    return pygame.sndarray.make_sound(stereo)


# --- Track definitions (public-domain classical melodies) ---------------

TRACKS = {
    'fresa': {
        'name': 'Fresa Dreams',
        'wave': 'soft',
        'volume': 0.12,
        'tempo': 1.0,
        'chords': [('C4', 'E4', 'G4'), ('G3', 'B3', 'D4'), ('A3', 'C4', 'E4'),
                   ('F3', 'A3', 'C4'), ('C4', 'E4', 'G4')],
        'notes': [
            ('E5', 0.3), ('G5', 0.3), ('A5', 0.3), ('G5', 0.3),
            ('E5', 0.3), ('D5', 0.3), ('C5', 0.3), ('D5', 0.3),
            ('E5', 0.3), ('G5', 0.3), ('A5', 0.6), ('G5', 0.3),
            ('E5', 0.3), ('D5', 0.3), ('C5', 0.6), ('-', 0.3),
            ('G4', 0.3), ('A4', 0.3), ('C5', 0.3), ('E5', 0.3),
            ('D5', 0.3), ('C5', 0.3), ('A4', 0.3), ('G4', 0.3),
            ('A4', 0.3), ('C5', 0.3), ('E5', 0.6), ('D5', 0.3),
            ('C5', 0.3), ('A4', 0.3), ('G4', 0.6), ('-', 0.3),
            ('C5', 0.2), ('E5', 0.2), ('G5', 0.2), ('A5', 0.2),
            ('G5', 0.2), ('E5', 0.2), ('D5', 0.2), ('C5', 0.2),
            ('D5', 0.2), ('E5', 0.2), ('C5', 0.2), ('D5', 0.2),
            ('E5', 0.3), ('C5', 0.3), ('D5', 0.3), ('E5', 0.3),
            ('G5', 0.4), ('E5', 0.4), ('C5', 0.4), ('D5', 0.4),
            ('E5', 0.6), ('C5', 0.6), ('-', 0.4),
        ],
    },
    'ode': {
        'name': 'Oda a la Alegr\u00eda',
        'wave': 'soft',
        'volume': 0.12,
        'tempo': 1.0,
        'chords': [('C4', 'E4', 'G4'), ('F4', 'A4', 'C5'),
                   ('C4', 'E4', 'G4'), ('G4', 'B4', 'D5')],
        'notes': [
            ('E4', 0.25), ('E4', 0.25), ('F4', 0.25), ('G4', 0.25),
            ('G4', 0.25), ('F4', 0.25), ('E4', 0.25), ('D4', 0.25),
            ('C4', 0.25), ('C4', 0.25), ('D4', 0.25), ('E4', 0.25),
            ('E4', 0.25), ('D4', 0.25), ('D4', 0.5),
            ('E4', 0.25), ('E4', 0.25), ('F4', 0.25), ('G4', 0.25),
            ('G4', 0.25), ('F4', 0.25), ('E4', 0.25), ('D4', 0.25),
            ('C4', 0.25), ('C4', 0.25), ('D4', 0.25), ('E4', 0.25),
            ('D4', 0.25), ('C4', 0.25), ('C4', 0.5),
            ('D4', 0.25), ('D4', 0.25), ('E4', 0.25), ('C4', 0.25),
            ('D4', 0.25), ('E4', 0.25), ('F4', 0.25), ('E4', 0.25),
            ('C4', 0.25), ('D4', 0.25), ('E4', 0.25), ('F4', 0.25),
            ('E4', 0.25), ('D4', 0.25), ('C4', 0.25), ('D4', 0.5),
        ],
    },
    'elise': {
        'name': 'Para Elisa',
        'wave': 'piano',
        'volume': 0.13,
        'tempo': 0.95,
        'chord_volume': 0.035,
        'chords': [('A3', 'C4', 'E4'), ('A3', 'C4', 'E4'), ('E4', 'G#4', 'B4'),
                   ('A3', 'C4', 'E4'), ('A3', 'C4', 'E4'), ('E4', 'G#4', 'B4')],
        'notes': [
            ('E5', 0.25), ('D#5', 0.25), ('E5', 0.25), ('D#5', 0.25),
            ('E5', 0.25), ('B4', 0.25), ('D5', 0.25), ('C5', 0.25), ('A4', 1.0),
            ('C4', 0.25), ('E4', 0.25), ('A4', 0.25), ('B4', 1.0),
            ('E4', 0.25), ('G#4', 0.25), ('B4', 0.25), ('C5', 1.0),
            ('E4', 0.25), ('E5', 0.25), ('D#5', 0.25), ('E5', 0.25),
            ('D#5', 0.25), ('E5', 0.25), ('B4', 0.25), ('D5', 0.25),
            ('C5', 0.25), ('A4', 1.0),
            ('C4', 0.25), ('E4', 0.25), ('A4', 0.25), ('B4', 1.0),
            ('E4', 0.25), ('C5', 0.25), ('B4', 0.25), ('A4', 1.0),
        ],
    },
    'canon': {
        'name': 'Canon en Re',
        'wave': 'string',
        'volume': 0.11,
        'tempo': 0.9,
        'chord_volume': 0.03,
        'chords': [('D4', 'F#4', 'A4'), ('A3', 'C#4', 'E4'), ('B3', 'D4', 'F#4'),
                   ('F#3', 'A3', 'C#4'), ('G3', 'B3', 'D4'), ('D4', 'F#4', 'A4'),
                   ('G3', 'B3', 'D4'), ('A3', 'C#4', 'E4')],
        'notes': [
            ('D5', 0.25), ('F#5', 0.25), ('A5', 0.25), ('F#5', 0.25),
            ('A5', 0.25), ('G5', 0.25), ('F#5', 0.25), ('E5', 0.25),
            ('D5', 0.25), ('C#5', 0.25), ('B4', 0.25), ('A4', 0.25),
            ('B4', 0.25), ('A4', 0.25), ('G4', 0.25), ('F#4', 0.25),
            ('G4', 0.25), ('B4', 0.25), ('D5', 0.25), ('B4', 0.25),
            ('G4', 0.25), ('A4', 0.25), ('B4', 0.25), ('C#5', 0.25),
            ('D5', 0.25), ('B4', 0.25), ('G4', 0.25), ('B4', 0.25),
            ('A4', 0.25), ('C#4', 0.25), ('E4', 0.25), ('A4', 0.25),
        ],
    },
    'moon': {
        'name': 'Claro de Luna',
        'wave': 'bell',
        'volume': 0.12,
        'tempo': 1.4,
        'chord_volume': 0.03,
        'chords': [('A3', 'C4', 'E4'), ('F3', 'A3', 'C4'),
                   ('C4', 'E4', 'G4'), ('G3', 'B3', 'D4')],
        'notes': [
            ('C5', 0.25), ('E5', 0.25), ('A5', 0.25), ('E5', 0.25),
            ('C5', 0.25), ('F5', 0.25), ('A5', 0.25), ('F5', 0.25),
            ('C5', 0.25), ('E5', 0.25), ('G5', 0.25), ('E5', 0.25),
            ('B4', 0.25), ('D5', 0.25), ('G5', 0.25), ('D5', 0.25),
            ('C5', 0.25), ('E5', 0.25), ('A5', 0.25), ('E5', 0.25),
            ('F5', 0.25), ('A5', 0.25), ('C6', 0.25), ('A5', 0.25),
            ('E5', 0.25), ('G5', 0.25), ('C6', 0.25), ('G5', 0.25),
            ('D5', 0.25), ('G5', 0.25), ('B5', 0.25), ('G5', 0.25),
        ],
    },
    'spring': {
        'name': 'La Primavera',
        'wave': 'string',
        'volume': 0.09,
        'tempo': 0.7,
        'chord_volume': 0.03,
        'chords': [('A4', 'C#5', 'E5'), ('D4', 'F#4', 'A4'),
                   ('A4', 'C#5', 'E5'), ('E4', 'G#4', 'B4')],
        'notes': [
            ('A5', 0.125), ('B5', 0.125), ('C#6', 0.125), ('D6', 0.125),
            ('E6', 0.125), ('D6', 0.125), ('C#6', 0.125), ('B5', 0.125),
            ('A5', 0.125), ('B5', 0.125), ('C#6', 0.125), ('D6', 0.125),
            ('E6', 0.125), ('D6', 0.125), ('C#6', 0.125), ('B5', 0.125),
            ('A5', 0.25), ('E5', 0.25), ('A5', 0.25), ('B5', 0.25),
            ('C#6', 0.25), ('B5', 0.25), ('A5', 0.25), ('G#5', 0.25),
            ('A5', 0.25), ('B5', 0.25), ('C#6', 0.25), ('D6', 0.25),
            ('E6', 0.5), ('E5', 0.5),
        ],
    },
}


class MusicGenerator:
    def __init__(self):
        self.channel = None
        self.playing = False
        self.track = 'fresa'
        self._last_track = None
        self.volume = 0.7
        self._cache = {}

    def get_tracks(self):
        return list(TRACKS.keys())

    def track_name(self, key):
        track = TRACKS.get(key, TRACKS['fresa'])
        return track['name']

    def _build_track(self, key):
        if key not in self._cache:
            self._cache[key] = _build_sound(TRACKS[key])
        return self._cache[key]

    def start_music(self, key=None):
        if key:
            self.track = key
        if self.track not in TRACKS:
            self.track = 'fresa'
        if self.playing and self._last_track == self.track:
            return
        sound = self._build_track(self.track)
        channel = _music_channel()
        if self.channel:
            self.channel.stop()
        self.channel = channel
        channel.play(sound, -1)
        channel.set_volume(self.volume)
        self.playing = True
        self._last_track = self.track

    def select_track(self, key):
        if key not in TRACKS:
            return
        if key == self.track and self.playing:
            return
        self.track = key
        self._last_track = None
        self.start_music()

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        if self.channel and self.playing:
            self.channel.set_volume(self.volume)

    def stop_music(self):
        if self.channel:
            self.channel.stop()
            self.channel = None
        self.playing = False
        self._last_track = None

    def pause_music(self):
        if self.channel:
            self.channel.pause()

    def unpause_music(self):
        if self.channel:
            self.channel.unpause()


music_gen = MusicGenerator()


# --- Sound effects (soft, generated) -----------------------------------

def _sweep(f0, f1, duration, volume=0.15):
    n = int(_sample_rate * duration)
    if n == 0:
        return None
    samples = array.array('h', [0]) * n
    two_pi = 2 * math.pi
    for i in range(n):
        t = i / n
        freq = f0 + (f1 - f0) * t
        val = math.sin(two_pi * freq * (i / _sample_rate))
        fade = 0.15
        if i < n * fade:
            env = i / (n * fade)
        elif i > n * (1 - fade):
            env = (n - i) / (n * fade)
        else:
            env = 1.0
        samples[i] = max(-32768, min(32767, int(volume * 32767 * val * env)))
    return samples


def _sfx_to_stereo(buffer):
    arr = np.array(buffer, dtype=np.int16).reshape(-1, 1)
    arr = np.repeat(arr, 2, axis=1)
    return pygame.sndarray.make_sound(arr)


_SFX = {}
_channels_ready = False
_music_ch = None


def _music_channel():
    global _channels_ready, _music_ch
    if not _channels_ready:
        pygame.mixer.set_reserved(2)
        _channels_ready = True
    if _music_ch is None:
        _music_ch = pygame.mixer.Channel(1)
    return _music_ch


def _sfx_channel():
    global _channels_ready
    if not _channels_ready:
        pygame.mixer.set_reserved(2)
        _channels_ready = True
    channel = pygame.mixer.Channel(0)
    channel.set_volume(1.0)
    return channel


def _build_sfx(name):
    if name == 'jump':
        buffer = _sweep(430, 760, 0.10, 0.14)
        tail = _sweep(760, 1120, 0.06, 0.09)
        if buffer is not None and tail is not None:
            buffer = buffer + tail
    elif name == 'hurt':
        buffer = _sweep(820, 500, 0.08, 0.28)
        body = _sweep(520, 260, 0.55, 0.16)
        tail = _sweep(280, 180, 0.35, 0.12)
        if buffer is not None and body is not None:
            buffer = buffer + body
        if buffer is not None and tail is not None:
            buffer = buffer + tail
    elif name == 'stomp':
        buffer = _sweep(620, 260, 0.10, 0.20)
        tail = _sweep(180, 60, 0.14, 0.12)
        if buffer is not None and tail is not None:
            buffer = buffer + tail
    else:
        buffer = array.array('h', [0]) * int(_sample_rate * 0.05)
    if buffer is None:
        return None
    return _sfx_to_stereo(buffer)


def get_sfx(name):
    if name not in _SFX:
        _SFX[name] = _build_sfx(name)
    return _SFX[name]


def play_sfx(name):
    sound = get_sfx(name)
    if sound is None:
        return
    _sfx_channel().play(sound)
