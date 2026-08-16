# audio.py

import audiobusio
import audiocore
import audiomixer
import random
import os

import config

# ============================================================
# I2S
# ============================================================

audio = audiobusio.I2SOut(
    bit_clock=config.I2S_BCLK,
    word_select=config.I2S_LRC,
    data=config.I2S_DIN
)

# ============================================================
# MIXER
# ============================================================

mixer = audiomixer.Mixer(
    voice_count=1,
    sample_rate=48000,
    channel_count=2,
    bits_per_sample=16,
    samples_signed=True,
    buffer_size=2048
)


audio.play(mixer)

mixer.voice[0].level = config.VOLUME

ring_file = None
ring_wave = None
ringing = False


def start_ringing():
    global ring_file
    global ring_wave
    global ringing

    try:
        ring_file = open("/sd/ring.wav", "rb")
        ring_wave = audiocore.WaveFile(ring_file)

        ringing = True

        mixer.voice[0].play(ring_wave)

        print()
        print("==============================")
        print("RINGING")
        print("==============================")

    except Exception as e:
        print("RINGING ERROR:")
        print(e)

        ringing = False


def update_ringing():
    global ring_wave

    if not ringing:
        return

    # When one copy of ring.wav finishes,
    # immediately start it again.
    if not mixer.voice[0].playing:

        try:
            ring_file.seek(0)

            ring_wave = audiocore.WaveFile(
                ring_file
            )

            mixer.voice[0].play(ring_wave)

        except Exception as e:
            print("RING LOOP ERROR:")
            print(e)

            stop_ringing()


def stop_ringing():
    global ring_file
    global ring_wave
    global ringing

    ringing = False

    try:
        mixer.voice[0].stop()
    except Exception:
        pass

    if ring_file is not None:

        try:
            ring_file.close()
        except Exception:
            pass

    ring_file = None
    ring_wave = None

    print("RINGING STOPPED")


def play_ringing_once():
    play_sound("/sd/ring.wav")

def play_pickup():
    play_sound("/sd/pickup.wav")
# ============================================================
# FIND AUDIO FILES
# ============================================================

def find_wav_files():

    files = []

    try:
        for filename in os.listdir(
            config.AUDIO_DIRECTORY
        ):

            if filename.lower().endswith(".wav"):

                files.append(
                    config.AUDIO_DIRECTORY
                    + "/"
                    + filename
                )

    except Exception as e:
        print("Unable to read audio directory:", e)

    return files

wav_files = find_wav_files()

print("WAV FILES FOUND:",len(wav_files))
for filename in wav_files:
    print(" ",filename)


# ============================================================
# PLAY FILE
# ============================================================

def play_sound(filename):

    print()
    print("==============================")
    print("PLAYING")
    print("==============================")
    print(filename)

    try:
        with open(
            filename,
            "rb"
        ) as file:

            wave = audiocore.WaveFile(file)

#             print("Sample rate:",wave.sample_rate)
#             print("Bits:",wave.bits_per_sample)
#             print("Channels:",wave.channel_count)

            mixer.voice[0].play(wave)

            while mixer.voice[0].playing:

                import time
                time.sleep(0.01)

        print("PLAYBACK FINISHED")

    except Exception as e:

        print()
        print("==============================")
        print("AUDIO ERROR")
        print("==============================")
        print(e)
        print("==============================")


# ============================================================
# RANDOM AUDIO
# ============================================================

def play_random():

    if len(wav_files) == 0:
        print("No WAV files available.")
        return

    filename = random.choice(wav_files)
    play_sound(filename)
    
    