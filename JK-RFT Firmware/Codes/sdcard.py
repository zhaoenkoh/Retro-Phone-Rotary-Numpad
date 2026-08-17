# sdcard.py

import busio
import storage
import sdcardio

import config

# ============================================================
# SPI
# ============================================================

spi = busio.SPI(
    clock=config.SD_SCK,
    MOSI=config.SD_MOSI,
    MISO=config.SD_MISO
)


# ============================================================
# SD CARD
# ============================================================

sd = sdcardio.SDCard(
    spi,
    config.SD_CS,
    baudrate=8000000
)

# ============================================================
# FILESYSTEM
# ============================================================

vfs = storage.VfsFat(sd)

storage.mount(
    vfs,
    "/sd"
)

