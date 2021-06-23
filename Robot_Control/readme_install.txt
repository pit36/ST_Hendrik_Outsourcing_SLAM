Mainly pyCreate2 and OPC-UA are required to run the server and the client software.
Thus install pycreate2 and opcua by using pip:

>>> pip3 install opcua
>>> pip3 install pycreate2



Change into the Python filestructure to find the create2api.py. 
As GitHub user yaoli90 mentions here [https://github.com/MomsFriendlyRobotCompany/pycreate2/issues/12] modify the get_sensors() function in create2api.py to avoid the 'Flash CRC' and 'Wake up from sleep' msgs by replacing it with:

def get_sensors(self):
        opcode = OPCODES.SENSORS
        cmd = (100,)
        sensor_pkt_len = 80

        self.SCI.write(opcode, cmd)
        time.sleep(0.015)  # wait 15 msec

        packet_byte_data = self.SCI.read(sensor_pkt_len)

        flash_msg = packet_byte_data.find(b'(0x0)\n\r')
        wakeup_msg = packet_byte_data.find(b'conds\r\n')
        msg = max(flash_msg, wakeup_msg)

        if not msg == -1:
            print(packet_byte_data)
            packet_byte_data_continue=self.SCI.read(msg+7)
            packet_byte_data = packet_byte_data[msg+7:] + packet_byte_data_continue

        sensors = SensorPacketDecoder(packet_byte_data)

        return sensors

