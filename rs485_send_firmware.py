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

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client= ModbusClient(method = "rtu", port="/dev/ttyUSB0",stopbits = 1, bytesize = 8, parity = 'N', baudrate= 115200, timeout=0.5)

#Connect to the serial modbus server
connection = client.connect()
print (connection)

#---------Set start parameters
fw_file='/home/drjacka/garden_acs/1.hex' #firmware file
mb_unit=0x06 #MB test device number
#---------

#---------Make modbus payload
builder = BinaryPayloadBuilder(byteorder=Endian.Big,wordorder=Endian.Little)
#---------

#---------Init firmware
ih = IntelHex()
ih.fromfile(fw_file,format='hex')
a = ih.segments()
a_len = a[0][1] #Number of elements in firmware

aa_len = (a_len>>8) & 0xFF #Number of elements in firmware LSB
ab_len = a_len & 0xFF #Number of elements in firmware MSB

page_len=16
b=ih.tobinarray()
page_buf=[]
page_cnt=math.ceil(a_len/page_len)

j=0;
k=page_len;


#!!!!!!!!!!
elements_total = page_len * page_cnt
empty_rest = elements_total - a_len
#---------

#---------Send start message of firmware
crc32_func = crcmod.mkCrcFun(0x104C11DB7, initCrc=0, xorOut=0xFFFFFFFF) #Poly CRC-32: 0x104C11DB7 http://crcmod.sourceforge.net/crcmod.predefined.html
crc_sum32 = crc32_func(b)

crc_sum32_a = (crc_sum32>>16) & 0xFFFF
crc_sum32_b = crc_sum32 & 0xFFFF
crc_sum32_c = (crc_sum32_a>>8) & 0xFF
crc_sum32_d = crc_sum32_a & 0xFF
crc_sum32_e = (crc_sum32_b >> 8) & 0xFF
crc_sum32_f = crc_sum32_b & 0xFF

builder.add_16bit_uint(2) #Type of packet
builder.add_16bit_uint(1) #Reserved

builder.add_16bit_uint(aa_len) 
builder.add_16bit_uint(ab_len) 

builder.add_16bit_uint(crc_sum32_c) #CRC32 sum of firmware body
builder.add_16bit_uint(crc_sum32_d)
builder.add_16bit_uint(crc_sum32_e)
builder.add_16bit_uint(crc_sum32_f)

pg_num_h = (page_cnt >> 8 ) & 0xFF
pg_num_l = page_cnt & 0xFF

builder.add_16bit_uint(pg_num_h) #total number of pages
builder.add_16bit_uint(pg_num_l)

payload = builder.to_registers()
payload = builder.build()
client.write_registers(0, payload, skip_encode=True, unit=mb_unit)

time.sleep(0.1)

builder.reset()
#---------

#---------Prepare firmware array
for page_num in range (page_cnt):
    page_buf.append([])
    page_buf[page_num]=b[j:k]
    pg_len = len(page_buf[page_num])
    j+=page_len
    k+=page_len
#---------

#---------Add page head to builder array 
    builder.add_16bit_uint(1)   #Type of packet
    builder.add_16bit_uint(1)   #reserved
    #builder.add_16bit_uint(pg_len)   #Add length of page
    builder.add_16bit_uint(page_len)   #Add length of page
    builder.add_16bit_uint(page_num+1)   #Add number of page
#---------

#---------Add firmware to builder array
    for z in range (pg_len):
        builder.add_16bit_uint(page_buf[page_num][z])
#---------

#---------Add empty rest at the end of page, if needed
    #for a_len in range (empty_rest):
        #builder.add_16bit_uint(page_buf[page_cnt][a_len] = 0)
        #builder.add_16bit_uint(0)
#---------

#---------Send firmware body
    payload = builder.to_registers()
    payload = builder.build()
    client.write_registers(0, payload, skip_encode=True, unit=mb_unit)

    builder.reset()
#---------
client.close()

