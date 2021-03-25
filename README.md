# Introduction
Tool to output PMBus data from a supermicro 1U PSU on a Supermicro motherboard to nagios. Does not support warning/error as of now.

You should validate the bus and alter it in code. This might be different per board. (tested on a X10SRH with a PWS-721P-1R)

# Usage
```
usage: run.py [-h] [--temp] [--fan] [--input] [--output] [--power]

Do stuff to the ipmi bus to get the pmbus data

optional arguments:
  -h, --help    show this help message and exit
  --temp, -t    temp
  --fan, -f     fan
  --input, -i   input
  --output, -o  output
  --power, -p   power

```
