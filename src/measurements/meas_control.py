import os

import pyvisa as visa
import time


def open_device():
    rmag = visa.ResourceManager()  # '/usr/lib/x86_64-linux-gnu/libiovisa.so'
    list_devices = rmag.list_resources('?*')
    DEVISE_NAME = '34970A'
    for device in list_devices:
        temp_device = rmag.open_resource(device)
        try:
            if DEVISE_NAME in temp_device.query('*IDN?'):
                print(temp_device.query('*IDN?').strip(), ' --->>> OPENED')
                return temp_device

        except visa.errors.VisaIOError:
            print('Devise is not found')


def configure(device):
    # a34970.write_termination = '\n'
    # a34970.read_termination = '\n'
    # print(device.query('*IDN?'))
    device.write('*cls')
    device.write('*rst')
    #
    device.write('CONF:TEMP FRTD, 85 ,(@202, 203)')
    device.write('TEMP:TRAN:FRTD:RES:REF 1000,(@202, 203)')

    # print(device.query('TEMP:TRAN:FRTD:RES:REF? (@202, 203)'))

    device.write('TEMP:TRAN:FRTD:TYPE 85,(@202, 203)')
    # print(device.query('TEMP:TRAN:FRTD:TYPE? (@202, 203)'))

    # print(device.query('CONF? (@202, 203)'))
    device.write('ROUT:SCAN (@202, 203)')


def read_data(device):
    data = [float(value) for value in device.query('READ?').strip().split(',')]
    print(data)
    # time.sleep(1)


a34970 = open_device()
configure(a34970)
read_data(a34970)
# data = a34970.query('READ?')
# print(type(data))




# TODO write_async works correctly, but after that query goes to error
# print(f'session {a34970.session}')
# a34970.visalib.write_asynchronously(a34970.session, 'TEMP:TRAN:FRTD:RES:REF 100,(@202)'.encode())
# a34970.visalib.read_asynchronously(a34970.session, 'TEMP:TRAN:FRTD:RES:REF 1000,(@202)'.encode())
