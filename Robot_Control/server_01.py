import math
import sys
import time
from math import pi
# import os
import argparse
# from pathlib import Path
from sys import platform
from opcua import ua, Server, uamethod
from pycreate2 import Create2

# from collections import namedtuple

print("Started script server_01.py")

# global Variables
# bools
bMoving = False

#Roomba node
Roomba

# Prepare Roomba connection
sys.path.insert(0, "..")
default_port_gpio = "/dev/ttyAMA0"
default_port_usb = "/dev/ttyUSB0"


def parse_args():
    parser = argparse.ArgumentParser(description='roomba controller')
    parser.add_argument('-p', '--port', default=default_port_usb, help='communication interface')
    parser.add_argument('-e', '--encrypted', action='store_true', help='activate encryption')
    args = parser.parse_args()
    return args


opts = parse_args()
port = opts.port
encryption = opts.encrypted


def isLinux():
    if platform == "linux" or platform == "linux2":
        return True
    elif platform == "win32":
        # Windows...
        return False


if isLinux():
    bot = Create2(port=port, baud='115200')
else:
    # Windows...
    bot = 1


def initializeRobot():
    print("Initializing Robot communication")
    bot.start()
    bot.safe()
    # The robot will not charge, but you full control over it with a few exceptions.
    # If the cliff sensors or wheel drop sensors are triggered, the robot goes back to PASSIVE mode.
    # bot.full()
    # The robot will not charge and you have full control.
    # You are responsible to handle any response due to cliff, wheel drop or any other sensors.
    print("Robot started")


def closeRobotConnection():
    bot.close()


def printRobotSensors():
    sensors = bot.get_sensors()  # returns all data
    print(sensors)


def updateRobotSensors(roomba):
    sensors = bot.get_sensors()
    bumps_wheeldrops = roomba.get_child("{}:bumps_wheeldrops".format(idx))
    wall = roomba.get_child("{}:wall".format(idx))
    cliff_left = roomba.get_child("{}:cliff_left".format(idx))
    cliff_front_left = roomba.get_child("{}:cliff_front_left".format(idx))
    cliff_front_right = roomba.get_child("{}:cliff_front_right".format(idx))
    cliff_right = roomba.get_child("{}:cliff_right".format(idx))
    virtual_wall = roomba.get_child("{}:virtual_wall".format(idx))
    overcurrents = roomba.get_child("{}:overcurrents".format(idx))
    dirt_detect = roomba.get_child("{}:dirt_detect".format(idx))
    ir_opcode = roomba.get_child("{}:ir_opcode".format(idx))
    buttons = roomba.get_child("{}:buttons".format(idx))
    distance = roomba.get_child("{}:distance".format(idx))
    angle = roomba.get_child("{}:angle".format(idx))
    charger_state = roomba.get_child("{}:charger_state".format(idx))
    voltage = roomba.get_child("{}:voltage".format(idx))
    current = roomba.get_child("{}:current".format(idx))
    temperature = roomba.get_child("{}:temperature".format(idx))
    battery_charge = roomba.get_child("{}:battery_charge".format(idx))
    battery_capacity = roomba.get_child("{}:battery_capacity".format(idx))
    wall_signal = roomba.get_child("{}:wall_signal".format(idx))
    cliff_left_signal = roomba.get_child("{}:cliff_left_signal".format(idx))
    cliff_front_left_signal = roomba.get_child("{}:cliff_front_left_signal".format(idx))
    cliff_front_right_signal = roomba.get_child("{}:cliff_front_right_signal".format(idx))
    cliff_right_signal = roomba.get_child("{}:cliff_right_signal".format(idx))
    charger_available = roomba.get_child("{}:charger_available".format(idx))
    open_interface_mode = roomba.get_child("{}:open_interface_mode".format(idx))
    song_number = roomba.get_child("{}:song_number".format(idx))
    song_playing = roomba.get_child("{}:song_playing".format(idx))
    oi_stream_num_packets = roomba.get_child("{}:oi_stream_num_packets".format(idx))
    velocity = roomba.get_child("{}:velocity".format(idx))
    radius = roomba.get_child("{}:radius".format(idx))
    velocity_right = roomba.get_child("{}:velocity_right".format(idx))
    velocity_left = roomba.get_child("{}:velocity_left".format(idx))
    encoder_counts_left = roomba.get_child("{}:encoder_counts_left".format(idx))
    encoder_counts_right = roomba.get_child("{}:encoder_counts_right".format(idx))
    light_bumper = roomba.get_child("{}:light_bumper".format(idx))
    light_bumper_left = roomba.get_child("{}:light_bumper_left".format(idx))
    light_bumper_front_left = roomba.get_child("{}:light_bumper_front_left".format(idx))
    light_bumper_center_left = roomba.get_child("{}:light_bumper_center_left".format(idx))
    light_bumper_center_right = roomba.get_child("{}:light_bumper_center_right".format(idx))
    light_bumper_front_right = roomba.get_child("{}:light_bumper_front_right".format(idx))
    light_bumper_right = roomba.get_child("{}:light_bumper_right".format(idx))
    ir_opcode_left = roomba.get_child("{}:ir_opcode_left".format(idx))
    ir_opcode_right = roomba.get_child("{}:ir_opcode_right".format(idx))
    left_motor_current = roomba.get_child("{}:left_motor_current".format(idx))
    right_motor_current = roomba.get_child("{}:right_motor_current".format(idx))
    main_brush_current = roomba.get_child("{}:main_brush_current".format(idx))
    side_brush_current = roomba.get_child("{}:side_brush_current".format(idx))
    statis = roomba.get_child("{}:statis".format(idx))

    print("Updating Sensor values....")
    print("Distanz:", sensors.distance, "Winkel:", sensors.angle)
    print("li", sensors.encoder_counts_left, "re", sensors.encoder_counts_right)

    if sensors.distance != 0 or sensors.angle != 0:
        eventgen.event.distance = ua.Variant(sensors.distance)
        eventgen.event.angle = ua.Variant(sensors.angle)
        eventgen.trigger(message=("Distance: " + str(sensors.distance) + " Angle: " + str(sensors.angle)))

    bumps_wheeldrops.set_value(sensors.bumps_wheeldrops)
    wall.set_value(sensors.wall)
    cliff_left.set_value(sensors.cliff_left)
    cliff_front_left.set_value(sensors.cliff_front_left)
    cliff_front_right.set_value(sensors.cliff_front_right)
    cliff_right.set_value(sensors.cliff_right)
    virtual_wall.set_value(sensors.virtual_wall)
    overcurrents.set_value(sensors.overcurrents)
    dirt_detect.set_value(sensors.dirt_detect)
    ir_opcode.set_value(sensors.ir_opcode)
    buttons.set_value(sensors.buttons)
    distance.set_value(sensors.distance)
    angle.set_value(sensors.angle)
    charger_state.set_value(sensors.charger_state)
    voltage.set_value(sensors.voltage)
    current.set_value(sensors.current)
    temperature.set_value(sensors.temperature)
    battery_charge.set_value(sensors.battery_charge)
    battery_capacity.set_value(sensors.battery_capacity)
    wall_signal.set_value(sensors.wall_signal)
    cliff_left_signal.set_value(sensors.cliff_left_signal)
    cliff_front_left_signal.set_value(sensors.cliff_front_left_signal)
    cliff_front_right_signal.set_value(sensors.cliff_front_right_signal)
    cliff_right_signal.set_value(sensors.cliff_right_signal)
    charger_available.set_value(sensors.charger_available)
    open_interface_mode.set_value(sensors.open_interface_mode)
    song_number.set_value(sensors.song_number)
    song_playing.set_value(sensors.song_playing)
    oi_stream_num_packets.set_value(sensors.oi_stream_num_packets)
    velocity.set_value(sensors.velocity)
    radius.set_value(sensors.radius)
    velocity_right.set_value(sensors.velocity_right)
    velocity_left.set_value(sensors.velocity_left)
    encoder_counts_left.set_value(sensors.encoder_counts_left)
    encoder_counts_right.set_value(sensors.encoder_counts_right)
    light_bumper.set_value(sensors.light_bumper)
    light_bumper_left.set_value(sensors.light_bumper_left)
    light_bumper_front_left.set_value(sensors.light_bumper_front_left)
    light_bumper_center_left.set_value(sensors.light_bumper_center_left)
    light_bumper_center_right.set_value(sensors.light_bumper_center_right)
    light_bumper_front_right.set_value(sensors.light_bumper_front_right)
    light_bumper_right.set_value(sensors.light_bumper_right)
    ir_opcode_left.set_value(sensors.ir_opcode_left)
    ir_opcode_right.set_value(sensors.ir_opcode_right)
    left_motor_current.set_value(sensors.left_motor_current)
    right_motor_current.set_value(sensors.right_motor_current)
    main_brush_current.set_value(sensors.main_brush_current)
    side_brush_current.set_value(sensors.side_brush_current)
    statis.set_value(sensors.statis)


# method to be exposed through server
# uses a decorator to automatically convert to and from variants

driveSpeed = 100


@uamethod
def setSpeed(parent, newspeed):
    print("setSpeed called:", newspeed)
    bot.digit_led_ascii('speed')
    global driveSpeed
    driveSpeed = newspeed
    time.sleep(2)
    bot.digit_led_ascii(str(newspeed))
    # time.sleep(5) #sec
    return newspeed


@uamethod
def moveForward(parent, l_distance):
    global bMoving
    global Roomba
    while bMoving:
        time.sleep(0.001)
    bMoving = True
    print("moveForward called")
    bot.digit_led_ascii('for')
    bot.drive_direct(driveSpeed, driveSpeed)
    if l_distance > 0:
        time.sleep(l_distance / driveSpeed)
        bot.drive_stop()
        bot.digit_led_ascii('')
        bMoving = False
        updateRobotSensors(Roomba)
    return bMoving


@uamethod
def moveForwardCircular(parent, l_distance, l_radius):
    # negativer Radius == im Uhrzeigersinn
    l_radius_abs = math.fabs(l_radius)
    global bMoving
    global Roomba
    while bMoving:
        time.sleep(0.001)
    bMoving = True
    print("moveForwardCircular called")
    bot.digit_led_ascii('circ')
    # Berechne drivespeeds
    if l_radius > 0:
        # gegen Uhrzeigersinn
        driveSpeedlinks = int (driveSpeed * (l_radius_abs - 117.5) / l_radius_abs)
        driveSpeedrechts = int (driveSpeed * (l_radius_abs + 117.5) / l_radius_abs)
    elif l_radius < 0:
        # mit Uhrzeigersinn
        driveSpeedlinks = int (driveSpeed * (l_radius_abs + 117.5) / l_radius_abs)
        driveSpeedrechts = int (driveSpeed * (l_radius_abs - 117.5) / l_radius_abs)
    else:
        breakpoint()

    bot.drive_direct(driveSpeedrechts, driveSpeedlinks)
    if l_distance > 0:
        time.sleep(l_distance / driveSpeed)
        bot.drive_stop()
        bot.digit_led_ascii('')
        bMoving = False
        updateRobotSensors(Roomba)
    return bMoving


@uamethod
def moveBackward(parent, l_distance):
    global bMoving
    global Roomba
    while bMoving:
        time.sleep(0.001)
    bMoving = True
    print("moveBackward called")
    bot.digit_led_ascii('back')
    bot.drive_direct(-driveSpeed, -driveSpeed)
    if l_distance > 0:
        time.sleep(l_distance / driveSpeed)
        bot.drive_stop()
        bot.digit_led_ascii('')
        bMoving = False
        updateRobotSensors(Roomba)
    return bMoving


@uamethod
def rotateLeft(parent, l_angle):
    global bMoving
    global Roomba
    while bMoving:
        time.sleep(0.001)
    bMoving = True
    print("rotateLeft called")
    bot.digit_led_ascii('left')
    bot.drive_direct(driveSpeed, -driveSpeed)
    if l_angle > 0:
        time.sleep(l_angle * pi / 180 * 117.5 / driveSpeed)
        bot.drive_stop()
        bot.digit_led_ascii('')
        bMoving = False
        updateRobotSensors(Roomba)
    return bMoving


@uamethod
def rotateRight(parent, l_angle):
    global bMoving
    global Roomba
    while bMoving:
        time.sleep(0.001)
    bMoving = True
    print("rotateRight called")
    bot.digit_led_ascii('rite')
    bot.drive_direct(-driveSpeed, driveSpeed)
    if l_angle > 0:
        time.sleep(l_angle * pi / 180 * 117.5 / driveSpeed)
        bot.drive_stop()
        bot.digit_led_ascii('')
        bMoving = False
        updateRobotSensors(Roomba)
    return bMoving


@uamethod
def moveStop(parent):
    global bMoving
    global Roomba
    print("moveStop called")
    bot.digit_led_ascii('stop')
    bot.drive_stop()
    bMoving = False
    updateRobotSensors(Roomba)
    return bMoving


if __name__ == "__main__":

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://test.hendrik"
    idx = server.register_namespace(uri)

    ### Roombanode erstellen
    roombanode = server.nodes.objects.add_object(idx, "Roomba1")
    ### Methoden erstellen
    moveForwardNode = roombanode.add_method(idx, "moveForward", moveForward, [ua.VariantType.Int16],
                                            [ua.VariantType.Boolean])
    moveForwardCircularNode = roombanode.add_method(idx, "moveForwardCircular", moveForwardCircular,
                                                    [ua.VariantType.Int16, ua.VariantType.Int16],
                                                    [ua.VariantType.Boolean])
    moveBackwardNode = roombanode.add_method(idx, "moveBackward", moveBackward, [ua.VariantType.Int16],
                                             [ua.VariantType.Boolean])
    rotateLeftNode = roombanode.add_method(idx, "rotateLeft", rotateLeft, [ua.VariantType.Int16],
                                           [ua.VariantType.Boolean])
    rotateRightNode = roombanode.add_method(idx, "rotateRight", rotateRight, [ua.VariantType.Int16],
                                            [ua.VariantType.Boolean])
    moveStopNode = roombanode.add_method(idx, "moveStop", moveStop, [], [ua.VariantType.Boolean])
    setSpeedNode = roombanode.add_method(idx, "setSpeed", setSpeed, [ua.VariantType.Int16], [ua.VariantType.Int16])

    ### Eventgenerator
    eventnode = server.nodes.objects.add_object(idx, "EventGenNode")
    eventtype = server.create_custom_event_type(idx, 'EncoderEvent', ua.ObjectIds.BaseEventType,
                                                [('distance', ua.VariantType.Int64),
                                                 ('angle', ua.VariantType.Int64)])
    eventgen = server.get_event_generator(eventtype, eventnode)
    eventgen.event.Severity = 500

    ### Sensornodes erstellen
    bumps_wheeldropsnode = roombanode.add_variable(idx, "bumps_wheeldrops", 0)
    wallnode = roombanode.add_variable(idx, "wall", 0, ua.VariantType.Boolean)
    cliff_leftnode = roombanode.add_variable(idx, "cliff_left", 0, ua.VariantType.Boolean)
    cliff_front_leftnode = roombanode.add_variable(idx, "cliff_front_left", 0, ua.VariantType.Boolean)
    cliff_front_rightnode = roombanode.add_variable(idx, "cliff_front_right", 0, ua.VariantType.Boolean)
    cliff_rightnode = roombanode.add_variable(idx, "cliff_right", 0)
    virtual_wallnode = roombanode.add_variable(idx, "virtual_wall", 0)
    overcurrentsnode = roombanode.add_variable(idx, "overcurrents", 0)
    dirt_detectnode = roombanode.add_variable(idx, "dirt_detect", 0)
    ir_opcodenode = roombanode.add_variable(idx, "ir_opcode", 0)
    buttonsnode = roombanode.add_variable(idx, "buttons", 0)
    distancenode = roombanode.add_variable(idx, "distance", 0, ua.VariantType.Int16)
    anglenode = roombanode.add_variable(idx, "angle", 0, ua.VariantType.Int16)
    charger_statenode = roombanode.add_variable(idx, "charger_state", 0)
    voltagenode = roombanode.add_variable(idx, "voltage", 0)
    currentnode = roombanode.add_variable(idx, "current", 0)
    temperaturenode = roombanode.add_variable(idx, "temperature", 0)
    battery_chargenode = roombanode.add_variable(idx, "battery_charge", 0)
    battery_capacitynode = roombanode.add_variable(idx, "battery_capacity", 0)
    wall_signalnode = roombanode.add_variable(idx, "wall_signal", 0)
    cliff_left_signalnode = roombanode.add_variable(idx, "cliff_left_signal", 0)
    cliff_front_left_signalnode = roombanode.add_variable(idx, "cliff_front_left_signal", 0)
    cliff_front_right_signalnode = roombanode.add_variable(idx, "cliff_front_right_signal", 0)
    cliff_right_signalnode = roombanode.add_variable(idx, "cliff_right_signal", 0)
    charger_availablenode = roombanode.add_variable(idx, "charger_available", 0)
    open_interface_modenode = roombanode.add_variable(idx, "open_interface_mode", 0)
    song_numbernode = roombanode.add_variable(idx, "song_number", 0)
    song_playingnode = roombanode.add_variable(idx, "song_playing", 0)
    oi_stream_num_packetsnode = roombanode.add_variable(idx, "oi_stream_num_packets", 0)
    velocitynode = roombanode.add_variable(idx, "velocity", 0)
    radiusnode = roombanode.add_variable(idx, "radius", 0)
    velocity_rightnode = roombanode.add_variable(idx, "velocity_right", 0)
    velocity_leftnode = roombanode.add_variable(idx, "velocity_left", 0)
    encoder_counts_leftnode = roombanode.add_variable(idx, "encoder_counts_left", 0)
    encoder_counts_rightnode = roombanode.add_variable(idx, "encoder_counts_right", 0)
    light_bumpernode = roombanode.add_variable(idx, "light_bumper", 0)
    light_bumper_leftnode = roombanode.add_variable(idx, "light_bumper_left", 0)
    light_bumper_front_leftnode = roombanode.add_variable(idx, "light_bumper_front_left", 0)
    light_bumper_center_leftnode = roombanode.add_variable(idx, "light_bumper_center_left", 0)
    light_bumper_center_rightnode = roombanode.add_variable(idx, "light_bumper_center_right", 0)
    light_bumper_front_rightnode = roombanode.add_variable(idx, "light_bumper_front_right", 0)
    light_bumper_rightnode = roombanode.add_variable(idx, "light_bumper_right", 0)
    ir_opcode_leftnode = roombanode.add_variable(idx, "ir_opcode_left", 0)
    ir_opcode_rightnode = roombanode.add_variable(idx, "ir_opcode_right", 0)
    left_motor_currentnode = roombanode.add_variable(idx, "left_motor_current", 0)
    right_motor_currentnode = roombanode.add_variable(idx, "right_motor_current", 0)
    main_brush_currentnode = roombanode.add_variable(idx, "main_brush_current", 0)
    side_brush_currentnode = roombanode.add_variable(idx, "side_brush_current", 0)
    statisnode = roombanode.add_variable(idx, "statis", 0)

    # set all possible endpoint policies for clients to connect through
    # server.set_security_policy([
    #             ua.SecurityPolicyType.NoSecurity,
    #             ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
    #             ua.SecurityPolicyType.Basic256Sha256_Sign])
    # server.set_security_policy([ua.SecurityPolicyType.NoSecurity])

    if encryption:
        # load server certificate and private key. This enables endpoints
        # with signing and encryption.
        ## ENCRYPTION ###
        server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt])
        server.load_certificate("certificate-example.der")
        server.load_private_key("private-key-example.pem")
    else:
        ## NO ENCRYPTION ##
        server.set_security_policy([ua.SecurityPolicyType.NoSecurity])

    # get Objects node, this is where we should put our nodes
    root = server.get_root_node()

    objects = server.get_objects_node()
    Roomba = objects.get_child("{}:Roomba1".format(idx))
    server.link_method(Roomba.get_child("{}:moveForward".format(idx)), moveForward)
    server.link_method(Roomba.get_child("{}:moveForwardCircular".format(idx)), moveForwardCircular)
    server.link_method(Roomba.get_child("{}:moveBackward".format(idx)), moveBackward)
    server.link_method(Roomba.get_child("{}:rotateLeft".format(idx)), rotateLeft)
    server.link_method(Roomba.get_child("{}:rotateRight".format(idx)), rotateRight)
    server.link_method(Roomba.get_child("{}:moveStop".format(idx)), moveStop)
    server.link_method(Roomba.get_child("{}:setSpeed".format(idx)), setSpeed)

    # starting!
    server.start()

    if isLinux():
        initializeRobot()
        printRobotSensors()
        print("Server started...")

    try:
        count = 0
        while True:
            time.sleep(1)  # sec
            if not bMoving:
                if isLinux():
                    count = count + 1
                    print(count)
                    updateRobotSensors(Roomba)

    finally:
        # close connection, remove subcsriptions, etc
        server.stop()
        # closeRobotConnection()
