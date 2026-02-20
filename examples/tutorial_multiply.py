"""
Tutorial Example: Multiplication via Repeated Addition (4 × 6 = 24)
=====================================================================
Demonstrates multiplication using a counting loop.

Algorithm:
  - A is the loop counter (counts from 0 to the multiplier)
  - B is the accumulator (adds the multiplicand each iteration)
  - When A reaches the multiplier the loop ends and B holds the product

Program computes 4 × 6 = 24.

Memory layout (byte addresses):
  0000: MOVA  0   - initialise counter A = 0
  0002: MOVB  0   - initialise accumulator B = 0
  0004: ADDA  1   - A++ (loop counter)
  0006: ADDB  6   - B += 6 (add multiplicand)
  0008: CMPA  4   - ZF = (A == 4)?  (compare to multiplier)
  0010: JNZ  -6   - loop back to pc 0004 while A != 4

Result: A = 4 (multiplier), B = 24 (product), ZF = True

Expected output:
    App: 3 0 4 0 1 1 2 6 7 4 10 -6
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 0 	=> A 0 ZF True
    0002 MOVB 0 	=> B 0 ZF True
    0004 ADDA 1 	=> A 1 ZF False
    0006 ADDB 6 	=> B 6 ZF False
    0008 CMPA 4 	=> ZF False
    0010 JNZ  -6 	=> ZF False PC 0004
    0004 ADDA 1 	=> A 2 ZF False
    0006 ADDB 6 	=> B 12 ZF False
    0008 CMPA 4 	=> ZF False
    0010 JNZ  -6 	=> ZF False PC 0004
    0004 ADDA 1 	=> A 3 ZF False
    0006 ADDB 6 	=> B 18 ZF False
    0008 CMPA 4 	=> ZF False
    0010 JNZ  -6 	=> ZF False PC 0004
    0004 ADDA 1 	=> A 4 ZF False
    0006 ADDB 6 	=> B 24 ZF False
    0008 CMPA 4 	=> ZF True
    0010 JNZ  -6 	=> ZF True PC 0004
    App: 3 0 4 0 1 1 2 6 7 4 10 -6
    A 4 B 24 PC 0012 ZF True
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from MicroProcessor import MicroProcessor, MOVA, MOVB, ADDA, ADDB, CMPA, JNZ

up = MicroProcessor()

# Compute 4 × 6 = 24
# Multiplier = 4 (how many times to add), Multiplicand = 6 (what to add each time)
up.run([
    MOVA, 0,    # pc 0000: A = 0  (loop counter)
    MOVB, 0,    # pc 0002: B = 0  (accumulator / result)
    ADDA, 1,    # pc 0004: A++
    ADDB, 6,    # pc 0006: B += 6
    CMPA, 4,    # pc 0008: ZF = (A == 4)?
    JNZ, -6,    # pc 0010: loop back to pc 0004 while A != 4
])
