#!/usr/bin/env python3

import os
import sys
import time
import datetime
from influxdb import InfluxDBClient

import pymodbus
import serial
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
from pymodbus.transaction import ModbusRtuFramer

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

influx_host = 'localhost'
port = 8086
dbname = "my_local_db"
user = "admin"
password = "admin"

def get_data_points_04(temperature_1, humidity_1, co2_1, temperature_2, humidity_2, co2_2, soil1, soil2):

    iso = time.ctime()
    json_body = [
                {
                "measurement": "ambient_celcius",
                "tags": {"host": influx_host},
                "time": iso,
                "fields": {
                    "value": temperature_1,
                    }
                },
		{
		"measurement": "ambient_humidity",
		"tags": {"host": influx_host},
                "time": iso,
                "fields": {
                    "value": humidity_1,
                    }
                },
		{
                "measurement": "ambient_co2",
                "tags": {"host": influx_host},
                "time": iso,
                "fields": {
                    "value": co2_1,
                    }
                },
                {
                "measurement": "outer_celcius",
                "tags": {"host": influx_host},
                "time": iso,
                "fields": {
                    "value": temperature_2,
                    }
                },
                { 
                "measurement": "outer_humidity",
                "tags": {"host": influx_host},
                "time": iso,
                "fields": {
                    "value": humidity_2,
                    }
                },
                { 
                "measurement": "outer_co2",
                "tags": {"host": influx_host},
                "time": iso,
                "fields": {
                    "value": co2_2,
                    }
                },
                {
                "measurement": "soil_moisture1",
                "tags": {"host": influx_host},
                "time": iso,
                "fields": {
                    "value": soil1,
                    }
                },
                { 
                "measurement": "soil_moisture2",
                "tags": {"host": influx_host},
                "time": iso,
                "fields": {
                    "value": soil2,
                    }
                }

            ]
    return json_body

#def get_data_points_05(temperature_2, humidity_2, co2_2):

#    iso = time.ctime()
#    json_body = [
#                {
#                "measurement": "outer_celcius",
#                "tags": {"host": influx_host},
#                "time": iso,
#                "fields": {
#                    "value": temperature_2,
#                    }
#                },
#                {
#                "measurement": "outer_humidity",
#                "tags": {"host": influx_host},
#                "time": iso,
#                "fields": {
#                    "value": humidity_2,
#                    }
#                },
#                {
#                "measurement": "outer_co2",
#                "tags": {"host": influx_host},
#                "time": iso,
#                "fields": {
#                    "value": co2_2,
#                    }
#                }
#            ]
#    return json_body


capture_interval = 5.0
client = InfluxDBClient(influx_host, port, user, password, dbname)

clientMB = ModbusClient(method = "rtu", port="/dev/ttyAMA0",stopbits = 1, bytesize = 8, parity = 'N', baudrate= 115200, timeout=0.5)

while 1:
    connection = clientMB.connect()

    result = clientMB.read_holding_registers(0,7,unit= 0x04)
    result2 = clientMB.read_holding_registers(0,7,unit= 0x05)
    result3 = clientMB.read_holding_registers(0,2,unit= 0x06)

    a = result.registers[0]/16
    temp_1 = round(a,1)
    humidity_1 = result.registers[6]
    co2_1 = result.registers[1]
    #data1 = get_data_points_04(temp_1, humidity_1, co2_1)
    #client.write_points(data1)

    a2 = result2.registers[0]/16
    temp_2 = round(a2,1)
    humidity_2 = result2.registers[6]
    co2_2 = result2.registers[1]

    soil1 = result3.registers[0]
    soil2 = result3.registers[1]

    data2 = get_data_points_04(temp_1, humidity_1, co2_1, temp_2, humidity_2, co2_2, soil1, soil2)

#    client.write_points(data1)
    client.write_points(data2)
    print(result.registers)
    print(result2.registers)

    clientMB.close()
    time.sleep(capture_interval)
