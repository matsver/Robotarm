#!/usr/bin/env pybricks-micropython 
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color
from pybricks.tools import wait

ev3 = EV3Brick()

ev3.speaker.beep()

MIDDLE = 110
RIGHT = 210
LEFT = 20

LOW = -60
SCAN = -50
HIGH = -15

OPEN = 60


color_list = [Color.RED, Color.GREEN]

base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])
base_motor.control.limits(speed=60, acceleration=120)
base_switch = TouchSensor(Port.S1)

elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])
elbow_motor.control.limits(speed=60, acceleration=120)
elbow_switch = TouchSensor(Port.S2)

gripper_motor = Motor(Port.A)
color_sensor = ColorSensor(Port.S3)


gripper_motor.run_until_stalled(-50, then=Stop.HOLD)
gripper_motor.reset_angle(0)


def init():
    elbow_motor.run(60) 
    while not elbow_switch.pressed():
        wait(10)
    elbow_motor.reset_angle(0)
    elbow_motor.hold()

    base_motor.run(-60) 
    while not base_switch.pressed():
        wait(10)
    base_motor.reset_angle(0)
    base_motor.hold()

    elbow_motor.run_target(60, HIGH)
    base_motor.run_target(60, MIDDLE)
    gripper_motor.run_target(50, OPEN)

    for i in range(3):
        wait(5)
        ev3.speaker.beep()

def scan():
    elbow_motor.run_target(60, SCAN)
    scanned = color_sensor.color()
    print(scanned)
    return scanned

init()

for j in range(3):
    base_motor.run_target(60, RIGHT)
    elbow_motor.run_target(60, LOW)
    gripper_motor.run_until_stalled(-50, then=Stop.HOLD)
    if scan() in color_list:
        elbow_motor.run_target(60, HIGH)
        base_motor.run_target(60, LEFT)
        elbow_motor.run_target(60, LOW)
        gripper_motor.run_target(50, OPEN)
        elbow_motor.run_target(60, HIGH)
    else:
        elbow_motor.run_target(60, HIGH)
        base_motor.run_target(60, MIDDLE)
        elbow_motor.run_target(60, LOW)
        gripper_motor.run_target(50, OPEN)
        elbow_motor.run_target(60, HIGH)
