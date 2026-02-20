"""
Extension Example: Register-to-Register Operations
====================================================
Demonstrates ADDAB (22), ADDBA (23), SUBAB (24), SUBBA (25), CMPAB (26).
These instructions operate on both registers without an immediate argument.

This file requires those extensions to be added to MicroProcessor.py first.

--------------------------------------------------------------------
Implementation to add to MicroProcessor.py
--------------------------------------------------------------------

Opcode constants:
    ADDAB = 22   # B = B + A
    ADDBA = 23   # A = A + B
    SUBAB = 24   # B = B - A
    SUBBA = 25   # A = A - B
    CMPAB = 26   # ZF = (A == B)

New methods inside MicroProcessor:
    def addab(self):
        self.reg_b += self.reg_a
        self.zero = True if 0 == self.reg_b else False
        print(f'{self.pc:04d} ADDAB  \t=> B {self.reg_b} ZF {self.zero}')
        self.pc += 2

    def addba(self):
        self.reg_a += self.reg_b
        self.zero = True if 0 == self.reg_a else False
        print(f'{self.pc:04d} ADDBA  \t=> A {self.reg_a} ZF {self.zero}')
        self.pc += 2

    def subab(self):
        self.reg_b -= self.reg_a
        self.zero = True if 0 == self.reg_b else False
        print(f'{self.pc:04d} SUBAB  \t=> B {self.reg_b} ZF {self.zero}')
        self.pc += 2

    def subba(self):
        self.reg_a -= self.reg_b
        self.zero = True if 0 == self.reg_a else False
        print(f'{self.pc:04d} SUBBA  \t=> A {self.reg_a} ZF {self.zero}')
        self.pc += 2

    def cmpab(self):
        self.zero = True if self.reg_a == self.reg_b else False
        print(f'{self.pc:04d} CMPAB  \t=> ZF {self.zero}')
        self.pc += 2

New elif branches inside run():
    elif instruction == ADDAB:
        self.addab()
    elif instruction == ADDBA:
        self.addba()
    elif instruction == SUBAB:
        self.subab()
    elif instruction == SUBBA:
        self.subba()
    elif instruction == CMPAB:
        self.cmpab()

--------------------------------------------------------------------
Example program 1 — ADDAB accumulates A into B (doubling B with ADDAB)
--------------------------------------------------------------------

Program bytes: MOVA 5, MOVB 10, ADDAB 0
  0000: MOVA  5   -- A = 5
  0002: MOVB 10   -- B = 10
  0004: ADDAB 0   -- B = B + A = 15

Expected output:
    App: 3 5 4 10 22 0
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 5  	=> A 5 ZF False
    0002 MOVB 10 	=> B 10 ZF False
    0004 ADDAB   	=> B 15 ZF False
    App: 3 5 4 10 22 0
    A 5 B 15 PC 0006 ZF False

--------------------------------------------------------------------
Example program 2 — SUBAB computes B - A
--------------------------------------------------------------------

Program bytes: MOVA 3, MOVB 10, SUBAB 0
  0000: MOVA  3   -- A = 3
  0002: MOVB 10   -- B = 10
  0004: SUBAB 0   -- B = B - A = 7

Expected output:
    App: 3 3 4 10 24 0
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 3  	=> A 3 ZF False
    0002 MOVB 10 	=> B 10 ZF False
    0004 SUBAB   	=> B 7 ZF False
    App: 3 3 4 10 24 0
    A 3 B 7 PC 0006 ZF False

--------------------------------------------------------------------
Example program 3 — CMPAB checks whether A == B
--------------------------------------------------------------------

Program bytes: MOVA 7, MOVB 7, CMPAB 0
  0000: MOVA  7   -- A = 7
  0002: MOVB  7   -- B = 7
  0004: CMPAB 0   -- ZF = (A == B) = True

Expected output:
    App: 3 7 4 7 26 0
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 7 	=> A 7 ZF False
    0002 MOVB 7 	=> B 7 ZF False
    0004 CMPAB  	=> ZF True
    App: 3 7 4 7 26 0
    A 7 B 7 PC 0006 ZF True

--------------------------------------------------------------------
Example program 4 — SUBBA computes A - B, useful for finding difference
--------------------------------------------------------------------

Program bytes: MOVA 15, MOVB 6, SUBBA 0
  0000: MOVA 15   -- A = 15
  0002: MOVB  6   -- B = 6
  0004: SUBBA 0   -- A = A - B = 9

Expected output:
    App: 3 15 4 6 25 0
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 15 	=> A 15 ZF False
    0002 MOVB 6  	=> B 6 ZF False
    0004 SUBBA   	=> A 9 ZF False
    App: 3 15 4 6 25 0
    A 9 B 6 PC 0006 ZF False

--------------------------------------------------------------------
NOTE: This file will not run correctly until ADDAB (22), ADDBA (23),
      SUBAB (24), SUBBA (25), and CMPAB (26) are implemented in
      MicroProcessor.py.
--------------------------------------------------------------------
"""

ADDAB = 22
ADDBA = 23
SUBAB = 24
SUBBA = 25
CMPAB = 26

print("ext_register_ops.py: ADDAB/ADDBA/SUBAB/SUBBA/CMPAB extensions are not yet")
print("implemented in MicroProcessor.py.")
print("See the docstring in this file and extensions.md for implementation details.")
print()
print("Program 1: MOVA 5,  MOVB 10, ADDAB  => B = 15  (B = B + A)")
print("Program 2: MOVA 3,  MOVB 10, SUBAB  => B = 7   (B = B - A)")
print("Program 3: MOVA 7,  MOVB 7,  CMPAB  => ZF=True (A == B)")
print("Program 4: MOVA 15, MOVB 6,  SUBBA  => A = 9   (A = A - B)")
