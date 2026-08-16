# inputs.py

import time
import digitalio

import config

# ============================================================
# ENCODERS
# ============================================================

encoder_inputs = []
encoder_last_state = []
encoder_moving = []
encoder_last_movement = []

for pin in config.ENCODER_PINS:

    gpio = digitalio.DigitalInOut(pin)
    gpio.direction = digitalio.Direction.INPUT
    gpio.pull = digitalio.Pull.UP

    encoder_inputs.append(gpio)
    encoder_last_state.append(gpio.value)

    encoder_moving.append(False)
    encoder_last_movement.append(0.0)

# ============================================================
# SHARED ENCODER SWITCH
# ============================================================

encoder_switch = digitalio.DigitalInOut(config.ENCODER_SWITCH_PIN)
encoder_switch.direction = digitalio.Direction.INPUT
encoder_switch.pull = digitalio.Pull.UP

last_encoder_switch = True

# ============================================================
# FUNCTION BUTTONS
# ============================================================

function_buttons = {}
last_function_buttons = {}

for name, pin in config.FUNCTION_BUTTON_PINS.items():

    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

    function_buttons[name] = button
    last_function_buttons[name] = True


# ============================================================
# HANDSET
# ============================================================

handset = digitalio.DigitalInOut(config.HANDSET_PIN)
handset.direction = digitalio.Direction.INPUT
handset.pull = digitalio.Pull.UP

# ============================================================
# GP27 SPECIAL BUTTON
# ============================================================

speaker_button = function_buttons["MULTIPLY"]

speaker_button_last_state = True
speaker_hold_start = None
speaker_hold_triggered = False

# ============================================================
# UPDATE
# ============================================================

def update():

    global last_encoder_switch
    global speaker_button_last_state
    global speaker_hold_start
    global speaker_hold_triggered

    events = []
    now = time.monotonic()

    # ========================================================
    # ENCODER ROTATION
    # ========================================================

    for index, encoder in enumerate(encoder_inputs):

        current = encoder.value
        previous = encoder_last_state[index]
        
        # ----------------------------------------------------
        # Falling edge
        # ----------------------------------------------------

        if previous and not current:

            encoder_moving[index] = True
            encoder_last_movement[index] = now

        encoder_last_state[index] = current

        # ----------------------------------------------------
        # Rotation stopped
        # ----------------------------------------------------

        if encoder_moving[index]:

            elapsed = (
                now
                - encoder_last_movement[index]
            )

            if elapsed >= config.ROTATION_TIMEOUT:

                encoder_moving[index] = False

                # Encoder 1 = digit 0
                # ...
                # Encoder 9 = digit 8
                # Encoder 10 = digit 9

                print("ENCODER", index + 1,"STOPPED")
                events.append(
                    (
                        "ENCODER",
                        index,
                        "TURN"
                    )
                )

    # ========================================================
    # ENCODER SWITCH
    # ========================================================

    current_switch = encoder_switch.value


    if (
        not current_switch
        and last_encoder_switch
    ):

        time.sleep(0.05)

        if not encoder_switch.value:

            print("ENCODER SWITCH PRESSED")
            events.append(
                (
                    "ENCODER",
                    0,
                    "PRESS"
                )
            )


    last_encoder_switch = current_switch

    # ========================================================
    # FUNCTION BUTTONS
    # ========================================================

    for name, button in function_buttons.items():

        # GP27 is handled separately below.
        if name == "MULTIPLY":
            continue

        state = button.value

        if (
            not state
            and last_function_buttons[name]
        ):

            time.sleep(0.05)

            if not button.value:

                print("FUNCTION:",name)
                events.append(
                    (
                        "FUNCTION",
                        name
                    )
                )


        last_function_buttons[name] = state


    # ========================================================
    # GP27
    #
    # Short press:
    #     KEYPAD ASTERISK
    #
    # Hold >= 3 seconds:
    #     Toggle speaker mode
    #
    # ========================================================

    current_speaker_button = speaker_button.value

    # --------------------------------------------------------
    # Pressed
    # --------------------------------------------------------

    if (
        speaker_button_last_state
        and not current_speaker_button
    ):

        speaker_hold_start = now
        speaker_hold_triggered = False

        print("GP27 PRESSED")

    # --------------------------------------------------------
    # Held
    # --------------------------------------------------------

    if (
        not current_speaker_button
        and speaker_hold_start is not None
        and not speaker_hold_triggered
    ):

        held_time = (
            now
            - speaker_hold_start
        )

        if held_time >= config.SPEAKER_MODE_HOLD_TIME:

            speaker_hold_triggered = True

            print("GP27 LONG HOLD")
            events.append(
                (
                    "SPEAKER",
                    "TOGGLE"
                )
            )

    # --------------------------------------------------------
    # Released
    # --------------------------------------------------------

    if (
        not speaker_button_last_state
        and current_speaker_button
    ):

        if (
            speaker_hold_start is not None
            and not speaker_hold_triggered
        ):

            print("GP27 SHORT PRESS")
            events.append(
                (
                    "FUNCTION",
                    "KEYPAD_ASTERISK"
                )
            )


        speaker_hold_start = None
        speaker_hold_triggered = False

    speaker_button_last_state = (
        current_speaker_button
    )

    return events


# ============================================================
# HANDSET STATE
# ============================================================

def handset_lifted():

    return handset.value