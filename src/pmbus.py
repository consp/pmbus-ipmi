import subprocess
import struct
from binascii import unhexlify
from time import sleep

class VENDOR:
    SUPERMICRO = 0

class pmbus(object):
    bus = 7
    address = 0
    vout_mode = None
    vout_exp = None

    def __init__(self, bus=7, address=0x78):
        self.bus = bus
        self.address = address
        self.vendor = VENDOR.SUPERMICRO

        # set exp of vout
        self.vout_mode_get()

    def _raw_command(self, byte, length, counter=0, expt=True):
        # ipmitool raw 0x06 0x52 0x07 0x78 0x01 0x8c
        while counter < 10:
            try:
                output = subprocess.run(['ipmitool', 'raw', '0x06', '0x52', '0x%02X' % (self.bus), '0x%02X' % (self.address), '0x%02X' % (length), '0x%02X' % (byte)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout

                output = output.replace(b" ", b"")
                output = output.replace(b"\n", b"")
                #print(output)
                if length == 2:
                    return struct.unpack("H", unhexlify(output))[0]
                elif length == 1:
                    return struct.unpack("B", unhexlify(output))[0]
                return unhexlify(output)
            except Exception as e:
                if not expt:
                    return None
                sleep(2)
                counter = counter + 1
                pass

    def status(self):
        # 0x0C, vendor defined
        if self.vendor == VENDOR.SUPERMICRO:
            data = self._raw_command(0x0C, 1)
        else:
            data = None
        return data

    def temperature(self):
        # 0x8D to 0x8F
        return [self.linear11(self._raw_command(0x8d + i, 2)) for i in range(0, 3)]

    def temperature_max(self):
        # 0x0D, vendor defined
        if self.vendor == VENDOR.SUPERMICRO:
            data = self._raw_command(0x0D, 2)
        else:
            data = None
        return data

    def fanspeed(self):
        # 0x90 to 0x91
        if self.vendor == VENDOR.SUPERMICRO:
            # supermicro does RPM=(1/0.262) *(Fan Pulse Count * 60 /2), value is direct, also uses MAIN 0x0a in some psus
            data = [(1/0.262) * ((self._raw_command(0x90 + i, 2)) * 60.0/2)  for i in range(0, 2)]
        else:
            data = [self.linear11(self._raw_command(0x90 + i, 2)) for i in range(0, 2)]
        return data

    def fanspeed_low(self):
        # 0x0E, vendor defined
        if self.vendor == VENDOR.SUPERMICRO:
            data = self._raw_command(0x0E, 2)
        else:
            data = None
        return data

    def vout_mode_get(self):
        # 0x
        if self.vendor == VENDOR.SUPERMICRO:
            data = self._raw_command(0x20, 1, expt=False)
        else:
            data = self._raw_command(0x20, 1, expt=False)
        if data is None:
            raise ValueError()
        rv = [data >> 5, data & 0b00011111]
        self.vout_mode = rv[0]
        self.vout_exp = rv[1]
        return rv

    def volt_in(self):
        # 0x88
        return self.linear11(self._raw_command(0x88, 2))

    def amps_in(self):
        # 0x89
        return self.linear11(self._raw_command(0x89, 2))

    def volt_out(self):
        # 0x8B
        return self.linear16(self._raw_command(0x8B, 2), self.vout_exp)

    def amps_out(self):
        # 0x8C
        return self.linear11(self._raw_command(0x8C, 2))

    def volt_frequency(self):
        # 0x95
        return self.linear11(self._raw_command(0x95, 2))

    def power_out(self):
        # 0x96
        return self.linear11(self._raw_command(0x96, 2))

    def power_in(self):
        # 0x97
        return self.linear11(self._raw_command(0x97, 2))

    def linear11(self, data):
        exp = data >> 11
        mant = (data & 0b0000011111111111)
        return  self.twos_comp(mant, 11)*(2.0**(self.twos_comp(exp, 5)))

    def linear16(self, mant, exp):
        return  mant*(2.0**(self.twos_comp(exp, 5)))

    def twos_comp(self, val, bits):
        #compute the 2's complement of int value val
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value
        return val
