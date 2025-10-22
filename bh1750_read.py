# bh1750_min.py
import time
from smbus2 import SMBus

I2C_BUS = 1
ADDR = 0x23          # 0x5c if ADDR tied high
CMD_POWER_ON = 0x01
CMD_RESET = 0x07
CMD_CONT_HRES = 0x10 # Continuous high-res (1 lx resolution)

with SMBus(I2C_BUS) as bus:
    # power on & reset
    bus.write_byte(ADDR, CMD_POWER_ON)
    time.sleep(0.01)
    bus.write_byte(ADDR, CMD_RESET)
    time.sleep(0.01)
    # set mode
    bus.write_byte(ADDR, CMD_CONT_HRES)
    time.sleep(0.18)   # first conversion ~120–180ms

    while True:
        # read two bytes
        data = bus.read_i2c_block_data(ADDR, 0x00, 2)
        raw = (data[0] << 8) | data[1]
        # per datasheet: lx = raw / 1.2
        lux = raw / 1.2
        print(f"Ambient Light: {lux:.2f} lx")
        time.sleep(0.5)

