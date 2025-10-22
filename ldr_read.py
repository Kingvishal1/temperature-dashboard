#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PIN = 17               # your OUT/DO pin
SAMPLE_PERIOD = 0.01   # 10 ms between reads
STABLE_MS = 120        # require 120 ms stable before toggling

GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_OFF)  # try PUD_OFF first

last_raw = GPIO.input(PIN)
stable_since = time.monotonic()
state = last_raw  # debounced state we've announced

def report(val):
    print("Light state:", "DARK/TRIGGER (0)" if val == 0 else "BRIGHT/NOTRIGGER (1)")

report(state)
try:
    while True:
        raw = GPIO.input(PIN)
        now = time.monotonic()

        if raw != last_raw:
            # input flipped; restart stability timer
            stable_since = now
            last_raw = raw
        else:
            # unchanged; has it been stable long enough?
            if raw != state and (now - stable_since) >= (STABLE_MS / 1000.0):
                state = raw
                report(state)

        time.sleep(SAMPLE_PERIOD)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
