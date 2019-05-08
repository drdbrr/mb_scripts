#!/usr/bin/env python3
import pymodbus
import serial
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
from pymodbus.transaction import ModbusRtuFramer

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

#count= the number of registers to read
#unit= the slave unit this request is targeting
#address= the starting address to read from

client= ModbusClient(method = "rtu", port="/dev/ttyUSB0",stopbits = 1, bytesize = 8, parity = 'N', baudrate= 115200, timeout=0.5)

#Connect to the serial modbus server
connection = client.connect()
print (connection)

#builder = BinaryPayloadBuilder(byteorder=Endian.Big,wordorder=Endian.Little)

#builder.add_32bit_uint(0x11223344)
#builder.add_32bit_uint(0x55667788)
#payload = builder.to_registers()
#payload = builder.build()

#client.write_registers(0, payload, skip_encode=True, unit=1)


#rq = client.write_coil(0, True, unit=0x07)
#assert(rq.function_code < 0x80)     # test that we are not an error

#Starting add, num of reg to read, slave unit.
result = client.read_holding_registers(0,7,unit= 0x02)
#result = client.read_holding_registers(0,125,unit= 0x04)
#result = client.read_holding_registers(0,125,unit= 0x04)
#result = client.read_holding_registers(0,125,unit= 0x04)

#result.registers[0] = result.registers[0]/16

print(result.registers)
#print(result)
#print(result.registers)


#Closes the underlying socket connection
client.close()

