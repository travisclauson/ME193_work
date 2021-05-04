import adafruit_bmp280 as bmp
from adafruit_bmp280 import (
    _CHIP_ID,
    _REGISTER_CHIPID,
    _REGISTER_DIG_T1,
    _REGISTER_SOFTRESET,
    _REGISTER_STATUS,
    _REGISTER_CTRL_MEAS,
    _REGISTER_CONFIG,
    _REGISTER_PRESSUREDATA,
    _REGISTER_TEMPDATA,
)
from micropython import const

verbose = False

register_names = { #for readability (I know there must be a more elegant way of doing this all...)
    208: "CHIP ID",
    136: "DIG T1",
    224: "SOFT RESET",
    243: "STATUS",
    244: "CTRL MEAS",
    245: "CONFIG",
    247: "PRESSURE DATA",
    250: "TEMP DATA"
}

register_values = {
    _REGISTER_CHIPID: _CHIP_ID,  # When queried, the chip ID must be what the library expects
    _REGISTER_DIG_T1: 0x01,  # Used by _read_coefficients
    _REGISTER_STATUS: 0x01,  # Used by _get_status (and by extension _read_temperature and pressure)
    _REGISTER_TEMPDATA: 0x01,  # Used by _read_temperature
    _REGISTER_PRESSUREDATA: 0x01,  # Used by pressure
}


def _read_register(self, register, length): #custom read_register function that returns an hard-coded value
    val = [register_values[register]] * length
    if (verbose):
        print("Read {} from {} register with length {}".format(val[0], register_names[register], length))
    return val


def _write_register_byte(self, register, value): #custom write_register function that skips over any write commands
    if (verbose):
            print("Wrote {} to {} register".format(value, register_names[register]))


# these redirect function calls to my custom functions
bmp.Adafruit_BMP280._read_register = _read_register
bmp.Adafruit_BMP280._write_register_byte = _write_register_byte

sensor = bmp.Adafruit_BMP280()

pressure_reg_values = [1,501,1000,1<<16]
temp_reg_values = [1,5850,5,1<<16]
DIG_T1_reg_values = [1,5,10,100]

expected_pressure_val = [301315.6, 1014.41, 1013.58, -3466.52]
expected_temp_val = [0.0000, 24.624, 35.694, -76.576]

print("Expected Values (Pressure(hPa), Temperature(C))     Actual Values (Pressure, Temperature)")
sensor = []
for i in range(len(pressure_reg_values)):
    register_values[_REGISTER_DIG_T1] = DIG_T1_reg_values[i]
    sensor.append(bmp.Adafruit_BMP280()) # since DIG_1T reg cannot be changed after sensor object created
    register_values[_REGISTER_PRESSUREDATA] = pressure_reg_values[i]
    register_values[_REGISTER_TEMPDATA] = temp_reg_values[i]
    print(expected_pressure_val[i], "  ", expected_temp_val[i], end=" ")
    print("                                ", sensor[i].pressure, "  ", sensor[i].temperature)
#used to scan for desired values
"""
for i in range(1):
    for j in range(500):
        for k in range(1):
            pressure_reg_val = 1000
            temp_reg_val = 50*j
            register_values[_REGISTER_PRESSUREDATA] = pressure_reg_val
            register_values[_REGISTER_TEMPDATA] = temp_reg_val
            digT1_reg_val = register_values[_REGISTER_DIG_T1]
            if (sensor.temperature > 10 and sensor.temperature < 50 and sensor.pressure > 990 and sensor.pressure < 1020):
                print("DIG_T1 (coefficient register): ", digT1_reg_val)
                print("Pressure Register: ", pressure_reg_val, end = " ")
                print("Temp Register: ", temp_reg_val)
                print("Pressure Reading: ", sensor.pressure, end = " ")
                print("Temp Reading: ", sensor.temperature)
                print()
"""
