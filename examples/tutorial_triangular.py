"""
Tutorial Example: Triangular Number T(5) = 15
===============================================
Demonstrates computing the 5th triangular number using repeated addition.

A triangular number T(N) = 1 + 2 + 3 + ... + N.

Using the closed-form formula:
    T(N) = N × (N + 1) / 2

For N = 5:
    T(5) = 5 × 6 / 2 = 5 × 3 = 15

We compute 5 × 3 = 15 using the multiplication loop:
  - A is the loop counter (0 → 5)
  - B accumulates the result (adds 3 each iteration)

Memory layout (byte addresses):
  0000: MOVA  0   - initialise counter A = 0
  0002: MOVB  0   - initialise result  B = 0
  0004: ADDA  1   - A++
  0006: ADDB  3   - B += 3  (the value (N+1)/2 = 6/2 = 3)
  0008: CMPA  5   - ZF = (A == 5)?  (loop N = 5 times)
  0010: JNZ  -6   - loop while A != 5

Result: A = 5, B = 15 = T(5), ZF = True

Expected output:
    App: 3 0 4 0 1 1 2 3 7 5 10 -6
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 0 	=> A 0 ZF True
    0002 MOVB 0 	=> B 0 ZF True
    0004 ADDA 1 	=> A 1 ZF False
    0006 ADDB 3 	=> B 3 ZF False
    0008 CMPA 5 	=> ZF False
    0010 JNZ  -6 	=> ZF False PC 0004
    0004 ADDA 1 	=> A 2 ZF False
    0006 ADDB 3 	=> B 6 ZF False
    0008 CMPA 5 	=> ZF False
    0010 JNZ  -6 	=> ZF False PC 0004
    0004 ADDA 1 	=> A 3 ZF False
    0006 ADDB 3 	=> B 9 ZF False
    0008 CMPA 5 	=> ZF False
    0010 JNZ  -6 	=> ZF False PC 0004
    0004 ADDA 1 	=> A 4 ZF False
    0006 ADDB 3 	=> B 12 ZF False
    0008 CMPA 5 	=> ZF False
    0010 JNZ  -6 	=> ZF False PC 0004
    0004 ADDA 1 	=> A 5 ZF False
    0006 ADDB 3 	=> B 15 ZF False
    0008 CMPA 5 	=> ZF True
    0010 JNZ  -6 	=> ZF True PC 0004
    App: 3 0 4 0 1 1 2 3 7 5 10 -6
    A 5 B 15 PC 0012 ZF True
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from MicroProcessor import MicroProcessor, MOVA, MOVB, ADDA, ADDB, CMPA, JNZ

up = MicroProcessor()

# Compute T(5) = 1+2+3+4+5 = 15.
# Using T(N) = N*(N+1)/2 = 5*3 = 15, implemented as "add 3 to B, 5 times".
up.run([
    MOVA, 0,    # pc 0000: A = 0  (loop counter)
    MOVB, 0,    # pc 0002: B = 0  (result accumulator)
    ADDA, 1,    # pc 0004: A++
    ADDB, 3,    # pc 0006: B += 3  (= (N+1)/2 = 3)
    CMPA, 5,    # pc 0008: ZF = (A == 5)?
    JNZ, -6,    # pc 0010: loop back to pc 0004 while A != 5
])
