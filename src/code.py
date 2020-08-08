from analogio import AnalogIn
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
from adafruit_debouncer import Debouncer

import board
import time
import simpleio
import digitalio

ledMain = simpleio.DigitalOut(board.D13)

vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)
kit = MotorKit(steppers_microsteps=4)

decDirection = stepper.BACKWARD
decStyle = stepper.SINGLE
decMove = False
decDelay = 0.11332

raDirection = stepper.FORWARD
raStyle = stepper.SINGLE
raMove = False
raDelay = 0.11332

def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2

def make_output_led(pin):
    led = digitalio.DigitalInOut(pin)
    led.direction = digitalio.Direction.OUTPUT
    return led

def make_debouncable(pin):
    switch_io = digitalio.DigitalInOut(pin)
    switch_io.direction = digitalio.Direction.INPUT
    switch_io.pull = digitalio.Pull.UP
    return switch_io

ledDown = make_output_led(board.A2)
ledUp = make_output_led(board.A3)
ledLeft = make_output_led(board.A4)
ledRight = make_output_led(board.A5)

buttonDown = Debouncer(make_debouncable(board.D4))
buttonUp = Debouncer(make_debouncable(board.D5))
buttonLeft = Debouncer(make_debouncable(board.D6),0.5)
buttonRight = Debouncer(make_debouncable(board.D9),0.5)

kit.stepper1.release()
kit.stepper2.release()
raTriggerLatch = False

TICKS_PER_SEC = 1_000_000_000

heartbeatTicks = TICKS_PER_SEC
raLastTicks = 0
decLastTicks = 0
lastTicks = 0
lastUpDateTicks = 0

decRateTicks = (decDelay * TICKS_PER_SEC) // 4
raRateTicks = raDelay * TICKS_PER_SEC
UpdateTicks = 0.05  * TICKS_PER_SEC

while True:
    currentTicks = time.monotonic_ns();

    if currentTicks - UpdateTicks > lastUpDateTicks:
        lastUpDateTicks = currentTicks
        buttonDown.update()
        buttonUp.update()
        buttonLeft.update()
        buttonRight.update()

    raTrigger = (not buttonLeft.value or not buttonRight.value) and (not (buttonLeft.value and buttonRight.value))

    if raTrigger and not raTriggerLatch:
        raTriggerLatch = True
        raMove = not raMove
        if not buttonLeft.value:
            raDirection = stepper.BACKWARD
        elif not buttonRight.value:
            raDirection = stepper.FORWARD
    elif raTriggerLatch and not raTrigger:
        raTriggerLatch = False

    decMove = (not buttonUp.value or not buttonDown.value) and (not (buttonUp.value and buttonDown.value))

    if decMove:
        if not buttonUp.value:
            decDirection = stepper.BACKWARD
        elif not buttonDown.value:
            decDirection = stepper.FORWARD

    if raMove:
        if (time.monotonic_ns() - raLastTicks > raRateTicks):
            numsteps = kit.stepper1.onestep(direction=raDirection, style=raStyle)
            if numsteps % 32 == 0:
                if raDirection == stepper.FORWARD:
                    ledRight.value = not ledRight.value
                else:
                    ledLeft.value = not ledLeft.value
            raLastTicks = time.monotonic_ns()
    else:
        kit.stepper1.release()
        ledRight.value = False
        ledLeft.value = False

    if decMove:
        if (time.monotonic_ns() - decLastTicks > decRateTicks):
            numsteps = kit.stepper2.onestep(direction=decDirection, style=decStyle)
            if numsteps % 32 == 0:
                if decDirection == stepper.BACKWARD:
                    ledUp.value = not ledUp.value
                else:
                    ledDown.value = not ledDown.value
            decLastTicks = time.monotonic_ns()
    else:
        kit.stepper2.release()
        ledUp.value = False
        ledDown.value = False

    currentTime = time.monotonic_ns()
    interval = currentTime - currentTicks

    if currentTicks - heartbeatTicks > lastTicks:
        ledMain.value = not ledMain.value
        lastTicks = currentTicks
        battery_voltage = get_voltage(vbat_voltage)
        print("VBat voltage: {:.2f}".format(battery_voltage))
        #print(f"Up: {buttonUp.value} Down: {buttonDown.value} Left: {buttonLeft.value} Right: {buttonRight.value}")
        #print(f"RA Trigger: {raTrigger}, RA Move: {raMove}")
        print(f"Interval: {interval}")