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

TOTALBITS = 15  # Start at 0
LEDbits = []
TRACERS = 3  # number of tracers
FullOnDutyCycle = 0xffff  # full on
DutyCycle = []
for i in reversed(range(TRACERS)):
    DutyCycle.append(int(FullOnDutyCycle/(TRACERS-i)))
new_min = 0.025  # min and max delay time(seconds)
new_max = 2
delaySpeed = analogio.AnalogIn(board.GP28)  # rotary for speed of bolt


class LaserFire():
    def __init__(self):
        # Setup LED list
        subcommand1 = 'LEDbits.append(pwmio.PWMOut(board.GP'
        subcommand2 = ', frequency=1000))'
        for i in range(TOTALBITS+1):
            fullcommand = subcommand1 + str(i) + subcommand2
            exec(fullcommand)

    def Fire():
        for i in range(8):
            # remapped_delaySpeed = int(map_range(delaySpeed.value,
            # 0, 65520, new_min, new_max))
            remapped_delaySpeed = map_range(delaySpeed.value,
                                            200, 65520, new_min, new_max)
            j = i + 8
            # set bolt and tracers
            for d in range(TRACERS):
                print(i, d, DutyCycle[d])
                LEDbits[i-d].duty_cycle = DutyCycle[d]
                LEDbits[j-d].duty_cycle = DutyCycle[d]
            # cleanup overflowed tracers
            for x in range(TRACERS):
                if i < x:
                    LEDbits[i-x].duty_cycle = 0
                    LEDbits[j-x].duty_cycle = 0

            time.sleep(remapped_delaySpeed)

            for i in range(len(LEDbits)):  # turn off all LED's
                LEDbits[i].duty_cycle = 0x0000


if __name__ == '__main__':
    LaserFire()
    while True:
        LaserFire.Fire()
