import serial
import time
import numpy as np
from threading import Thread


class CHSerial:

    def __init__(self, port):
        self.cohop = serial.Serial(port=port, bytesize=serial.EIGHTBITS, baudrate=9600,
                                   parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1)
        self.limit = 2  # limit for the number of retries when an error occurs
        self.retries = 0
        self.timeout = 2  # timeout in seconds

    def rw_data(self, data):
        self.cohop.flushInput()
        self.cohop.flushOutput()
        self.cohop.write(bytearray(data))
        self.cohop.flush()

        waiting = time.time()
        while not self.cohop.in_waiting:
            if time.time() - waiting > self.timeout:
                return -1, -1
            time.sleep(0.05)

        time.sleep(0.5)
        data = []
        received_bytes = self.cohop.in_waiting
        print('bytes -> ', received_bytes)

        # read 18 bytes from the dispenser to get the status
        if received_bytes == 6:
            data.append((self.cohop.read(6)).hex())
        elif received_bytes == 18:
            data.append((self.cohop.read(18)).hex())
        elif received_bytes == 24:
            data.append((self.cohop.read(24)).hex())
        else:
            return -1, -1
        data[len(data) - 1] = [int('0x'+data[len(data)-1][x:x+2], 16)
                               for x in range(0, len(data[len(data)-1]), 2)]
        hex_data = self.dec_to_hex(data[0])
        return data[0], hex_data

    def poll_data(self, initialize=False):
        poll_buff = [0x05, 0x10, 0x00, 0x11, 0x00, 0x26]  # polling data
        state_ok = [0x05, 0x01, 0x00, 0x04, 0x00, 0x0A]  # response ok
        state_nc = [0x05, 0x01, 0x00, 0x04,
                    0x02, 0x0C]  # response no coins

        data, hex_data = self.rw_data(poll_buff)
        print("data received -> ", hex_data)  # debug

        def data_comp(to_comp):
            return not sum(np.bitwise_xor(data, to_comp))

        delay = 0.05
        if initialize:
            delay = 4

        while (data == -1 or not data_comp(state_ok)) and self.retries < self.limit and initialize:
            self.retries += 1
            data, hex_data = self.rw_data(poll_buff)
            time.sleep(delay)
        self.retries = 0

        if data_comp(state_ok):
            print("SYSTEMS OK.")
            return 0
        elif data_comp(state_nc):
            print("NO COINS!!")
            return 1
        else:
            print("AN ERROR HAS OCCURED ON THE DISPENSER SIDE!")
            return 2

    def dispense(self, count):  # dispense count number of coins
        dispense_buff = [0x05, 0x10, 0x00, 0x18, 0x01, 0x2E]
        ok_res = [0x05, 0x01, 0x00, 0xAA, 0x01, 0xB1,
                  0x05, 0x01, 0x00, 0x07, 0x00, 0x0D,
                  0x05, 0x01, 0x00, 0x08, 0x00, 0x0E]
        nc_res = [0x05, 0x01, 0x00, 0xAA, 0x01, 0xB1,
                  0x05, 0x01, 0x00, 0x07, 0x00, 0x0D,
                  0x05, 0x01, 0x00, 0x08, 0x00, 0x0E,
                  0x05, 0x01, 0x00, 0x04, 0x02, 0x0C]

        data, hex_data = self.rw_data(dispense_buff)
        print("received data -> ", hex_data)  # debug
        while data == -1 and self.retries < self.limit:
            self.retries += 1
            data, hex_data = self.rw_data(dispense_buff)
        self.retries = 0

        def data_comp(comp1, comp2):
            return not sum(np.bitwise_xor(comp1, comp2))
        if len(data) == len(nc_res) and data_comp(data, nc_res):
            print("NO COINS!!")
            return self.dec_to_hex(dispense_buff), hex_data
        elif len(data) == len(ok_res) and data_comp(data, ok_res):
            print("DISPENSED!")
            return self.dec_to_hex(dispense_buff), hex_data
        print("Error")
        return hex_data, 0

    def dec_to_hex(self, array):
        hex_final_list = []
        hex_list = []
        for i, elem in enumerate(array):
            if i % 6 == 0 and i:
                hex_final_list.append(hex_list)
                hex_list = []
            hex_list.append(hex(elem))
        hex_final_list.append(hex_list)
        return hex_final_list

if  __name__=='__main__':
    d = CHSerial(port='/dev/ttyUSB0')

    d.poll_data(True)
    d.dispense(1)