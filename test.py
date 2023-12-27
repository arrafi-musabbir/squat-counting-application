import serial.tools.list_ports
ports = [port.device for port in serial.tools.list_ports.comports()]
print("ports found!: ", ports)

ports = [port.device for port in serial.tools.list_ports.comports() if port.device.startswith('/dev/ttyUSB')]
print("ports found!: ", ports)


import subprocess
pswd = ''

port = '/dev/ttyUSB0'
print("\ntrying to connect to ", port)
print(subprocess.run(f'echo {pswd} | sudo -S chmod a+rw {port}', shell=True))
port = '/dev/ttyS0'
print("\ntrying to connect to ", port)
print(subprocess.run(f'echo {pswd} | sudo -S chmod a+rw {port}', shell=True))