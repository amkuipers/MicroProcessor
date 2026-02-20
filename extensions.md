# MicroProcessor Extensions Guide

A step-by-step guide to extending the MicroProcessor simulator with new
RISC-style instructions.

---

## Table of Contents

1. [How to Add Any New Instruction](#how-to-add-any-new-instruction)
2. [RISC vs CISC Philosophy](#risc-vs-cisc-philosophy)
3. [Backward Compatibility](#backward-compatibility)
4. [Testing Methodology](#testing-methodology)
5. [New Instructions (opcodes 11–34)](#new-instructions)
   - [NOP (11)](#1-nop--opcode-11)
   - [HALT (12)](#2-halt--opcode-12)
   - [INCA (13)](#3-inca--opcode-13)
   - [INCB (14)](#4-incb--opcode-14)
   - [DECA (15)](#5-deca--opcode-15)
   - [DECB (16)](#6-decb--opcode-16)
   - [CLRA (17)](#7-clra--opcode-17)
   - [CLRB (18)](#8-clrb--opcode-18)
   - [SWAB (19)](#9-swab--opcode-19)
   - [MOVAB (20)](#10-movab--opcode-20)
   - [MOVBA (21)](#11-movba--opcode-21)
   - [ADDAB (22)](#12-addab--opcode-22)
   - [ADDBA (23)](#13-addba--opcode-23)
   - [SUBAB (24)](#14-subab--opcode-24)
   - [SUBBA (25)](#15-subba--opcode-25)
   - [CMPAB (26)](#16-cmpab--opcode-26)
   - [NEGA (27)](#17-nega--opcode-27)
   - [NEGB (28)](#18-negb--opcode-28)
   - [JMP (29)](#19-jmp--opcode-29)
   - [ANDA (30)](#20-anda--opcode-30)
   - [ORA (31)](#21-ora--opcode-31)
   - [XORA (32)](#22-xora--opcode-32)
   - [SHLA (33)](#23-shla--opcode-33)
   - [SHRA (34)](#24-shra--opcode-34)

---

## How to Add Any New Instruction

Every new instruction requires **three changes** to `MicroProcessor.py`:

### Step 1 — Add the opcode constant

At the top of the file, after the existing constants:

```python
# existing
JNZ = 10

# new
MY_INSTR = 11   # choose the next available opcode number
```

### Step 2 — Add the handler method

Inside the `MicroProcessor` class, add a new method.  Follow the existing
style:

```python
def my_instr(self, argument):
    # perform the operation
    self.reg_a = ...
    # update the zero flag if the operation changes a register
    self.zero = True if 0 == self.reg_a else False
    # print the trace line
    print(f'{self.pc:04d} MYINSTR {argument} \t=> A {self.reg_a} ZF {self.zero}')
    # always advance the program counter by 2
    self.pc += 2
```

For instructions that do not use the argument, still accept it (to match the
2-byte format) but ignore it and print a fixed trace without the argument.

### Step 3 — Add the `elif` branch in `run()`

Inside the `while` loop of `run()`, add:

```python
elif instruction == MY_INSTR:
    self.my_instr(argument)
```

Place it before the final `else` (NOP/unknown opcode) branch.

---

## RISC vs CISC Philosophy

**RISC** (Reduced Instruction Set Computer) favours:
- Few, simple instructions that each do one thing
- Fixed-width instruction encoding (this simulator uses 2 bytes throughout)
- Operations on registers rather than memory
- Composability — complex operations built from simple ones

**CISC** (Complex Instruction Set Computer) favours complex instructions that
do many things in one step (e.g. a single MUL instruction that multiplies two
registers and stores the result).

All 24 new instructions in this guide follow RISC principles:
- Each instruction performs exactly one conceptual operation
- The 2-byte fixed format is preserved
- Instructions are orthogonal (each can be combined freely with others)
- No instruction has side effects beyond its documented register/flag changes

---

## Backward Compatibility

- New opcodes (11+) do not conflict with existing opcodes (1–10).
- Programs written for the original 10-instruction set continue to work
  unchanged because the new `elif` branches are only reached for the new
  opcode values.
- Opcode 0 still causes an infinite loop (a known quirk of the base code).
- The unknown-opcode NOP behaviour (the `else` branch) still applies to any
  opcode not explicitly handled.

---

## Testing Methodology

After implementing each new instruction:

1. **Smoke test**: run a minimal program that uses only the new instruction and
   verify the trace output and final register/flag state manually.
2. **Edge cases**: test with argument 0 (should often set ZF=True), with large
   values, and with negative values where applicable.
3. **Combination test**: write a program that mixes the new instruction with
   existing ones and verify the interaction.
4. **Regression test**: re-run the original 5×5 multiplication demo
   (`python MicroProcessor.py`) and confirm it still produces the same output.

---

## New Instructions

---

### 1. NOP — opcode 11

**Motivation**: Every processor needs a no-operation instruction for padding
program memory, inserting timing delays, or reserving space for future code.

**RISC justification**: The simplest possible instruction; keeps timing
predictable and enables structural uniformity in program layouts.

**Opcode constant**:
```python
NOP = 11
```

**Handler method**:
```python
def nop(self, argument):
    print(f'{self.pc:04d} NOP    \t=> (no operation)')
    self.pc += 2
```

**`elif` branch in `run()`**:
```python
elif instruction == NOP:
    self.nop(argument)
```

**Example 1** — Use NOP as padding between instructions:
```python
up.run([
    MOVA, 5,    # pc 0000: A = 5
    NOP,  0,    # pc 0002: do nothing
    ADDA, 3,    # pc 0004: A = 8
])
# Expected: A = 8, B = 0
```

Expected trace:
```
App: 3 5 11 0 1 3
A 0 B 0 PC 0000 ZF True
0000 MOVA 5 	=> A 5 ZF False
0002 NOP    	=> (no operation)
0004 ADDA 3 	=> A 8 ZF False
App: 3 5 11 0 1 3
A 8 B 0 PC 0006 ZF False
```

**Example 2** — Multiple NOPs (e.g. reserving space):
```python
up.run([
    MOVB, 10,   # pc 0000: B = 10
    NOP,  0,    # pc 0002
    NOP,  0,    # pc 0004
    ADDB, 5,    # pc 0006: B = 15
])
# Expected: B = 15
```

---

### 2. HALT — opcode 12

**Motivation**: Without HALT, a program ends only when the PC walks off the
end of the array.  HALT provides an explicit, readable stopping point and
allows unreachable code to safely follow the halt point.

**RISC justification**: Essential control-flow primitive; every real processor
has a stop/idle instruction.

**Opcode constant**:
```python
HALT = 12
```

**Handler method**:
```python
def halt(self, argument):
    print(f'{self.pc:04d} HALT   \t=> stopping execution')
    self.pc = len(self.app)   # move PC past end to exit the while loop
```

**`elif` branch in `run()`**:
```python
elif instruction == HALT:
    self.halt(argument)
```

**Example 1** — HALT after computing a result:
```python
up.run([
    MOVA, 0,    # pc 0000
    MOVB, 0,    # pc 0002
    ADDA, 1,    # pc 0004  <-- loop start
    ADDB, 5,    # pc 0006
    CMPA, 3,    # pc 0008
    JNZ, -6,    # pc 0010: loop back to pc 0004 while A != 3
    HALT, 0,    # pc 0012: stop cleanly
])
# Expected: A = 3, B = 15
```

Expected trace (partial):
```
...
0010 JNZ  -6 	=> ZF True PC 0004
0012 HALT   	=> stopping execution
App: ...
A 3 B 15 PC 0014 ZF True
```

**Example 2** — HALT prevents unreachable instructions from running:
```python
up.run([
    MOVA, 7,    # pc 0000: A = 7
    HALT, 0,    # pc 0002: stop here
    MOVA, 99,   # pc 0004: never reached
])
# Expected: A = 7  (not 99)
```

See also: `examples/ext_halt.py`

---

### 3. INCA — opcode 13

**Motivation**: Incrementing a register by 1 is the most common loop-counter
operation.  `ADDA 1` works but wastes the argument byte.

**RISC justification**: Common idiom; a dedicated opcode makes programs
shorter and more readable.

**Opcode constant**:
```python
INCA = 13
```

**Handler method**:
```python
def inc_a(self, argument):
    self.reg_a += 1
    self.zero = True if 0 == self.reg_a else False
    print(f'{self.pc:04d} INCA   \t=> A {self.reg_a} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == INCA:
    self.inc_a(argument)
```

**Example 1** — Simple increment:
```python
up.run([MOVA, 4, INCA, 0])
# Expected: A = 5
```

Expected trace:
```
0000 MOVA 4 	=> A 4 ZF False
0002 INCA   	=> A 5 ZF False
```

**Example 2** — Counting loop using INCA:
```python
up.run([
    MOVA,  0,   # pc 0000
    INCA,  0,   # pc 0002  <-- loop start
    CMPA, 10,   # pc 0004
    JNZ,  -4,   # pc 0006: back to 0002
])
# Expected: A = 10
```

---

### 4. INCB — opcode 14

**Motivation**: Symmetric counterpart to INCA for register B.

**RISC justification**: Orthogonality — every A operation should have a B
equivalent.

**Opcode constant**:
```python
INCB = 14
```

**Handler method**:
```python
def inc_b(self, argument):
    self.reg_b += 1
    self.zero = True if 0 == self.reg_b else False
    print(f'{self.pc:04d} INCB   \t=> B {self.reg_b} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == INCB:
    self.inc_b(argument)
```

**Example 1** — Increment B:
```python
up.run([MOVB, 9, INCB, 0])
# Expected: B = 10
```

**Example 2** — Use INCA and INCB to increment both registers:
```python
up.run([MOVA, 3, MOVB, 7, INCA, 0, INCB, 0])
# Expected: A = 4, B = 8
```

---

### 5. DECA — opcode 15

**Motivation**: Decrement for countdown loops.  `SUBA 1` works but the trace
prints `ADDA -1`, which is confusing.  DECA is explicit and clear.

**RISC justification**: Symmetric to INCA; critical for countdown loops and
stack-pointer management in more advanced architectures.

**Opcode constant**:
```python
DECA = 15
```

**Handler method**:
```python
def dec_a(self, argument):
    self.reg_a -= 1
    self.zero = True if 0 == self.reg_a else False
    print(f'{self.pc:04d} DECA   \t=> A {self.reg_a} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == DECA:
    self.dec_a(argument)
```

**Example 1** — Countdown from 3 to 0:
```python
up.run([
    MOVA,  3,   # pc 0000: A = 3
    DECA,  0,   # pc 0002: A--      <-- loop start
    JNZ,  -2,   # pc 0004: loop back to 0002 while A != 0
])
# Expected: A = 0, ZF = True
```

Expected trace:
```
0000 MOVA 3 	=> A 3 ZF False
0002 DECA   	=> A 2 ZF False
0004 JNZ  -2 	=> ZF False PC 0002
0002 DECA   	=> A 1 ZF False
0004 JNZ  -2 	=> ZF False PC 0002
0002 DECA   	=> A 0 ZF True
0004 JNZ  -2 	=> ZF True PC 0002
```

**Example 2** — DECA sets ZF when A reaches 0:
```python
up.run([MOVA, 1, DECA, 0])
# Expected: A = 0, ZF = True
```

---

### 6. DECB — opcode 16

**Motivation**: Symmetric counterpart to DECA.

**Opcode constant**:
```python
DECB = 16
```

**Handler method**:
```python
def dec_b(self, argument):
    self.reg_b -= 1
    self.zero = True if 0 == self.reg_b else False
    print(f'{self.pc:04d} DECB   \t=> B {self.reg_b} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == DECB:
    self.dec_b(argument)
```

**Example 1**:
```python
up.run([MOVB, 5, DECB, 0, DECB, 0])
# Expected: B = 3
```

**Example 2** — Countdown using DECB:
```python
up.run([
    MOVB,  4,
    DECB,  0,   # <-- loop start
    JNZ,  -2,   # loop while B != 0
])
# Expected: B = 0, ZF = True
```

---

### 7. CLRA — opcode 17

**Motivation**: Clearing a register to zero is very common.  `MOVA 0` works
but CLRA is shorter and more expressive.

**RISC justification**: Single-purpose, fast register-clear; common in
interrupt handlers and loop initialisations.

**Opcode constant**:
```python
CLRA = 17
```

**Handler method**:
```python
def clr_a(self, argument):
    self.reg_a = 0
    self.zero = True
    print(f'{self.pc:04d} CLRA   \t=> A 0 ZF True')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == CLRA:
    self.clr_a(argument)
```

**Example 1** — Clear A after use:
```python
up.run([MOVA, 42, CLRA, 0])
# Expected: A = 0, ZF = True
```

**Example 2** — Reset A to restart a loop:
```python
up.run([MOVA, 99, ADDA, 1, CLRA, 0, ADDA, 5])
# Expected: A = 5 (cleared to 0 then 5 added)
```

---

### 8. CLRB — opcode 18

**Motivation**: Symmetric counterpart to CLRA.

**Opcode constant**:
```python
CLRB = 18
```

**Handler method**:
```python
def clr_b(self, argument):
    self.reg_b = 0
    self.zero = True
    print(f'{self.pc:04d} CLRB   \t=> B 0 ZF True')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == CLRB:
    self.clr_b(argument)
```

**Example 1**:
```python
up.run([MOVB, 100, CLRB, 0])
# Expected: B = 0
```

**Example 2** — Clear accumulator before multiply:
```python
up.run([
    CLRA, 0,    # pc 0000: A = 0 (counter)
    CLRB, 0,    # pc 0002: B = 0 (accumulator)
    ADDA, 1,    # pc 0004: A++
    ADDB, 7,    # pc 0006: B += 7
    CMPA, 3,    # pc 0008
    JNZ, -6,    # pc 0010
])
# Expected: A = 3, B = 21
```

---

### 9. SWAB — opcode 19

**Motivation**: Swapping A and B is needed whenever you want to save the
result of one computation into the other register before overwriting it.

**RISC justification**: Essential for two-register architectures; without swap,
many algorithms require extra copies via memory.

**Opcode constant**:
```python
SWAB = 19
```

**Handler method**:
```python
def swab(self, argument):
    self.reg_a, self.reg_b = self.reg_b, self.reg_a
    self.zero = True if 0 == self.reg_a else False
    print(f'{self.pc:04d} SWAB   \t=> A {self.reg_a} B {self.reg_b} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == SWAB:
    self.swab(argument)
```

**Example 1** — Swap A and B:
```python
up.run([MOVA, 10, MOVB, 25, SWAB, 0])
# Expected: A = 25, B = 10
```

Expected trace:
```
0000 MOVA 10 	=> A 10 ZF False
0002 MOVB 25 	=> B 25 ZF False
0004 SWAB   	=> A 25 B 10 ZF False
```

**Example 2** — Use SWAB to move multiply result from B back to A:
```python
up.run([
    MOVA, 0, MOVB, 0,
    ADDA, 1, ADDB, 4, CMPA, 3, JNZ, -6,   # B = 3*4 = 12
    SWAB, 0,   # A = 12 (result), B = 3 (old counter)
])
# Expected: A = 12, B = 3
```

See also: `examples/ext_swap.py`

---

### 10. MOVAB — opcode 20

**Motivation**: Copy A into B without disturbing A.  Needed before operations
that overwrite one register while the other must be preserved.

**RISC justification**: Register-to-register move is fundamental; avoids using
a memory location as a temporary.

**Opcode constant**:
```python
MOVAB = 20
```

**Handler method**:
```python
def movab(self, argument):
    self.reg_b = self.reg_a
    self.zero = True if 0 == self.reg_b else False
    print(f'{self.pc:04d} MOVAB  \t=> B {self.reg_b} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == MOVAB:
    self.movab(argument)
```

**Example 1** — Copy A into B:
```python
up.run([MOVA, 7, MOVAB, 0])
# Expected: A = 7, B = 7
```

**Example 2** — Save A in B before modifying A, then restore with SWAB:
```python
up.run([MOVA, 7, MOVAB, 0, ADDA, 3, SWAB, 0])
# Expected: A = 7 (restored), B = 10 (modified value)
```

---

### 11. MOVBA — opcode 21

**Motivation**: Symmetric counterpart to MOVAB (copy B into A).

**Opcode constant**:
```python
MOVBA = 21
```

**Handler method**:
```python
def movba(self, argument):
    self.reg_a = self.reg_b
    self.zero = True if 0 == self.reg_a else False
    print(f'{self.pc:04d} MOVBA  \t=> A {self.reg_a} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == MOVBA:
    self.movba(argument)
```

**Example 1**:
```python
up.run([MOVB, 15, MOVBA, 0])
# Expected: A = 15, B = 15
```

**Example 2** — Transfer loop result from B to A for further computation:
```python
up.run([
    MOVA, 0, MOVB, 0,
    ADDA, 1, ADDB, 6, CMPA, 4, JNZ, -6,   # B = 24
    MOVBA, 0,   # A = 24
    ADDA, 1,    # A = 25
])
# Expected: A = 25, B = 24
```

---

### 12. ADDAB — opcode 22

**Motivation**: Add register A to register B (B = B + A).  Enables
register-to-register arithmetic — required for doubling, accumulating, and
many other algorithms.

**RISC justification**: Most essential register-to-register arithmetic
operation; enables algorithms impossible with only immediate operands.

**Opcode constant**:
```python
ADDAB = 22
```

**Handler method**:
```python
def addab(self, argument):
    self.reg_b += self.reg_a
    self.zero = True if 0 == self.reg_b else False
    print(f'{self.pc:04d} ADDAB  \t=> B {self.reg_b} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == ADDAB:
    self.addab(argument)
```

**Example 1** — B = B + A:
```python
up.run([MOVA, 5, MOVB, 10, ADDAB, 0])
# Expected: A = 5, B = 15
```

**Example 2** — Double A using MOVAB + ADDAB:
```python
up.run([MOVA, 6, MOVAB, 0, ADDAB, 0])
# MOVAB: B = A = 6
# ADDAB: B = B + A = 6 + 6 = 12
# Expected: A = 6, B = 12  (A doubled into B)
```

See also: `examples/ext_register_ops.py`

---

### 13. ADDBA — opcode 23

**Motivation**: Add register B to register A (A = A + B).  Symmetric to ADDAB.

**Opcode constant**:
```python
ADDBA = 23
```

**Handler method**:
```python
def addba(self, argument):
    self.reg_a += self.reg_b
    self.zero = True if 0 == self.reg_a else False
    print(f'{self.pc:04d} ADDBA  \t=> A {self.reg_a} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == ADDBA:
    self.addba(argument)
```

**Example 1**:
```python
up.run([MOVA, 3, MOVB, 4, ADDBA, 0])
# Expected: A = 7, B = 4
```

**Example 2** — Fibonacci step: new A = A + B, then swap:
```python
up.run([MOVA, 1, MOVB, 1, ADDBA, 0, SWAB, 0])
# ADDBA: A = 1 + 1 = 2
# SWAB:  A = 1 (old B), B = 2 (new Fib)
# Expected: A = 1, B = 2
```

---

### 14. SUBAB — opcode 24

**Motivation**: Subtract A from B (B = B − A).  Enables comparison by
difference and range-checking patterns.

**Opcode constant**:
```python
SUBAB = 24
```

**Handler method**:
```python
def subab(self, argument):
    self.reg_b -= self.reg_a
    self.zero = True if 0 == self.reg_b else False
    print(f'{self.pc:04d} SUBAB  \t=> B {self.reg_b} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == SUBAB:
    self.subab(argument)
```

**Example 1** — B = B - A:
```python
up.run([MOVA, 3, MOVB, 10, SUBAB, 0])
# Expected: A = 3, B = 7
```

**Example 2** — SUBAB sets ZF when B − A = 0:
```python
up.run([MOVA, 5, MOVB, 5, SUBAB, 0])
# Expected: A = 5, B = 0, ZF = True
```

See also: `examples/ext_register_ops.py`

---

### 15. SUBBA — opcode 25

**Motivation**: Subtract B from A (A = A − B).  Symmetric to SUBAB.

**Opcode constant**:
```python
SUBBA = 25
```

**Handler method**:
```python
def subba(self, argument):
    self.reg_a -= self.reg_b
    self.zero = True if 0 == self.reg_a else False
    print(f'{self.pc:04d} SUBBA  \t=> A {self.reg_a} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == SUBBA:
    self.subba(argument)
```

**Example 1** — A = A - B:
```python
up.run([MOVA, 15, MOVB, 6, SUBBA, 0])
# Expected: A = 9, B = 6
```

**Example 2** — Compute absolute-difference hint (detect negative result):
```python
up.run([MOVA, 4, MOVB, 7, SUBBA, 0])
# A = 4 - 7 = -3  (Python integers handle negative values natively)
# Expected: A = -3, ZF = False
```

See also: `examples/ext_register_ops.py`

---

### 16. CMPAB — opcode 26

**Motivation**: Compare A with B and set ZF.  Avoids needing to load an
immediate value when both operands are already in registers.

**RISC justification**: Non-destructive register comparison is fundamental;
enables conditional branching based on register contents.

**Opcode constant**:
```python
CMPAB = 26
```

**Handler method**:
```python
def cmpab(self, argument):
    self.zero = True if self.reg_a == self.reg_b else False
    print(f'{self.pc:04d} CMPAB  \t=> ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == CMPAB:
    self.cmpab(argument)
```

**Example 1** — Equal registers set ZF:
```python
up.run([MOVA, 7, MOVB, 7, CMPAB, 0])
# Expected: ZF = True
```

**Example 2** — Unequal registers clear ZF:
```python
up.run([MOVA, 5, MOVB, 8, CMPAB, 0])
# Expected: ZF = False
```

See also: `examples/ext_register_ops.py`

---

### 17. NEGA — opcode 27

**Motivation**: Negate A (A = −A, i.e. two's complement negation).  Useful
for implementing subtraction via add-of-negative and for sign changes.

**RISC justification**: Negation is a single ALU operation; composable with
ADDBA/ADDAB to implement subtraction.

**Opcode constant**:
```python
NEGA = 27
```

**Handler method**:
```python
def nega(self, argument):
    self.reg_a = -self.reg_a
    self.zero = True if 0 == self.reg_a else False
    print(f'{self.pc:04d} NEGA   \t=> A {self.reg_a} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == NEGA:
    self.nega(argument)
```

**Example 1** — Negate a positive value:
```python
up.run([MOVA, 5, NEGA, 0])
# Expected: A = -5, ZF = False
```

**Example 2** — Double negation returns to original:
```python
up.run([MOVA, 8, NEGA, 0, NEGA, 0])
# Expected: A = 8, ZF = False
```

---

### 18. NEGB — opcode 28

**Motivation**: Symmetric counterpart to NEGA.

**Opcode constant**:
```python
NEGB = 28
```

**Handler method**:
```python
def negb(self, argument):
    self.reg_b = -self.reg_b
    self.zero = True if 0 == self.reg_b else False
    print(f'{self.pc:04d} NEGB   \t=> B {self.reg_b} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == NEGB:
    self.negb(argument)
```

**Example 1**:
```python
up.run([MOVB, 3, NEGB, 0])
# Expected: B = -3, ZF = False
```

**Example 2** — NEGB then ADDBA computes A − B using add-of-negative:
```python
up.run([MOVA, 10, MOVB, 3, NEGB, 0, ADDBA, 0])
# NEGB: B = -3
# ADDBA: A = A + B = 10 + (-3) = 7
# Expected: A = 7, B = -3
```

---

### 19. JMP — opcode 29

**Motivation**: An unconditional relative jump.  Currently, JNZ after
`ADDA 1` acts as an unconditional jump only because ZF happens to be False;
this is fragile.  JMP is explicit and safe.

**RISC justification**: Unconditional branch is a fundamental control-flow
primitive; makes programs clearer and eliminates dependency on ZF state.

**Opcode constant**:
```python
JMP = 29
```

**Handler method**:
```python
def jump(self, relative):
    print(f'{self.pc:04d} JMP  {relative} \t=> PC {self.pc+relative:04d}')
    self.pc += relative
```

**`elif` branch**:
```python
elif instruction == JMP:
    self.jump(argument)
```

**Example 1** — Unconditional infinite loop (use with care):
```python
up.run([
    MOVA, 0,    # pc 0000
    INCA, 0,    # pc 0002  <-- loop
    CMPA, 3,    # pc 0004
    JZ,   4,    # pc 0006: exit when A == 3
    JMP,  -6,   # pc 0008: unconditionally back to 0002
                # pc 0010: end (reached by JZ)
])
# Expected: A = 3
```

**Example 2** — Skip over a block:
```python
up.run([
    MOVA, 5,    # pc 0000
    JMP,  4,    # pc 0002: jump to 0006
    MOVA, 0,    # pc 0004: skipped!
    ADDA, 3,    # pc 0006: A = 5 + 3 = 8
])
# Expected: A = 8
```

---

### 20. ANDA — opcode 30

**Motivation**: Bitwise AND of A with an immediate value.  Used for masking
(isolating specific bits), testing flags, and clearing bits.

**RISC justification**: Bitwise operations are core ALU operations in every
RISC architecture; opens the door to bit manipulation.

**Opcode constant**:
```python
ANDA = 30
```

**Handler method**:
```python
def and_a(self, i):
    self.reg_a &= i
    self.zero = True if 0 == self.reg_a else False
    print(f'{self.pc:04d} ANDA {i} \t=> A {self.reg_a} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == ANDA:
    self.and_a(argument)
```

**Example 1** — Mask lower nibble:
```python
up.run([MOVA, 181, ANDA, 15])   # 181 = 0b10110101, 15 = 0b00001111
# Expected: A = 5 = 0b00000101
```

**Example 2** — Test even/odd (bit 0):
```python
up.run([MOVA, 7, ANDA, 1])   # 7 is odd: bit 0 = 1
# Expected: A = 1, ZF = False  (ZF=False means odd)
up.run([MOVA, 6, ANDA, 1])   # 6 is even: bit 0 = 0
# Expected: A = 0, ZF = True   (ZF=True means even)
```

See also: `examples/ext_bitwise.py`

---

### 21. ORA — opcode 31

**Motivation**: Bitwise OR of A with an immediate value.  Used for setting
specific bits.

**Opcode constant**:
```python
ORA = 31
```

**Handler method**:
```python
def or_a(self, i):
    self.reg_a |= i
    self.zero = True if 0 == self.reg_a else False
    print(f'{self.pc:04d} ORA  {i} \t=> A {self.reg_a} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == ORA:
    self.or_a(argument)
```

**Example 1** — Set bits 4 and 5:
```python
up.run([MOVA, 12, ORA, 48])   # 12 = 0b00001100, 48 = 0b00110000
# Expected: A = 60 = 0b00111100
```

**Example 2** — OR with 0 is a no-op (useful for testing ZF):
```python
up.run([MOVA, 0, ORA, 0])
# Expected: A = 0, ZF = True
```

See also: `examples/ext_bitwise.py`

---

### 22. XORA — opcode 32

**Motivation**: Bitwise XOR of A with an immediate value.  XOR with self = 0
(fast clear idiom); XOR with 0xFF toggles all bits.

**Opcode constant**:
```python
XORA = 32
```

**Handler method**:
```python
def xor_a(self, i):
    self.reg_a ^= i
    self.zero = True if 0 == self.reg_a else False
    print(f'{self.pc:04d} XORA {i} \t=> A {self.reg_a} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == XORA:
    self.xor_a(argument)
```

**Example 1** — XOR with same value clears A:
```python
up.run([MOVA, 42, XORA, 42])
# Expected: A = 0, ZF = True
```

**Example 2** — Toggle specific bits:
```python
up.run([MOVA, 0b00001111, XORA, 0b11111111])   # flip all 8 bits
# Expected: A = 0b11110000 = 240
```

See also: `examples/ext_bitwise.py`

---

### 23. SHLA — opcode 33

**Motivation**: Shift A left by N bits, equivalent to multiplying A by 2^N.
Much faster than repeated doubling loops.

**RISC justification**: Barrel-shifter operations are a RISC staple;
multiplication by powers of 2 is extremely common.

**Opcode constant**:
```python
SHLA = 33
```

**Handler method**:
```python
def shl_a(self, i):
    self.reg_a <<= i
    self.zero = True if 0 == self.reg_a else False
    print(f'{self.pc:04d} SHLA {i} \t=> A {self.reg_a} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == SHLA:
    self.shl_a(argument)
```

**Example 1** — Multiply by 2:
```python
up.run([MOVA, 3, SHLA, 1])
# Expected: A = 6
```

**Example 2** — Compute 2^5 = 32 in one instruction:
```python
up.run([MOVA, 1, SHLA, 5])
# Expected: A = 32
```

See also: `examples/ext_shift.py`

---

### 24. SHRA — opcode 34

**Motivation**: Shift A right by N bits, equivalent to integer-dividing A by
2^N.  Symmetric to SHLA.

**Opcode constant**:
```python
SHRA = 34
```

**Handler method**:
```python
def shr_a(self, i):
    self.reg_a >>= i
    self.zero = True if 0 == self.reg_a else False
    print(f'{self.pc:04d} SHRA {i} \t=> A {self.reg_a} ZF {self.zero}')
    self.pc += 2
```

**`elif` branch**:
```python
elif instruction == SHRA:
    self.shr_a(argument)
```

**Example 1** — Halve A:
```python
up.run([MOVA, 20, SHRA, 1])
# Expected: A = 10
```

**Example 2** — Integer divide by 8 (shift right 3):
```python
up.run([MOVA, 40, SHRA, 3])
# Expected: A = 5  (40 / 8 = 5)
```

See also: `examples/ext_shift.py`

---

## Summary of All New Opcodes

| Opcode | Mnemonic | Operation | Example file |
|--------|----------|-----------|-------------|
| 11 | NOP   | No operation | — |
| 12 | HALT  | Stop execution | `ext_halt.py` |
| 13 | INCA  | A = A + 1 | — |
| 14 | INCB  | B = B + 1 | — |
| 15 | DECA  | A = A − 1 | — |
| 16 | DECB  | B = B − 1 | — |
| 17 | CLRA  | A = 0 | — |
| 18 | CLRB  | B = 0 | — |
| 19 | SWAB  | A ↔ B | `ext_swap.py` |
| 20 | MOVAB | B = A | `ext_swap.py` |
| 21 | MOVBA | A = B | `ext_swap.py` |
| 22 | ADDAB | B = B + A | `ext_register_ops.py` |
| 23 | ADDBA | A = A + B | `ext_register_ops.py` |
| 24 | SUBAB | B = B − A | `ext_register_ops.py` |
| 25 | SUBBA | A = A − B | `ext_register_ops.py` |
| 26 | CMPAB | ZF = (A == B) | `ext_register_ops.py` |
| 27 | NEGA  | A = −A | — |
| 28 | NEGB  | B = −B | — |
| 29 | JMP   | pc += offset (unconditional) | — |
| 30 | ANDA  | A = A & imm | `ext_bitwise.py` |
| 31 | ORA   | A = A \| imm | `ext_bitwise.py` |
| 32 | XORA  | A = A ^ imm | `ext_bitwise.py` |
| 33 | SHLA  | A = A << imm | `ext_shift.py` |
| 34 | SHRA  | A = A >> imm | `ext_shift.py` |

---

## Cross-references

- For the base ISA and architecture overview, see **`tutorial.md`**.
- For example programs demonstrating the extended instructions, see the
  **`examples/`** folder (`ext_*.py` files).
- The original 10-instruction set is defined and implemented in
  **`MicroProcessor.py`**.
