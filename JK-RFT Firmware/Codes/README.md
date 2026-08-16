# Raspberry Pi Pico Retro Phone Rotary Numpad Project
# RINGDINGDONG
## Overview

CircuitPython is used in this project for a telephone-style Raspberry Pi Pico audio device.

Features:
- 10 rotary encoders mapped to digits 0–9
- Shared encoder push switch
- Handset detection
- Speaker mode
- Speaker-mode indicator LED
- Two MAX98357A I2S amplifiers
- Shared I2S bus with separate amplifier enable pins
- MicroSD WAV playback
- Looping incoming-call ringing
- Flashing LED while ringing
- `pickup.wav` when handset is lifted
- Random WAV playback
- USB HID keypad/function output
- USB storage disabled by `boot.py`

## Hardware Pin Configuration

### I2S

| Function | GPIO | Physical Pin |
|---|---:|---:|
| LRC / WS | GP19 | 25 |
| BCLK | GP20 | 26 |
| DIN | GP21 | 27 |

### MAX98357A Enable

| Function | GPIO | Physical Pin |
|---|---:|---:|
| Speaker MAX98357A #1 | GP17 | 22 |
| Handset MAX98357A #2 | GP18 | 24 |

Both amplifiers share LRC, BCLK and DIN. GP17/GP18 select the active amplifier.

### Buttons / Keypad

| Function | GPIO | Physical Pin |
|---|---:|---:|
| PLUS | GP22 | 29 |
| MINUS | GP26 | 31 |
| MULTIPLY | GP27 | 32 |
| DIVIDE | GP28 | 34 |
| HANDSET | GP0 | 1 |
| LED | GP1 | 2 |

`MULTIPLY` is also the speaker-mode toggle.

### Encoders

| Encoder | OUT A | GPIO | Physical Pin |
|---|---|---:|---:|
| Encoder 1 | A | GP6 | 9 |
| Encoder 2 | A | GP7 | 10 |
| Encoder 3 | A | GP8 | 11 |
| Encoder 4 | A | GP9 | 12 |
| Encoder 5 | A | GP10 | 14 |
| Encoder 6 | A | GP11 | 15 |
| Encoder 7 | A | GP12 | 16 |
| Encoder 8 | A | GP13 | 17 |
| Encoder 9 | A | GP14 | 19 |
| Encoder 10 | A | GP15 | 20 |

All encoder switches share GP16 (physical pin 21).

Encoder digit mapping is zero-based:

```text
Encoder 1  -> index 0 -> digit 0
Encoder 2  -> index 1 -> digit 1
Encoder 3  -> index 2 -> digit 2
Encoder 4  -> index 3 -> digit 3
Encoder 5  -> index 4 -> digit 4
Encoder 6  -> index 5 -> digit 5
Encoder 7  -> index 6 -> digit 6
Encoder 8  -> index 7 -> digit 7
Encoder 9  -> index 8 -> digit 8
Encoder 10 -> index 9 -> digit 9
```

### MicroSD

| Function | GPIO | Physical Pin |
|---|---:|---:|
| CS | GP5 | 7 |
| SCK | GP2 | 4 |
| MOSI | GP3 | 5 |
| MISO | GP4 | 6 |

SD SPI is currently configured for 8 MHz.

## Project Files

### `boot.py`

Runs before `code.py` and configures CircuitPython USB behavior. The project uses it to disable the CIRCUITPY USB storage drive.

This does not disable USB HID functionality and does not affect the MicroSD filesystem mounted at `/sd`.

### `code.py`

Main application coordinator.

Responsible for:
- polling input events
- handset state
- speaker mode
- ringing sequence
- amplifier selection requests
- pickup sound
- random audio playback
- HID event routing

It should contain high-level application logic rather than low-level hardware handling.

### `config.py`

Central hardware configuration.

Contains:
- GPIO assignments
- I2S pins
- amplifier enable pins
- encoder pins
- button pins
- handset pin
- LED pin
- SD SPI pins
- timing/configuration values

GPIO changes should normally be made here.

### `inputs.py`

Handles physical input.

Responsibilities:
- encoder scanning
- encoder index-to-digit mapping
- encoder push detection
- function buttons
- handset detection
- speaker-mode control
- input debouncing
- generation of standardized events

Example encoder event:

```text
ENCODER, 3, TURN
```

means encoder index 3 generated a rotation event.

### `hid_keyboard.py`

Converts application events into USB HID keyboard/keypad output.

The digit table follows the same zero-based mapping:

```text
index 0 -> Keycode.ZERO
index 1 -> Keycode.ONE
...
index 9 -> Keycode.NINE
```

Data path:

```text
Encoder
  ↓
inputs.py
  ↓
digit/index
  ↓
code.py
  ↓
hid_keyboard.py
  ↓
USB HID
```

### `speaker.py`

Controls:
- MAX98357A #1 / speaker output
- MAX98357A #2 / handset output
- GP1 indicator LED
- speaker-mode LED
- ringing LED flashing

Typical high-level functions include:

```python
speaker.set_speaker_output()
speaker.set_handset_output()
speaker.start_ring_indicator()
speaker.update_ring_indicator()
speaker.stop_ring_indicator()
```

The LED is kept in `speaker.py` because it represents output/amplifier state.

### `audio.py`

Handles:
- I2S output
- audio mixer
- WAV discovery
- random audio
- `ring.wav`
- ringing loop
- stopping ringing
- `pickup.wav`

Special sounds are outside the random audio directory.

## SD Card File Layout

```text
SD CARD/
├── ring.wav
├── pickup.wav
└── audio/
    ├── audio_01.wav
    ├── audio_02.wav
    ├── audio_03.wav
    └── ...
```

Special sounds:

```text
/sd/ring.wav
/sd/pickup.wav
```

Random audio:

```text
/sd/audio/*.wav
```

`ring.wav` and `pickup.wav` are deliberately outside `/sd/audio` so they are not selected as random content.

## Normal Handset Call Sequence

When an encoder is pressed:

```text
Encoder pressed
      ↓
Speaker MAX98357A selected
      ↓
ring.wav starts
      ↓
ring.wav loops
      ↓
GP1 flashes
      ↓
Wait for handset pickup
```

When the handset is lifted:

```text
Handset lifted
      ↓
Stop ring.wav
      ↓
Stop flashing LED
      ↓
Select handset MAX98357A
      ↓
pickup.wav
      ↓
Random audio
```

`pickup.wav` only plays in normal handset mode.

## Speaker Mode

Speaker mode is toggled using the configured `MULTIPLY` control.

When speaker mode is active:

```text
Speaker amplifier enabled
LED ON steadily
```

When an encoder event triggers playback:

```text
ring.wav once
      ↓
random audio
```

`pickup.wav` is not played in speaker mode.

## Ringing LED

During normal handset ringing, GP1 flashes without blocking the input loop.

Typical sequence:

```text
ON → OFF → ON → OFF → ...
```

When the handset is lifted:

```text
ringing stops
LED turns OFF
handset amplifier selected
```

Speaker mode uses a steady LED rather than the ringing flash.

## Audio Amplifier Architecture

Both MAX98357A boards share:

```text
GP19 -> LRC
GP20 -> BCLK
GP21 -> DIN
```

Enable controls:

```text
GP17 -> Speaker MAX98357A
GP18 -> Handset MAX98357A
```

Only the intended amplifier should normally be enabled.

The current design does not depend on a particular L/R/mono channel mode because the audio content is intended to be the same on either output.

## MicroSD and CIRCUITPY Filesystems

The Pico's internal CircuitPython filesystem and the MicroSD filesystem are separate:

```text
CIRCUITPY
```

versus:

```text
/sd
```

A folder named `sd` inside CIRCUITPY does not represent the physical SD card.

The physical card is explicitly mounted using the SD driver at:

```text
/sd
```

## USB Storage

`boot.py` disables the CIRCUITPY mass-storage device.

Therefore the Pico may no longer appear as a normal CIRCUITPY drive in Windows Explorer.

This is intentional.

USB HID and USB mass storage are separate functions. The project can still use HID keyboard output while USB storage is disabled.

An empty `settings.toml` is acceptable if no other project settings are required there and `boot.py` does not depend on values from it.


## Module Communication

Overall architecture:

```text
                 HARDWARE
                    │
                    ▼
              ┌───────────┐
              │ inputs.py │
              └─────┬─────┘
                    │ events
                    ▼
              ┌───────────┐
              │  code.py  │
              │ main logic│
              └───┬───┬───┘
                  │   │
          ┌───────┘   └────────┐
          ▼                    ▼
   ┌────────────┐       ┌───────────────┐
   │ speaker.py │       │hid_keyboard.py│
   │ amp + LED  │       │ USB HID       │
   └──────┬─────┘       └───────────────┘
          │
          ▼
   ┌────────────┐
   │  audio.py  │
   │ WAV + I2S  │
   └──────┬─────┘
          │
          ▼
     MAX98357A
```


## Quick Pin Reference

```text
I2S
GP19 = LRC
GP20 = BCLK
GP21 = DIN

AMPLIFIER ENABLE (SD_MODE)
GP17 = Speaker MAX98357A
GP18 = Handset MAX98357A

BUTTONS
GP22 = PLUS
GP26 = MINUS
GP27 = MULTIPLY
GP28 = DIVIDE

HANDSET / LED
GP0 = Handset
GP1 = LED

ENCODERS
GP6  = Encoder 1
GP7  = Encoder 2
GP8  = Encoder 3
GP9  = Encoder 4
GP10 = Encoder 5
GP11 = Encoder 6
GP12 = Encoder 7
GP13 = Encoder 8
GP14 = Encoder 9
GP15 = Encoder 10
GP16 = Shared encoder switches

SD
GP2 = SCK
GP3 = MOSI
GP4 = MISO
GP5 = CS
```
