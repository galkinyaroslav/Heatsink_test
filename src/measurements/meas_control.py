import pyvisa as visa
from pyvisa import Resource

CHANNELS = '(@101:110,201:210)'


def find_device() -> Resource:
    rmag = visa.ResourceManager()  # '/usr/lib/x86_64-linux-gnu/libiovisa.so'
    list_devices = rmag.list_resources('?*')
    print(list_devices)
    DEVISE_NAME = '34970A'
    for device in list_devices:
        try:
            temp_device = rmag.open_resource(device)
            temp_name = temp_device.query('*IDN?')
            if DEVISE_NAME in temp_name:
                print(temp_name.strip(), '--->>>', device)
                # temp_device.close()
                return temp_device

        except visa.errors.VisaIOError:
            print('This is not appropriate device or device is not found')


def configure(device: Resource) -> dict:
    device.write_termination = '\n'
    device.read_termination = '\n'
    device.write('*RST')
    device.write('*CLS')

    device.write(f'CONF:TEMP FRTD, 85, {CHANNELS}')
    device.write(f'TEMP:TRAN:FRTD:RES:REF 1000, {CHANNELS}')

    # print(device.query(f'TEMP:TRAN:FRTD:RES:REF? {CHANNELS}'))

    device.write(f'TEMP:TRAN:FRTD:TYPE 85, {CHANNELS}')
    # print(device.query(f'TEMP:TRAN:FRTD:TYPE? {CHANNELS}'))

    # print(device.query(f'CONF? {CHANNELS}'))
    device.write(f'ROUT:SCAN {CHANNELS}')
    message = f"{device.query('*IDN?')} --->>> CONFIGURED"
    print(message)
    return {'message': message}


def read_data(device: Resource) -> dict:
    device.write(f'INIT')
    row_data = device.query(f'FETC?')
    data = [float(value) for value in row_data.strip().split(',')]
    # print(data)
    return {'data': data}


if __name__ == '__main__':
    a34970 = find_device()
    configure(a34970)
    read_data(a34970)
    a34970.close()
