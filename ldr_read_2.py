from  gpiozero import LightSensor
ldr = LightSensor(11)
while True:
          print (ldr.value)
