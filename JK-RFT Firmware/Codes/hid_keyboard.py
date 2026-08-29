# hid_keyboard.py

import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


# ============================================================
# KEYBOARD
# ============================================================

keyboard = Keyboard(usb_hid.devices)

# ============================================================
# DIGITS
# ============================================================

digit_keys = [

    Keycode.ZERO,       # 0
    Keycode.ONE,        # 1
    Keycode.TWO,        # 2
    Keycode.THREE,      # 3
    Keycode.FOUR,       # 4
    Keycode.FIVE,       # 5
    Keycode.SIX,        # 6
    Keycode.SEVEN,      # 7
    Keycode.EIGHT,      # 8
    Keycode.NINE,       # 9

]

# ============================================================
# FUNCTION KEYS
# ============================================================

function_keys = {

    "PLUS": Keycode.KEYPAD_PLUS,
    "MINUS": Keycode.KEYPAD_MINUS,
    "MULTIPLY": Keycode.KEYPAD_ASTERISK,
    "DIVIDE": Keycode.KEYPAD_FORWARD_SLASH,

}


# ============================================================
# SEND DIGIT
# ============================================================

def send_digit(number):

    keyboard.press(
        digit_keys[number]
    )

    keyboard.release_all()


# ============================================================
# SEND FUNCTION
# ============================================================

def send_function(name):

    if name not in function_keys:
        print("Unknown function:",name)
        return

    keyboard.press(
        function_keys[name]
    )
    
    keyboard.release_all()


# ============================================================
# SEND KEYPAD ASTERISK
# ============================================================

def send_keypad_asterisk():

    keyboard.press(
        Keycode.KEYPAD_ASTERISK
    )

    keyboard.release_all()
    
#send enter
    
def send_enter():

    keyboard.press(
        Keycode.ENTER
    )

    keyboard.release_all()