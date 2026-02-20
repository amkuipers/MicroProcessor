"""
Tutorial Example: Computing a Power (2^4 = 16)
================================================
Demonstrates computing a power using repeated addition.

Because the current ISA has no register-to-register add (that would be the
ADDAB extension), we use the mathematical identity:

    2^4  =  4^2  =  4 × 4  =  16

Both expressions equal 16.  We compute 4 × 4 with the standard multiplication
loop: add 4 to B exactly 4 times.

Algorithm:
  - A is the loop counter (0 → 4)
  - B accumulates the result (adds the base each iteration)

Memory layout (byte addresses):
  0000: MOVA  0   - initialise counter A = 0
  0002: MOVB  0   - initialise result  B = 0
  0004: ADDA  1   - A++
  0006: ADDB  4   - B += 4
  0008: CMPA  4   - ZF = (A == 4)?
  0010: JNZ  -6   - loop while A != 4

Result: A = 4, B = 16 = 2^4, ZF = True

Expected output:
    App: 3 0 4 0 1 1 2 4 7 4 10 -6
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 0 	=> A 0 ZF True
    0002 MOVB 0 	=> B 0 ZF True
    0004 ADDA 1 	=> A 1 ZF False
    0006 ADDB 4 	=> B 4 ZF False
    0008 CMPA 4 	=> ZF False
    0010 JNZ  -6 	=> ZF False PC 0004
    0004 ADDA 1 	=> A 2 ZF False
    0006 ADDB 4 	=> B 8 ZF False
    0008 CMPA 4 	=> ZF False
    0010 JNZ  -6 	=> ZF False PC 0004
    0004 ADDA 1 	=> A 3 ZF False
    0006 ADDB 4 	=> B 12 ZF False
    0008 CMPA 4 	=> ZF False
    0010 JNZ  -6 	=> ZF False PC 0004
    0004 ADDA 1 	=> A 4 ZF False
    0006 ADDB 4 	=> B 16 ZF False
    0008 CMPA 4 	=> ZF True
    0010 JNZ  -6 	=> ZF True PC 0004
    App: 3 0 4 0 1 1 2 4 7 4 10 -6
    A 4 B 16 PC 0012 ZF True
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from MicroProcessor import MicroProcessor, MOVA, MOVB, ADDA, ADDB, CMPA, JNZ

up = MicroProcessor()

# Compute 2^4 = 16.
# Using the identity 2^4 = 4^2 = 4 * 4, implemented as "add 4 to B, 4 times".
up.run([
    MOVA, 0,    # pc 0000: A = 0  (loop counter)
    MOVB, 0,    # pc 0002: B = 0  (result accumulator)
    ADDA, 1,    # pc 0004: A++
    ADDB, 4,    # pc 0006: B += 4
    CMPA, 4,    # pc 0008: ZF = (A == 4)?
    JNZ, -6,    # pc 0010: loop back to pc 0004 while A != 4
])
