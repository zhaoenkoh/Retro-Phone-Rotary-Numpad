# config.py

import board


# ============================================================
# ENCODERS
# ============================================================

# One A-channel pin per encoder.
#
# Encoder number corresponds to the digit:
#
# Encoder 1  -> 1
# Encoder 2  -> 2
# ...
# Encoder 9  -> 9
# Encoder 10 -> 0

ENCODER_PINS = [
    board.GP6,    # Encoder 1
    board.GP7,    # Encoder 2
    board.GP8,    # Encoder 3
    board.GP9,    # Encoder 4
    board.GP10,   # Encoder 5
    board.GP11,   # Encoder 6
    board.GP12,   # Encoder 7
    board.GP13,   # Encoder 8
    board.GP14,   # Encoder 9
    board.GP15,   # Encoder 10
]


# All encoder push switches are connected together.
ENCODER_SWITCH_PIN = board.GP16


# ============================================================
# FUNCTION BUTTONS
# ============================================================

FUNCTION_BUTTON_PINS = {
    "PLUS": board.GP22,
    "MINUS": board.GP26,
    "MULTIPLY": board.GP27,
    "DIVIDE": board.GP28,
}


# ============================================================
# HANDSET
# ============================================================

HANDSET_PIN = board.GP0


# ============================================================
# SPEAKER MODE LED
# ============================================================

LED_PIN = board.GP1


# ============================================================
# MAX98357A
# ============================================================

# Speaker amplifier
SPEAKER_ENABLE_PIN = board.GP17

# Handset amplifier
HANDSET_ENABLE_PIN = board.GP18


# ============================================================
# I2S
# ============================================================

I2S_LRC = board.GP19
I2S_BCLK = board.GP20
I2S_DIN = board.GP21


# ============================================================
# MICROSD
# ============================================================

SD_SCK = board.GP2
SD_MOSI = board.GP3
SD_MISO = board.GP4
SD_CS = board.GP5


# ============================================================
# AUDIO
# ============================================================

AUDIO_DIRECTORY = "/sd/audio"

VOLUME = 0.2

SPEAKER_MODE_HOLD_TIME = 3.0

ROTATION_TIMEOUT = 0.3