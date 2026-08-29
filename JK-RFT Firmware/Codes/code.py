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
# HANDSET EDGE DETECTION
# ============================================================

# inputs.handset_lifted() returns:
#
# False = handset resting
# True  = handset lifted
#
# The physical handset signal is assumed to be:
#
# HIGH = handset resting
# LOW  = handset lifted
#
# Therefore:
#
# False -> True
#
# is the negative edge of the physical signal.

previous_handset_state = inputs.handset_lifted()


# ============================================================
# ENCODER PRESS AUDIO
# ============================================================

def handle_encoder_press():

    # --------------------------------------------------------
    # Speaker mode
    # --------------------------------------------------------

    if speaker.is_speaker_mode():

        print("Speaker mode active.")

        audio.play_ringing_once() # Play ring.wav once

        print("Playing immediately.")

        audio.play_random() # Random audio play

        return


    # --------------------------------------------------------
    # Handset mode
    # --------------------------------------------------------

    else:

        if inputs.handset_lifted():

            # Handset is already lifted
            time.sleep(0.05)

            audio.play_random() # Random audio play

        else:

            # Handset is resting
            print("Waiting for handset to be lifted...")

            speaker.set_speaker_output() # Enable speaker output
            speaker.start_ring_indicator() # Flash LED for ringing effect
            audio.start_ringing() # Play ring.wav


            # ------------------------------------------------
            # Wait for handset to be lifted
            # ------------------------------------------------

            while not inputs.handset_lifted():

                audio.update_ringing()
                speaker.update_ring_indicator()

                time.sleep(0.01)


            # ------------------------------------------------
            # Handset lifted
            # ------------------------------------------------

            audio.stop_ringing()

            speaker.stop_ring_indicator()


            # ------------------------------------------------
            # Play pickup sound
            # ------------------------------------------------

            print("Playing pickup.wav...")

            audio.play_pickup()

            time.sleep(0.05)


            # ------------------------------------------------
            # Switch audio to handset
            # ------------------------------------------------

            speaker.set_handset_output()


            print("HANDSET LIFTED")
            print("Playing audio...")


            time.sleep(0.05)

            audio.play_random()


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    # ========================================================
    # UPDATE INPUTS
    # ========================================================

    events = inputs.update()


    # ========================================================
    # HANDSET NEGATIVE EDGE
    # ========================================================

    current_handset_state = inputs.handset_lifted()


    # Physical negative edge:
    #
    # Handset resting -> handset lifted
    #
    # False -> True in our logical function

    if previous_handset_state and not current_handset_state:

        print("HANDSET NEGATIVE EDGE")


        # ----------------------------------------------------
        # Only send ENTER when no audio/ringing operation
        # is currently being handled.
        #
        # IMPORTANT:
        # This assumes the main loop is only running while
        # the system is idle.
        # ----------------------------------------------------

        hid_keyboard.send_enter()
        
        
        


    # Save state for next loop

    previous_handset_state = current_handset_state


    # ========================================================
    # PROCESS INPUT EVENTS
    # ========================================================

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

                print("ENCODER DIGIT:", digit)

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


    # ========================================================
    # LOOP DELAY
    # ========================================================

    time.sleep(0.01)