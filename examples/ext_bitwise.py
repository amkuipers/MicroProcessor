"""
Extension Example: Bitwise Operations — ANDA (30), ORA (31), XORA (32)
=======================================================================
This file documents what execution WOULD look like after implementing the
bitwise instructions described in extensions.md.
It requires those extensions to be added to MicroProcessor.py first.

--------------------------------------------------------------------
Implementation to add to MicroProcessor.py
--------------------------------------------------------------------

Opcode constants:
    ANDA = 30
    ORA  = 31
    XORA = 32

New methods inside MicroProcessor:
    def and_a(self, i):
        self.reg_a &= i
        self.zero = True if 0 == self.reg_a else False
        print(f'{self.pc:04d} ANDA {i} \t=> A {self.reg_a} ZF {self.zero}')
        self.pc += 2

    def or_a(self, i):
        self.reg_a |= i
        self.zero = True if 0 == self.reg_a else False
        print(f'{self.pc:04d} ORA  {i} \t=> A {self.reg_a} ZF {self.zero}')
        self.pc += 2

    def xor_a(self, i):
        self.reg_a ^= i
        self.zero = True if 0 == self.reg_a else False
        print(f'{self.pc:04d} XORA {i} \t=> A {self.reg_a} ZF {self.zero}')
        self.pc += 2

New elif branches inside run():
    elif instruction == ANDA:
        self.and_a(argument)
    elif instruction == ORA:
        self.or_a(argument)
    elif instruction == XORA:
        self.xor_a(argument)

--------------------------------------------------------------------
Example program 1 — ANDA isolates the lower 4 bits (nibble mask)
--------------------------------------------------------------------

Program bytes: MOVA 0b10110101 (=181), ANDA 0b00001111 (=15)
  0000: MOVA 181  -- A = 0b10110101
  0002: ANDA  15  -- A &= 0b00001111  => A = 0b00000101 = 5

Expected output:
    App: 3 181 30 15
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 181 	=> A 181 ZF False
    0002 ANDA 15  	=> A 5 ZF False
    App: 3 181 30 15
    A 5 B 0 PC 0004 ZF False

--------------------------------------------------------------------
Example program 2 — XORA clears A (XOR with itself pattern via ORA first)
--------------------------------------------------------------------

Program bytes: MOVA 42, XORA 42
  0000: MOVA  42  -- A = 42
  0002: XORA  42  -- A ^= 42  => A = 0  (XOR with self = 0)

Expected output:
    App: 3 42 32 42
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 42 	=> A 42 ZF False
    0002 XORA 42 	=> A 0 ZF True
    App: 3 42 32 42
    A 0 B 0 PC 0004 ZF True

--------------------------------------------------------------------
Example program 3 — ORA sets specific bits
--------------------------------------------------------------------

Program bytes: MOVA 0b00001100 (=12), ORA 0b00110000 (=48)
  0000: MOVA  12  -- A = 0b00001100
  0002: ORA   48  -- A |= 0b00110000  => A = 0b00111100 = 60

Expected output:
    App: 3 12 31 48
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 12 	=> A 12 ZF False
    0002 ORA  48 	=> A 60 ZF False
    App: 3 12 31 48
    A 60 B 0 PC 0004 ZF False

--------------------------------------------------------------------
NOTE: This file will not run correctly until ANDA (30), ORA (31),
      and XORA (32) are implemented in MicroProcessor.py.
--------------------------------------------------------------------
"""

ANDA = 30
ORA  = 31
XORA = 32

print("ext_bitwise.py: ANDA/ORA/XORA extensions are not yet implemented in MicroProcessor.py.")
print("See the docstring in this file and extensions.md for implementation details.")
print()
print("Program 1: MOVA 181, ANDA 15  => A = 5  (lower nibble mask)")
print("Program 2: MOVA 42,  XORA 42  => A = 0  (XOR-self clears register)")
print("Program 3: MOVA 12,  ORA  48  => A = 60 (set bits 4 and 5)")
