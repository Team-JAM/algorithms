#!/usr/bin/env python3

"""Decoder ls8 for mining loop"""

import sys
from loop_cpu import CPU

program = 'wishing_well.ls8'

def decode():
    cpu = CPU()

    cpu.load(program)
    return cpu.run()