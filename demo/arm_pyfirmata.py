import pyfirmata
import time
uno = pyfirmata.Arduino('/dev/ttyUSB_UNO')
mega = pyfirmata.ArduinoMega('/dev/ttyUSB_MEGA')

servo = dict()

servo[1] = uno.get_pin('d:5:s')
servo[2] = uno.get_pin('d:6:s')

servo[3] = mega.get_pin('d:8:s')
servo[4] = mega.get_pin('d:9:s')

n = 2

    
servo[n].write(70)
time.sleep(0.5)
servo[n].write(80)
time.sleep(0.5)
servo[n].write(90)
time.sleep(0.5)
servo[n].write(80)
time.sleep(0.5)
servo[n].write(70)
time.sleep(0.5)
    #servo[n].write(95)
    #time.sleep(0.5)
#    time.sleep(0.5)
#    servo[n].write(90)
#    time.sleep(0.5)
#    servo[n].write(45)
#    time.sleep(0.5)
#    servo[n].write(0)
#    time.sleep(0.5)
#    servo[n].write(45)
#    time.sleep(0.5)
#    servo[n].write(90)
#    time.sleep(0.5)
    
