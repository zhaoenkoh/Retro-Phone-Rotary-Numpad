# speaker.py

import time
import digitalio

import config

# ============================================================
# MAX98357A ENABLE PINS
# ============================================================
speaker_amp = digitalio.DigitalInOut(config.SPEAKER_ENABLE_PIN)
speaker_amp.direction = digitalio.Direction.OUTPUT

handset_amp = digitalio.DigitalInOut(config.HANDSET_ENABLE_PIN)
handset_amp.direction = digitalio.Direction.OUTPUT

# ============================================================
# SPEAKER MODE LED
# ============================================================
led = digitalio.DigitalInOut(config.LED_PIN)
led.direction = digitalio.Direction.OUTPUT

# ============================================================
# STARTUP
# ============================================================

# Start in handset mode.
speaker_amp.value = False
handset_amp.value = True

led.value = False

RING_LED_INTERVAL = 0.5
ring_led_state = False
last_ring_led_toggle = 0.0

# ============================================================
# SPEAKER MODE
# ============================================================
speaker_mode = False

# ============================================================
# LED CONTROL
# ============================================================
def set_led(state):
    led.value = state


def start_ring_indicator():

    global ring_led_state
    global last_ring_led_toggle

    ring_led_state = False
    last_ring_led_toggle = time.monotonic()

    led.value = False


def update_ring_indicator():

    global ring_led_state
    global last_ring_led_toggle

    now = time.monotonic()

    if now - last_ring_led_toggle >= RING_LED_INTERVAL:

        last_ring_led_toggle = now
        ring_led_state = not ring_led_state
        led.value = ring_led_state


def stop_ring_indicator():

    global ring_led_state

    ring_led_state = False
    led.value = False
    
# ============================================================
# AUDIO OUTPUT SELECTION
# ============================================================

def set_handset_output():

    global speaker_mode

    speaker_mode = False
    speaker_amp.value = False # Turn speaker amplifier OFF first.

    time.sleep(0.05)

    handset_amp.value = True # Turn handset amplifier ON.
    led.value = False # LED OFF.


def set_speaker_output():

    global speaker_mode

    speaker_mode = True
    handset_amp.value = False # Turn handset amplifier OFF first.

    time.sleep(0.05)

    speaker_amp.value = True # Turn speaker amplifier ON.
    led.value = True # LED ON.


# ============================================================
# TOGGLE
# ============================================================

def toggle():

    if speaker_mode:
        
        print("SPEAKER MODE: OFF")
        set_handset_output()
        

    else:
        
        print("SPEAKER MODE: ON")
        set_speaker_output()
        

# ============================================================
# STATUS
# ============================================================
def is_speaker_mode():
    return speaker_mode


def is_handset_mode():
    return not speaker_mode

