#!/usr/bin/python3
from pmbus import pmbus
import argparse
try:
    b = pmbus(bus=7, address=0x78)
except ValueError:
    b = None
    pass
try:
    c = pmbus(bus=7, address=0x7A)
except ValueError:
    c = None
    pass

parser = argparse.ArgumentParser(description='Do stuff to the ipmi bus to get the pmbus data')
parser.add_argument("--temp", "-t", help="temp", action="store_true", default=False)
parser.add_argument("--fan", "-f", help="fan", action="store_true", default=False)
parser.add_argument("--input", "-i", help="input", action="store_true", default=False)
parser.add_argument("--output", "-o", help="output", action="store_true", default=False)
parser.add_argument("--power", "-p", help="power", action="store_true", default=False)

#volt_frequency = b.volt_frequency()

args = parser.parse_args()
if args.temp:
    temperature = b.temperature() if b is not None else 0
    temperature2 = c.temperature() if c is not None else 0
    print("OK: Power ok %s %s | %s %s" % (
        "%d %d" % (temperature[0], temperature[1]) if b is not None else "",
        "%d %d" % (temperature2[0], temperature2[1]) if c is not None else "",
        "Temp1=%dC Temp2=%dC" % (temperature[0], temperature[1]) if b is not None else "",
        "Temp3=%dC Temp4=%dC" % (temperature2[0], temperature2[1]) if c is not None else ""))
if args.fan:
    fanspeed = b.fanspeed() if b is not None else 0
    fanspeed2 = c.fanspeed() if c is not None else 0
    print("OK: Power ok %s %s | %s %s" % (
            "%d" % (fanspeed[0]) if b is not None else "",
            "%d" % (fanspeed2[0]) if c is not None else "",
            "Fan1=%dRPM" % (fanspeed[0]) if b is not None else "",
            "Fan2=%dRPM" % (fanspeed2[0]) if c is not None else "",
            )
         )
if args.input:
    volt_in = b.volt_in() if b is not None else 0
    volt2_in = c.volt_in() if c is not None else 0
    amps_in = b.amps_in() if b is not None else 0
    amps2_in = c.amps_in() if c is not None else 0
    print("OK: Power ok %s %s | %s %s " % (
        "1: %0.1fV %0.1fA" % (volt_in, amps_in) if b is not None else "",
        "2: %0.1fV %0.1fA" % (volt2_in, amps2_in) if c is not None else "",
        "Volt1_In=%0.1fV Amps1_In=%0.1fA" % (volt_in, amps_in) if b is not None else "",
        "Volt2_In=%0.1fV Amps2_In=%0.1fA" % (volt2_in, amps2_in) if c is not None else ""))
if args.output:
    volt_out = b.volt_out() if b is not None else 0
    volt2_out = c.volt_out() if c is not None else 0
    amps_out = b.amps_out() if b is not None else 0
    amps2_out = c.amps_out() if c is not None else 0
    print("OK: Power ok %s %s | %s %s " % (
        "1: %0.1fV %0.1fA" % (volt_out, amps_out) if b is not None else "",
        "2: %0.1fV %0.1fA" % (volt2_out, amps2_out) if c is not None else "",
        "Volt1_Out=%0.1fV Amps1_Out=%0.1fA" % (volt_out, amps_out) if b is not None else "",
        "Volt2_Out=%0.1fV Amps2_Out=%0.1fA" % (volt2_out, amps2_out) if c is not None else ""))
if args.power:
    power_in = b.power_in() if b is not None else 0
    power_out = b.power_out() if b is not None else 0
    diff = power_in - power_out if b is not None else 0
    eff = (power_out / power_in) * 100.0 if b is not None else 0
    power2_in = c.power_in() if c is not None else 0
    power2_out = c.power_out() if c is not None else 0
    diff2 = power2_in - power2_out if c is not None else 0
    eff2 = (power2_out / power2_in) * 100.0 if c is not None else 0
    print("OK: Power ok %s %s | %s %s" % (
        "In1: %0.1fW Out1: %0.1fW Diff1: %0.1fW Efficiency1: %0.1f%%" % (power_in, power_out, diff, eff) if b is not None else "",
        "In2: %0.1fW Out2: %0.1fW Diff2: %0.1fW Efficiency2: %0.1f%%" % (power2_in, power2_out, diff2, eff2) if c is not None else "",
        "Power_In=%0.1fW Power_Out=%0.1fW Power_diff=%0.1fW Efficiency=%0.1f%%" % (power_in, power_out, diff, eff) if b is not None else "",
        "Power2_In=%0.1fW Power2_Out=%0.1fW Power2_diff=%0.1fW Efficiency2=%0.1f%%" % (power2_in, power2_out, diff2, eff2) if c is not None else ""))

exit(0)
