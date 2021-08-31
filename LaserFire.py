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
import pwmio 
import time
import analogio
from adafruit_simplemath import map_range



class LaserFire():
    TOTALBITS = 16
    LEDbits = []
    TRACERS = 3  # number of tracers
    FullOnDutyCycle = 0xffff  # full on
    DutyCycle = []
    pathlength = int(TOTALBITS/2)
    speedcontrol = True
    new_min = 0.015  # min and max delay time(seconds)
    new_max = 2
    delaySpeed = analogio.AnalogIn(board.GP28)  # rotary for speed of bolt
    direction = 1

    def __init__(self, **kwargs):
        # Only allowed for tracers and path length
        if kwargs != {}:
            if 'tracers' in kwargs:
                LaserFire.TRACERS = kwargs['tracers']
            if 'lrange' in kwargs:
                LaserFire.pathlength = kwargs['lrange']
            if 'laserSpeed' in kwargs:  # laserSpeed in seconds
                if kwargs['laserSpeed'] != '':
                    LaserFire.speedcontrol = False
                    LaserFire.delaySpeed = kwargs['laserSpeed']
                else:
                    LaserFire.delaySpeed = LaserFire.delaySpeed
            if 'direction' in kwargs:
                LaserFire.direction = kwargs['direction']
                
       
        # Setup LED list
        subcommand1 = 'LaserFire.LEDbits.append(pwmio.PWMOut(board.GP'
        subcommand2 = ', frequency=1000))'
        for i in range(LaserFire.TOTALBITS):
            fullcommand = subcommand1 + str(i) + subcommand2
            exec(fullcommand)

    def Fire(direction=1):
        LaserFire.direction = direction
        if LaserFire.speedcontrol:
             # Get the delay from the rotary - may change if needed to pass as param.
            remapped_delaySpeed = map_range(LaserFire.delaySpeed.value,200, 65520,
                                            LaserFire.new_min, LaserFire.new_max)
        else:
            remapped_delaySpeed = LaserFire.delaySpeed
         # Set the tracer PWM
        if LaserFire.direction == 1:
            for i in reversed(range(LaserFire.TRACERS)):
                LaserFire.DutyCycle.append(int(LaserFire.FullOnDutyCycle/(LaserFire.TRACERS-i)))
        else:
            for i in range(LaserFire.TRACERS):
                LaserFire.DutyCycle.append(int(LaserFire.FullOnDutyCycle/(LaserFire.TRACERS-i)))
        
        if LaserFire.direction == 1:
            for i in range(LaserFire.pathlength):
                j = i + LaserFire.pathlength
                # set bolt and tracers
                for d in range(LaserFire.TRACERS):
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
                    LaserFire.LEDbits[i].duty_cycle = 0
        else:
            for i in reversed(range(LaserFire.pathlength)):
                j = LaserFire.pathlength + i
                
                # set bolt and tracers
                for d in reversed(range(LaserFire.TRACERS)):
                    print('i,j, d',i,j, d)
                    LaserFire.LEDbits[i-d].duty_cycle = LaserFire.DutyCycle[d]
                    LaserFire.LEDbits[j-d].duty_cycle = LaserFire.DutyCycle[d]
                # cleanup overflowed tracers
                for x in reversed(range(LaserFire.TRACERS)):
                    if i > LaserFire.pathlength - x:
                        print('x tracer overflow',i,x)
                        LaserFire.LEDbits[i-x].duty_cycle = 0
                        LaserFire.LEDbits[j-x].duty_cycle = 0
                time.sleep(remapped_delaySpeed)
                    # Turn everthing off
                for i in range(len(LaserFire.LEDbits)):  # turn off all LED's
                    LaserFire.LEDbits[i].duty_cycle = 0
        
    def LaserFireClose():
        print('Closing outputs.')
        for i in range(len(LaserFire.LEDbits)):
            LaserFire.LEDbits[i].deinit()

           

if __name__ == '__main__':
#     LaserFire(tracers=3, range=8, laserSpeed=0.2)  # laserSpeed is steps/sec (in sec.)
    LaserFire()
    try:
        while True:
            LaserFire.Fire(direction=-1)
    except KeyboardInterrupt:
        LaserFire.LaserFireClose()
