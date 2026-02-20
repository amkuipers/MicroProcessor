"""
Extension Example: Shift Operations — SHLA (33), SHRA (34)
==========================================================
This file documents what execution WOULD look like after implementing the
shift instructions described in extensions.md.
It requires those extensions to be added to MicroProcessor.py first.

Shifting left by N bits is equivalent to multiplying by 2^N.
Shifting right by N bits is equivalent to integer-dividing by 2^N.

--------------------------------------------------------------------
Implementation to add to MicroProcessor.py
--------------------------------------------------------------------

Opcode constants:
    SHLA = 33
    SHRA = 34

New methods inside MicroProcessor:
    def shl_a(self, i):
        self.reg_a <<= i
        self.zero = True if 0 == self.reg_a else False
        print(f'{self.pc:04d} SHLA {i} \t=> A {self.reg_a} ZF {self.zero}')
        self.pc += 2

    def shr_a(self, i):
        self.reg_a >>= i
        self.zero = True if 0 == self.reg_a else False
        print(f'{self.pc:04d} SHRA {i} \t=> A {self.reg_a} ZF {self.zero}')
        self.pc += 2

New elif branches inside run():
    elif instruction == SHLA:
        self.shl_a(argument)
    elif instruction == SHRA:
        self.shr_a(argument)

--------------------------------------------------------------------
Example program 1 — SHLA 1 doubles A (multiply by 2)
--------------------------------------------------------------------

Program bytes: MOVA 3, SHLA 1
  0000: MOVA  3   -- A = 3
  0002: SHLA  1   -- A <<= 1  => A = 6  (3 * 2)

Expected output:
    App: 3 3 33 1
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 3 	=> A 3 ZF False
    0002 SHLA 1 	=> A 6 ZF False
    App: 3 3 33 1
    A 6 B 0 PC 0004 ZF False

--------------------------------------------------------------------
Example program 2 — SHLA 3 multiplies A by 8 (2^3)
--------------------------------------------------------------------

Program bytes: MOVA 5, SHLA 3
  0000: MOVA  5   -- A = 5
  0002: SHLA  3   -- A <<= 3  => A = 40  (5 * 8)

Expected output:
    App: 3 5 33 3
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 5 	=> A 5 ZF False
    0002 SHLA 3 	=> A 40 ZF False
    App: 3 5 33 3
    A 40 B 0 PC 0004 ZF False

--------------------------------------------------------------------
Example program 3 — SHRA 1 halves A (integer divide by 2)
--------------------------------------------------------------------

Program bytes: MOVA 20, SHRA 1
  0000: MOVA 20   -- A = 20
  0002: SHRA  1   -- A >>= 1  => A = 10  (20 / 2)

Expected output:
    App: 3 20 34 1
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 20 	=> A 20 ZF False
    0002 SHRA 1  	=> A 10 ZF False
    App: 3 20 34 1
    A 10 B 0 PC 0004 ZF False

--------------------------------------------------------------------
Example program 4 — Compute 2^5 = 32 using SHLA
--------------------------------------------------------------------

Program bytes: MOVA 1, SHLA 5
  0000: MOVA  1   -- A = 1  (start with 2^0)
  0002: SHLA  5   -- A <<= 5  => A = 32  (1 * 2^5)

Expected output:
    App: 3 1 33 5
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 1 	=> A 1 ZF False
    0002 SHLA 5 	=> A 32 ZF False
    App: 3 1 33 5
    A 32 B 0 PC 0004 ZF False

--------------------------------------------------------------------
NOTE: This file will not run correctly until SHLA (33) and SHRA (34)
      are implemented in MicroProcessor.py.
--------------------------------------------------------------------
"""

SHLA = 33
SHRA = 34

print("ext_shift.py: SHLA/SHRA extensions are not yet implemented in MicroProcessor.py.")
print("See the docstring in this file and extensions.md for implementation details.")
print()
print("Program 1: MOVA 3,  SHLA 1  => A = 6   (3 * 2)")
print("Program 2: MOVA 5,  SHLA 3  => A = 40  (5 * 8)")
print("Program 3: MOVA 20, SHRA 1  => A = 10  (20 / 2)")
print("Program 4: MOVA 1,  SHLA 5  => A = 32  (2^5)")
