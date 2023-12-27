import serial.tools.list_ports
ports = [port.device for port in serial.tools.list_ports.comports()]

print(ports)
import subprocess
pswd = 'alisca'
port = '/dev/ttyUSB0'
print(subprocess.run(f'echo {pswd} | sudo -S chmod a+rw {port}', shell=True))
port = '/dev/ttyS0'
print(subprocess.run(f'echo {pswd} | sudo -S chmod a+rw {port}', shell=True))