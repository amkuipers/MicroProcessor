"""
Tutorial Example: Counting Loop (0 to 3)
==========================================
Demonstrates using JZ and JNZ to implement a counting loop.

Algorithm:
  - A counts from 0 up to 3
  - CMPA 3  sets ZF=True when A equals 3
  - JZ 6    exits the loop when ZF is True
  - ADDA 1  increments the counter
  - JNZ -6  loops back to CMPA while ZF is False (A != 0, always true here)

Memory layout (byte addresses):
  0000: MOVA  0   - initialise counter
  0002: CMPA  3   - check if A == 3
  0004: JZ    6   - if equal, jump forward to end (pc 10)
  0006: ADDA  1   - increment A
  0008: JNZ  -6   - unconditional loop back to pc 2
  0010: (end)

Result: A = 3, ZF = True

Expected output:
    App: 3 0 7 3 9 6 1 1 10 -6
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 0 	=> A 0 ZF True
    0002 CMPA 3 	=> ZF False
    0004 JZ   6 	=> ZF False PC 0010
    0006 ADDA 1 	=> A 1 ZF False
    0008 JNZ  -6 	=> ZF False PC 0002
    0002 CMPA 3 	=> ZF False
    0004 JZ   6 	=> ZF False PC 0010
    0006 ADDA 1 	=> A 2 ZF False
    0008 JNZ  -6 	=> ZF False PC 0002
    0002 CMPA 3 	=> ZF False
    0004 JZ   6 	=> ZF False PC 0010
    0006 ADDA 1 	=> A 3 ZF False
    0008 JNZ  -6 	=> ZF False PC 0002
    0002 CMPA 3 	=> ZF True
    0004 JZ   6 	=> ZF True PC 0010
    App: 3 0 7 3 9 6 1 1 10 -6
    A 3 B 0 PC 0010 ZF True
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from MicroProcessor import MicroProcessor, MOVA, ADDA, CMPA, JZ, JNZ

up = MicroProcessor()

up.run([
    MOVA, 0,    # pc 0000: A = 0  (initialise counter)
    CMPA, 3,    # pc 0002: ZF = (A == 3)?
    JZ,   6,    # pc 0004: if ZF, jump to pc 0010 (end)
    ADDA, 1,    # pc 0006: A++
    JNZ, -6,    # pc 0008: loop back to pc 0002 (JNZ acts as unconditional here)
])
