# code.py

import time
import sdcard # Mount SD card before audio accesses it.
import inputs
import hid_keyboard
import audio
import speaker

# ============================================================
# STARTUP
# ============================================================

print()
print("==============================")
print(" RINGDINGDONG")
print("==============================")
print()


# ============================================================
# ENCODER PRESS AUDIO
# ============================================================

def handle_encoder_press():

    # --------------------------------------------------------
    # Speaker mode
    # --------------------------------------------------------
    if speaker.is_speaker_mode():

        print("Speaker mode active.")
        audio.play_ringing_once() #Play ring.wav once
        
        print("Playing immediately.")
        audio.play_random() #Random audio play

        return

    # --------------------------------------------------------
    # Handset mode
    # --------------------------------------------------------
    else:
        
        if inputs.handset_lifted(): #Assume pressed when handset is lifted
            
            time.sleep(0.05)
            audio.play_random() #Random audio play
        
        else: #Handset resting
            
            print("Waiting for handset to be lifted...")
            
            speaker.set_speaker_output() #Enable speaker output
            speaker.start_ring_indicator() #Flash LED for ringing effect
            audio.start_ringing() #Play ring.wav

            while not inputs.handset_lifted(): #Check if handset lifted
                
                audio.update_ringing() #Loop ring.wav
                speaker.update_ring_indicator() #Continue flashing LED
                time.sleep(0.01)

            #When handset lifted
            audio.stop_ringing() #Stop ring.wav
            speaker.stop_ring_indicator() #Turn off speaker LED
            
            # Play pickup sound
            print("Playing pickup.wav...")
            audio.play_pickup() #Play pickup.wav
            
            time.sleep(0.05)
            
            speaker.set_handset_output() #Enable handset output

            print("HANDSET LIFTED")
            print("Playing audio...")

            time.sleep(0.05)
            
            audio.play_random()


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    events = inputs.update() #Check for inputs

    for event in events:

        # ====================================================
        # ENCODER
        # ====================================================

        if event[0] == "ENCODER":

            action = event[2]

            # ------------------------------------------------
            # Rotation
            # ------------------------------------------------

            if action == "TURN":

                digit = event[1]

                print("ENCODER DIGIT:",digit)
                hid_keyboard.send_digit(digit)

            # ------------------------------------------------
            # Encoder pressed
            # ------------------------------------------------

            elif action == "PRESS":

                handle_encoder_press()

        # ====================================================
        # NORMAL FUNCTION BUTTON
        # ====================================================

        elif event[0] == "FUNCTION":

            name = event[1]

            if name == "KEYPAD_ASTERISK":

                hid_keyboard.send_keypad_asterisk()

            else:

                hid_keyboard.send_function(name)

        # ====================================================
        # SPEAKER MODE
        # ====================================================

        elif event[0] == "SPEAKER":

            if event[1] == "TOGGLE":

                speaker.toggle()


    time.sleep(0.01)
