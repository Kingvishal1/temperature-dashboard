#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from datetime import datetime
import subprocess

# ------------------- CONFIG -------------------
PIR_INPUT = 11          # GPIO pin (BOARD mode)
CAPTURE_DELAY = 1       # seconds motion must persist
COOLDOWN = 5            # seconds before another capture
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_INPUT, GPIO.IN)
# ------------------------------------------------

# Detect which camera command is available
if subprocess.call(["which", "rpicam-still"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
    CAMERA_CMD = "rpicam-still"
elif subprocess.call(["which", "libcamera-still"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
    CAMERA_CMD = "libcamera-still"
else:
    raise RuntimeError("No rpicam-still or libcamera-still available. Install camera support first!")

print(f"Using camera command: {CAMERA_CMD}")

def capture_image():
    """Capture both JPEG and RAW images with a timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    jpeg_name = f"image_{timestamp}.jpeg"
    raw_name = f"image_{timestamp}.dng"

    print(f"[+] Capturing images: {jpeg_name} and RAW...")

    if CAMERA_CMD == "rpicam-still":
        subprocess.run([CAMERA_CMD, "-o", jpeg_name, "--raw", "-t", "200"])
    else:  # libcamera-still
        subprocess.run([CAMERA_CMD, "-o", jpeg_name, "-r", "-t", "2000"])
        raw_name = jpeg_name.replace(".jpeg", ".dng")

    print(f"[✓] Saved: {jpeg_name} and {raw_name}")

try:
    print("[*] Waiting for motion...")
    last_capture_time = 0

    while True:
        if GPIO.input(PIR_INPUT):  # Motion started
            print("Motion detected. Waiting 2 seconds to confirm...")

            start_time = time.time()
            time.sleep(CAPTURE_DELAY)  # Wait without constant checking

            if GPIO.input(PIR_INPUT):  # Confirm motion is still ongoing
                if time.time() - last_capture_time >= COOLDOWN:
                    capture_image()
                    last_capture_time = time.time()
                else:
                    print("Cooldown active, skipping capture.")
            else:
                print("Motion did not persist for full 2 seconds. Ignored.")
        else:
            print("No motion...")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nExiting program...")

finally:
    GPIO.cleanup()
