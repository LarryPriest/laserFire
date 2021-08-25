# LaserFire.py
'''Written by Larry T, Priest (priestlt@protonmail.com)
August 2021
hardware:
    Raspberry pico, 16 LED's
Project goal:
    simulate laser canon fire, to be included in the K-9 and supercomputer
    projects.
Software:
    CircuitPython or micropython whichever I can get to work.
'''
import board
import analogio
import pwmio 
import time
from adafruit_simplemath import map_range

new_min = 0.025  # min and max delay time(seconds)
new_max = 2
delaySpeed = analogio.AnalogIn(board.GP28)  # rotary for speed of bolt


class LaserFire():
    TOTALBITS = 16
    LEDbits = []
    TRACERS = 3  # number of tracers
    FullOnDutyCycle = 0xffff  # full on
    DutyCycle = []
    pathlength = TOTALBITS/2
    
    def __init__(self, **kwargs):
        print(kwargs)
        if kwargs != {}:
            if 'tracers' in kwargs:
                LaserFire.TRACERS = kwargs['tracers']
            if 'range' in kwargs:
                LaserFire.pathlength = kwargs['range']
            
        for i in reversed(range(LaserFire.TRACERS)):
            LaserFire.DutyCycle.append(int(LaserFire.FullOnDutyCycle/(LaserFire.TRACERS-i)))
        # Setup LED list
        subcommand1 = 'LaserFire.LEDbits.append(pwmio.PWMOut(board.GP'
        subcommand2 = ', frequency=1000))'
        for i in range(LaserFire.TOTALBITS):
            fullcommand = subcommand1 + str(i) + subcommand2
            exec(fullcommand)

    def Fire():
         # remapped_delaySpeed = int(map_range(delaySpeed.value,
            # 0, 65520, new_min, new_max))
        remapped_delaySpeed = map_range(delaySpeed.value,
                                        200, 65520, new_min, new_max)
        for i in range(LaserFire.pathlength):
           
            j = i + LaserFire.pathlength
            # set bolt and tracers
            for d in range(LaserFire.TRACERS):
                print(i, d, LaserFire.DutyCycle[d])
                LaserFire.LEDbits[i-d].duty_cycle = LaserFire.DutyCycle[d]
                LaserFire.LEDbits[j-d].duty_cycle = LaserFire.DutyCycle[d]
            # cleanup overflowed tracers
            for x in range(LaserFire.TRACERS):
                if i < x:
                    LaserFire.LEDbits[i-x].duty_cycle = 0
                    LaserFire.LEDbits[j-x].duty_cycle = 0

            time.sleep(remapped_delaySpeed)

            for i in range(len(LaserFire.LEDbits)):  # turn off all LED's
                LaserFire.LEDbits[i].duty_cycle = 0x0000


if __name__ == '__main__':
    LaserFire(tracers=3, range=8)
    while True:
        LaserFire.Fire()
