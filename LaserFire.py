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

TOTALBITS = 15  # START AT 0
LEDbits = []
delaySpeed = analogio.AnalogIn(board.GP28)
DutyCycle = 0xffff
DutyCycle2 = DutyCycle/2
DutyCycle4 = DutyCycle/4
new_min = 0.025
new_max = 2


class LaserFire():

    def __init__(self):
        # setup delay pot

        # Setup LED list
        subcommand1 = 'LEDbits.append(pwmio.PWMOut(board.GP'
        subcommand2 = ', frequency=1000))'
        for i in range(TOTALBITS+1):
            fullcommand = subcommand1 + str(i) + subcommand2
            exec(fullcommand)


if __name__ == '__main__':
    LaserFire()
    while True:
        # remapped_delaySpeed = int(map_range(delaySpeed.value, 0, 65520, new_min, new_max))
        remapped_delaySpeed = map_range(delaySpeed.value, 200, 65520, new_min, new_max)

        for i in range(8):
            LEDbits[i].duty_cycle = int(DutyCycle)
            if i >= 1:
                LEDbits[i-1].duty_cycle = int(DutyCycle2)
            if i >= 2:
                LEDbits[i-2].duty_cycle = int(DutyCycle4)
            j = i + 8
            LEDbits[j].duty_cycle = int(DutyCycle)
            if j >= 9:
                LEDbits[j-1].duty_cycle = int(DutyCycle2)
            if j >= 10:
                LEDbits[j-2].duty_cycle = int(DutyCycle4)
            print(i, j, remapped_delaySpeed)
            time.sleep(remapped_delaySpeed)
            # print(delaySpeed.value, ' ', remapped_delaySpeed)
            LEDbits[i].duty_cycle = 0
            LEDbits[i-1].duty_cycle = 0
            LEDbits[i-2].duty_cycle = 0
            LEDbits[j].duty_cycle = 0
            LEDbits[j-1].duty_cycle = 0
            LEDbits[j-2].duty_cycle = 0
