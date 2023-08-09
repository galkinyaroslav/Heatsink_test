import pyvisa as visa


def find_device():
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


def configure(device):
    a34970.write_termination = '\n'
    a34970.read_termination = '\n'
    print(f"{device.query('*IDN?')} --->>> CONFIGURED")
    device.write('*RST')
    device.write('*CLS')

    device.write('CONF:TEMP FRTD, 85 ,(@202, 203)')
    device.write('TEMP:TRAN:FRTD:RES:REF 1000,(@202, 203)')

    print(device.query('TEMP:TRAN:FRTD:RES:REF? (@202, 203)'))

    device.write('TEMP:TRAN:FRTD:TYPE 85,(@202, 203)')
    print(device.query('TEMP:TRAN:FRTD:TYPE? (@202, 203)'))

    print(device.query('CONF? (@202, 203)'))
    device.write('ROUT:SCAN (@202, 203)')


def read_data(device):
    row_data = device.query('READ?')
    data = [float(value) for value in row_data.strip().split(',')]
    print(data)


if __name__ == '__main__':
    a34970 = find_device()
    configure(a34970)
    read_data(a34970)
