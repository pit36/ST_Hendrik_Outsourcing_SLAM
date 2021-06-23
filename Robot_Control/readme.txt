the client_01.py and server_01.py are based on python3

some not very common python packages are needed, see the readme_install.txt for instructions.

server_01.py is designed to run on the Raspberry Pi with a Create2 robot connected to it. It will connect to the robot as well as open a OPC UA server. The robot can be controlled by the OPC UA methods. The server does forward encoder data by a OPC UA event.

client_01.py is providing a easy way of programming a path for the robot to do. It needs the server already running on a known IP. The IP needs to be inserted at the __main__ functionality. After finishing the programmed run, it will create a test.csv with essential data. Please see the readme_testdata.txt for further information.
