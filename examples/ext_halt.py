"""
Extension Example: HALT (opcode 12)
=====================================
This file documents what execution WOULD look like after implementing the HALT
instruction as described in extensions.md.  It requires the extension to be
added to MicroProcessor.py before it can be run as-is.

HALT stops the run loop immediately and cleanly.  Without it, programs run
until the PC walks off the end of the program array.

--------------------------------------------------------------------
Implementation to add to MicroProcessor.py
--------------------------------------------------------------------

Opcode constant (at top of file):
    HALT = 12

New method inside MicroProcessor:
    def halt(self):
        print(f'{self.pc:04d} HALT   \t=> stopping execution')
        self.pc = len(self.app)   # move PC past end to exit the while loop

New elif branch inside run():
    elif instruction == HALT:
        self.halt()

--------------------------------------------------------------------
Example program 1 — HALT stops a loop after 2 iterations
--------------------------------------------------------------------

Program bytes: MOVA 0, ADDA 1, CMPA 2, JNZ -4, HALT 0
  0000: MOVA  0
  0002: ADDA  1   <-- loop start
  0004: CMPA  2
  0006: JNZ  -4   -- jumps back to 0002 while A != 2
  0008: HALT  0   -- stops execution cleanly

Expected output:
    App: 3 0 1 1 7 2 10 -4 12 0
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 0 	=> A 0 ZF True
    0002 ADDA 1 	=> A 1 ZF False
    0004 CMPA 2 	=> ZF False
    0006 JNZ  -4 	=> ZF False PC 0002
    0002 ADDA 1 	=> A 2 ZF False
    0004 CMPA 2 	=> ZF True
    0006 JNZ  -4 	=> ZF True PC 0002
    0008 HALT   	=> stopping execution
    App: 3 0 1 1 7 2 10 -4 12 0
    A 2 B 0 PC 0010 ZF True

--------------------------------------------------------------------
Example program 2 — HALT in the middle of a longer program
--------------------------------------------------------------------

Program bytes: MOVA 5, MOVB 3, HALT 0, ADDA 99, ADDB 99
  0000: MOVA  5
  0002: MOVB  3
  0004: HALT  0   -- stops here; instructions at 0006 and 0008 never execute
  0006: ADDA 99   (unreachable)
  0008: ADDB 99   (unreachable)

Expected output:
    App: 3 5 4 3 12 0 1 99 2 99
    A 0 B 0 PC 0000 ZF True
    0000 MOVA 5 	=> A 5 ZF False
    0002 MOVB 3 	=> B 3 ZF False
    0004 HALT   	=> stopping execution
    App: 3 5 4 3 12 0 1 99 2 99
    A 5 B 3 PC 0010 ZF False

--------------------------------------------------------------------
NOTE: This file will not run correctly until HALT (opcode 12) is
      implemented in MicroProcessor.py.  With the unmodified code,
      opcode 12 falls through to the NOP else-branch, and execution
      continues past the intended halt point.
--------------------------------------------------------------------
"""

# Opcode constant (define locally to allow this file to be read without
# modifying MicroProcessor.py, but the run() call is commented out).
HALT = 12

print("ext_halt.py: HALT extension is not yet implemented in MicroProcessor.py.")
print("See the docstring in this file and extensions.md for implementation details.")
print()
print("Program 1 would compute: A=2 before halting.")
print("Program 2 would compute: A=5, B=3 before halting (skipping ADDA 99, ADDB 99).")
