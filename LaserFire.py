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



class LaserFire():
    TOTALBITS = 16
    LEDbits = []
    TRACERS = 3  # number of tracers
    FullOnDutyCycle = 0xffff  # full on
    DutyCycle = []
    pathlength = TOTALBITS/2
    speedcontrol = True
    new_min = 0.015  # min and max delay time(seconds)
    new_max = 2
    delaySpeed = analogio.AnalogIn(board.GP28)  # rotary for speed of bolt

    
    def __init__(self, **kwargs):
        # Only allowed for tracers and path length
        if kwargs != {}:
            if 'tracers' in kwargs:
                LaserFire.TRACERS = kwargs['tracers']
            if 'range' in kwargs:
                LaserFire.pathlength = kwargs['range']
            if 'laserSpeed' in kwargs:  # laserSpeed in seconds
                if kwargs['laserSpeed'] != '':
                    LaserFire.speedcontrol = False
                    LaserFire.delaySpeed = kwargs['laserSpeed']
                else:
                    LaserFire.delaySpeed = LaserFire.delaySpeed
        # Set the tracer PWM   
        for i in reversed(range(LaserFire.TRACERS)):
            LaserFire.DutyCycle.append(int(LaserFire.FullOnDutyCycle/(LaserFire.TRACERS-i)))
        # Setup LED list
        subcommand1 = 'LaserFire.LEDbits.append(pwmio.PWMOut(board.GP'
        subcommand2 = ', frequency=1000))'
        for i in range(LaserFire.TOTALBITS):
            fullcommand = subcommand1 + str(i) + subcommand2
            exec(fullcommand)

    def Fire():
        if LaserFire.speedcontrol:
             # Get the delay from the rotary - may change if deeded to pass as param.
            remapped_delaySpeed = map_range(LaserFire.delaySpeed.value,200, 65520,
                                            LaserFire.new_min, LaserFire.new_max)
        else:
            remapped_delaySpeed = LaserFire.delaySpeed
            
        for i in range(LaserFire.pathlength):
            
            j = i + LaserFire.pathlength
            # set bolt and tracers
            for d in range(LaserFire.TRACERS):
                print(remapped_delaySpeed, i, d, LaserFire.DutyCycle[d])
                LaserFire.LEDbits[i-d].duty_cycle = LaserFire.DutyCycle[d]
                LaserFire.LEDbits[j-d].duty_cycle = LaserFire.DutyCycle[d]
            # cleanup overflowed tracers
            for x in range(LaserFire.TRACERS):
                if i < x:
                    LaserFire.LEDbits[i-x].duty_cycle = 0
                    LaserFire.LEDbits[j-x].duty_cycle = 0

            time.sleep(remapped_delaySpeed)
            
            # Turn everthing off
            for i in range(len(LaserFire.LEDbits)):  # turn off all LED's
                LaserFire.LEDbits[i].duty_cycle = 0x0000


if __name__ == '__main__':
#     LaserFire(tracers=3, range=8, laserSpeed=0.2)  # laserSpeed is steps/sec (in sec.)
    LaserFire(tracers=3, range=8)
    while True:
        LaserFire.Fire()
