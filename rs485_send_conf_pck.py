#!/usr/bin/env python3
import time
import pymodbus
import serial
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
from pymodbus.transaction import ModbusRtuFramer

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder

import crcmod
import math
from intelhex import IntelHex

import logging

mb_unit=0x07
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client= ModbusClient(method = "rtu", port="/dev/ttyUSB0",stopbits = 1, bytesize = 8, parity = 'N', baudrate= 115200, timeout=0.5)

#Connect to the serial modbus server
connection = client.connect()
print (connection)

builder = BinaryPayloadBuilder(byteorder=Endian.Big,wordorder=Endian.Little)


builder.add_16bit_uint(5)   #Type of packet
payload = builder.to_registers()
payload = builder.build()
client.write_registers(0, payload, skip_encode=True, unit=mb_unit)
builder.reset()
#time.sleep(20)

builder.add_16bit_uint(6)   #Type of packet
payload = builder.to_registers()
payload = builder.build()
client.write_registers(0, payload, skip_encode=True, unit=mb_unit)
builder.reset()
#time.sleep(20)

builder.add_16bit_uint(0)   #Type of packet
payload = builder.to_registers()
payload = builder.build()
client.write_registers(0, payload, skip_encode=True, unit=mb_unit)
builder.reset()

#time.sleep(2)

builder.add_16bit_uint(0)   #Type of packet
payload = builder.to_registers()
payload = builder.build()
client.write_registers(0, payload, skip_encode=True, unit=mb_unit)
builder.reset()

#time.sleep(10)

client.close()

