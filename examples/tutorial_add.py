"""
Tutorial Example: Simple Load and Add
======================================
Demonstrates loading a value into register A and adding an immediate value.

Program: MOVA 10, ADDA 5
Result:  A = 15

Expected output:
    App: 3 10 1 5
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 10 	=> A 10 ZF False
    0002 ADDA 5 	=> A 15 ZF False
    App: 3 10 1 5
    A 15 B 0 PC 0004 ZF False
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from MicroProcessor import MicroProcessor, MOVA, ADDA

up = MicroProcessor()

up.run([
    MOVA, 10,   # Load 10 into register A
    ADDA, 5,    # Add 5 to register A  => A = 15
])
