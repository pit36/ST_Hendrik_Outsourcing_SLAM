# Simple client for testing purposes
# will be elaborated for further useful things
#
#
from opcua import Client
import time
import datetime
import csv
import math

# global Variables

# calculated position robot
calpos = {"x": 0.0, "y": 0.0, "ori": 0.0}
# robot position from encoders
encWerte = []
encpos = {"x": 0.0, "y": 0.0, "ori": 0.0}
# robot position from visual sensory equipment
senpos = {"x": 0.0, "y": 0.0, "ori": 0.0}


class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def event_notification(self, event):
        print("New event:", event.Message.Text)
        zeitstempel = datetime.datetime.now()
        encWerte.append([event.distance, event.angle, zeitstempel])
        print(encWerte)


def writeToCsv(source, posx, posy, posz, degz, comment):
    zeitstempel = datetime.datetime.now()
    reihe = [source, zeitstempel, posx, posy, posz, degz, comment]
    with open('test.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(reihe)


def writeToCsv_Zeit(source, posx, posy, posz, degz, zeitstempel, comment):
    reihe = [source, zeitstempel, posx, posy, posz, degz, comment]
    with open('test.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(reihe)


def auswertungEncWert():
    global encpos
    global encWerte
    distance = encWerte[0][0]
    angle = encWerte[0][1]
    zeitstempel = encWerte[0][2]
    if angle == 0:
        if distance == 0:
            print("Enc. meldet Distanz 0 und Winkel 0")
        else:
            encpos["x"] = math.cos(math.radians(encpos["ori"])) * distance + encpos["x"]
            encpos["y"] = math.sin(math.radians(encpos["ori"])) * distance + encpos["y"]
            writeToCsv_Zeit('B', encpos["x"], encpos["y"], 0.0, encpos["ori"], zeitstempel, 'Distanz: ' + str(distance))
    else:
        if distance == 0:
            encpos["ori"] = encpos["ori"] + angle
            writeToCsv_Zeit('B', encpos["x"], encpos["y"], 0.0, encpos["ori"], zeitstempel, 'Winkel: ' + str(angle))
        else:
            # Winkel und Distanzänderung zugleich.
            # Annäherung über Bogen mit Tangentenwinkel, der je die Hälfte vom gefahrenen Winkel darstellt
            richtungsehne = encpos["ori"] + angle / 2
            längesehne = 2 * (distance / math.radians(math.fabs(angle))) * math.sin(math.radians(math.fabs(angle) / 2))
            encpos["x"] = math.cos(math.radians(richtungsehne)) * längesehne + encpos["x"]
            encpos["y"] = math.sin(math.radians(richtungsehne)) * längesehne + encpos["y"]
            encpos["ori"] = encpos["ori"] + angle
            writeToCsv_Zeit('B', encpos["x"], encpos["y"], 0.0, encpos["ori"], zeitstempel,
                            'Enc.Wert: Distanz: ' + str(distance) + ' Winkel: ' + str(angle))
    encWerte.pop(0)


def setSpeed(newspeed):
    res = objdata.call_method("{}:setSpeed".format(idx), newspeed)
    print("neue Geschwindigkeit:", res)


def moveForward(distance):
    global calpos
    res = objdata.call_method("{}:moveForward".format(idx), distance)
    calpos["x"] = math.cos(math.radians(calpos["ori"])) * distance + calpos["x"]
    calpos["y"] = math.sin(math.radians(calpos["ori"])) * distance + calpos["y"]
    writeToCsv('A', calpos["x"], calpos["y"], 0.0, calpos["ori"], 'Distanz: ' + str(distance))
    print("Roboter blieb stehen:", not res)

def moveForwardCircular(distance,radius):
    # negativer Radius == im Uhrzeigersinn
    global calpos

    res = objdata.call_method("{}:moveForwardCircular".format(idx), distance, radius)
    angle = (distance/radius) * (180/math.pi)
    # Annäherung über Bogen mit Tangentenwinkel, der die Hälfte vom gefahrenen Winkel darstellt
    richtungsehne = calpos["ori"] + angle / 2
    längesehne = 2 * (distance / math.radians(math.fabs(angle))) * math.sin(math.radians(math.fabs(angle) / 2))
    calpos["x"] = math.cos(math.radians(richtungsehne)) * längesehne + calpos["x"]
    calpos["y"] = math.sin(math.radians(richtungsehne)) * längesehne + calpos["y"]
    calpos["ori"] = calpos["ori"] + angle
    writeToCsv('A', calpos["x"], calpos["y"], 0.0, calpos["ori"], 'Distanz: ' + str(distance) + ' Winkel: ' + str(angle))
    print("Roboter blieb stehen:", not res)

def moveBackward(distance):
    global calpos
    res = objdata.call_method("{}:moveBackward".format(idx), distance)
    calpos["x"] = -math.cos(math.radians(calpos["ori"])) * distance + calpos["x"]
    calpos["y"] = -math.sin(math.radians(calpos["ori"])) * distance + calpos["y"]
    writeToCsv('A', calpos["x"], calpos["y"], 0.0, calpos["ori"], 'Distanz: ' + str(-distance))
    print("Roboter blieb stehen:", not res)


def rotateLeft(angle):
    global calpos
    res = objdata.call_method("{}:rotateLeft".format(idx), angle)
    calpos["ori"] = calpos["ori"] + angle
    writeToCsv('A', calpos["x"], calpos["y"], 0.0, calpos["ori"], 'Winkel' + str(angle))
    print("Roboter blieb stehen:", not res)


def rotateRight(angle):
    global calpos
    res = objdata.call_method("{}:rotateRight".format(idx), angle)
    calpos["ori"] = calpos["ori"] - angle
    writeToCsv('A', calpos["x"], calpos["y"], 0.0, calpos["ori"], 'Winkel' + str(-angle))
    print("Roboter blieb stehen:", not res)


def moveStop():
    res = objdata.call_method("{}:moveStop".format(idx))
    print("Roboter blieb stehen:", not res)


if __name__ == "__main__":
    # Connect
    # client = Client("opc.tcp://192.168.1.111:4840/server/")
    client = Client("opc.tcp://10.0.0.150:4840/server/")
    # client = Client("opc.tcp://admin@localhost:4840/server/") #connect using a user
    try:
        client.connect()
        client.load_type_definitions()  # load definition of server specific structures/extension objects

        rootnode = client.get_root_node()

        # getting the namespace idx
        uri = "http://test.hendrik"
        idx = client.get_namespace_index(uri)

        # get obj data for method calls
        objdata = rootnode.get_child(["0:Objects", "{}:Roomba1".format(idx)])

        # Now getting a variable node using its browse path
        dirtDetect = rootnode.get_child(["0:Objects", "{}:Roomba1".format(idx), "{}:dirt_detect".format(idx)])
        print("dirtDetect is at node: ", dirtDetect)
        print("Value:", dirtDetect.get_value())
        # and again
        leftenc = rootnode.get_child(["0:Objects", "{}:Roomba1".format(idx), "{}:encoder_counts_left".format(idx)])
        print("leftenc is at node: ", leftenc)
        print("Value:", leftenc.get_value())

        print("Set current position as Zeropoint")
        calpos["x"] = 0.0
        calpos["y"] = 0.0
        calpos["ori"] = 0.0
        writeToCsv('A', calpos["x"], calpos["y"], 0.0, calpos["ori"], 'Nullstellung A')
        encpos["x"] = 0.0
        encpos["y"] = 0.0
        encpos["ori"] = 0.0
        writeToCsv('B', encpos["x"], encpos["y"], 0.0, encpos["ori"], 'Nullstellung B')

        # subscribing to the event node
        handler = SubHandler()
        sub = client.create_subscription(250, handler)
        eventobj = rootnode.get_child(["0:Objects", "{}:EventGenNode".format(idx)])
        myevent = rootnode.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "{}:EncoderEvent".format(idx)])
        handle = sub.subscribe_events(eventobj, myevent)

        # set speed to x mm/s
        setSpeed(150)
        
        # motion commands

        # for i in range(0, 6):
        #     rotateLeft(5)
        #     time.sleep(2)
        
        for i in range(0, 12):
            moveForward(250)
            #time.sleep(2)

        for i in range(0, 8):
            distan=int ((math.pi * 600) /8)
            moveForwardCircular(distan,600)
            #time.sleep(2)

        # for i in range(0, 24):
        #     rotateRight(5)
        #     time.sleep(2)

        # for i in range(0, 12):
        #     moveForward(50)
        #     time.sleep(2)

        # for i in range(0, 24):
        #     rotateRight(5)
        #     time.sleep(2)
        #
        # for i in range(0, 12):
        #     moveForward(50)
        #     time.sleep(2)
        
        # do statistical logging
        time.sleep(5)
        print(encWerte)
        while len(encWerte) > 0:
            auswertungEncWert()
        print("Auswertung fertig")

    finally:
        client.disconnect()
