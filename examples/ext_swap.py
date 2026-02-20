"""
Extension Example: SWAB (opcode 19), MOVAB (opcode 20), MOVBA (opcode 21)
==========================================================================
This file documents what execution WOULD look like after implementing the
register-swap and register-copy instructions described in extensions.md.
It requires those extensions to be added to MicroProcessor.py first.

--------------------------------------------------------------------
Implementation to add to MicroProcessor.py
--------------------------------------------------------------------

Opcode constants:
    SWAB  = 19
    MOVAB = 20
    MOVBA = 21

New methods inside MicroProcessor:
    def swab(self):
        self.reg_a, self.reg_b = self.reg_b, self.reg_a
        self.zero = True if 0 == self.reg_a else False
        print(f'{self.pc:04d} SWAB   \t=> A {self.reg_a} B {self.reg_b} ZF {self.zero}')
        self.pc += 2

    def movab(self):
        self.reg_b = self.reg_a
        self.zero = True if 0 == self.reg_b else False
        print(f'{self.pc:04d} MOVAB  \t=> B {self.reg_b} ZF {self.zero}')
        self.pc += 2

    def movba(self):
        self.reg_a = self.reg_b
        self.zero = True if 0 == self.reg_a else False
        print(f'{self.pc:04d} MOVBA  \t=> A {self.reg_a} ZF {self.zero}')
        self.pc += 2

New elif branches inside run():
    elif instruction == SWAB:
        self.swab()
    elif instruction == MOVAB:
        self.movab()
    elif instruction == MOVBA:
        self.movba()

--------------------------------------------------------------------
Example program 1 — SWAB swaps A and B
--------------------------------------------------------------------

Program bytes: MOVA 10, MOVB 25, SWAB 0
  0000: MOVA 10   -- A = 10
  0002: MOVB 25   -- B = 25
  0004: SWAB  0   -- swap: A = 25, B = 10

Expected output:
    App: 3 10 4 25 19 0
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 10 	=> A 10 ZF False
    0002 MOVB 25 	=> B 25 ZF False
    0004 SWAB   	=> A 25 B 10 ZF False
    App: 3 10 4 25 19 0
    A 25 B 10 PC 0006 ZF False

--------------------------------------------------------------------
Example program 2 — MOVAB copies A into B, then SWAB restores
--------------------------------------------------------------------

Program bytes: MOVA 7, MOVAB 0, ADDA 3, SWAB 0
  0000: MOVA  7   -- A = 7
  0002: MOVAB 0   -- B = A = 7  (save a copy of A in B)
  0004: ADDA  3   -- A = 10
  0006: SWAB  0   -- A = 7 (old A from B), B = 10

Expected output:
    App: 3 7 20 0 1 3 19 0
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 7  	=> A 7 ZF False
    0002 MOVAB   	=> B 7 ZF False
    0004 ADDA 3  	=> A 10 ZF False
    0006 SWAB    	=> A 7 B 10 ZF False
    App: 3 7 20 0 1 3 19 0
    A 7 B 10 PC 0008 ZF False

--------------------------------------------------------------------
NOTE: This file will not run correctly until SWAB (19), MOVAB (20),
      and MOVBA (21) are implemented in MicroProcessor.py.
--------------------------------------------------------------------
"""

SWAB  = 19
MOVAB = 20
MOVBA = 21

print("ext_swap.py: SWAB/MOVAB/MOVBA extensions are not yet implemented in MicroProcessor.py.")
print("See the docstring in this file and extensions.md for implementation details.")
print()
print("Program 1 would swap A=10 and B=25 => A=25, B=10.")
print("Program 2 would save A=7 in B, modify A to 10, then restore => A=7, B=10.")
