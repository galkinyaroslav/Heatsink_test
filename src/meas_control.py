import os

import keysight as keysight
import pyvisa as visa
import time
import keysight
# os.add_dll_directory('lib64/libiovisa.so')

# configuring the backend
# rmtk = visa.ResourceManager('visa32')  # 'agvisa32', 'ktvisa32', 'visa32'
rmag = visa.ResourceManager('@py')  #'/usr/lib/x86_64-linux-gnu/libiovisa.so 'agvisa32', 'ktvisa32', 'visa32'
# print(rmtk)
print(rmag)

# list the devices
# ('ASRL1::INSTR', 'ASRL2::INSTR', 'GPIB0::3::INSTR', 'USB::0x0699::0x052C::C035430::INSTR')
# print(rmtk.list_resources('?*'))
print(rmag.list_resources('?*'))

a34970 = rmag.open_resource('ASRL/dev/ttyACM0::INSTR')
# a34970.write_termination = '\n'
# a34970.read_termination = '\n' # НАЙТИ ТЕРМИНАТОР В МАНУАЛЕ!!!!!!!!!!!!!
print(a34970.query('*IDN?'))
# # a34970.write('*cls')
# # a34970.write('*rst')
#
# a34970.write('CONF:TEMP FRTD, 85 ,(@202, 203)')
# a34970.visalib.write(a34970.session, 'TEMP:TRAN:FRTD:RES:REF 1000,(@202, 203)'.encode())
#
# print(a34970.query('TEMP:TRAN:FRTD:RES:REF? (@202, 203)'))
#
# a34970.write('TEMP:TRAN:FRTD:TYPE 85,(@202, 203)')
# print(a34970.query('TEMP:TRAN:FRTD:TYPE? (@202, 203)'))
#
# print(a34970.query('CONF? (@202, 203)'))
# a34970.write('ROUT:SCAN (@202, 203)')
# data = a34970.query('READ?')
# print(type(data))
# for _ in range(10):
#     print(a34970.query('READ?'))
#     time.sleep(1)


# TODO write_async works correctly, but after that query goes to error
# print(f'session {a34970.session}')
# a34970.visalib.write_asynchronously(a34970.session, 'TEMP:TRAN:FRTD:RES:REF 100,(@202)'.encode())
# a34970.visalib.read_asynchronously(a34970.session, 'TEMP:TRAN:FRTD:RES:REF 1000,(@202)'.encode())