# MicroProcessor Simulator Tutorial

A complete guide from beginner to advanced for the MicroProcessor Python simulator.

---

## Table of Contents

1. [Introduction](#part-1-introduction)
2. [Instruction Set Reference](#part-2-instruction-set-reference)
3. [Reading Trace Output](#part-3-reading-trace-output)
4. [Writing Your First Program](#part-4-writing-your-first-program)
5. [Loops and Conditionals](#part-5-loops-and-conditionals)
6. [Multiplication via Repeated Addition](#part-6-multiplication-via-repeated-addition)
7. [Advanced Patterns](#part-7-advanced-patterns)
8. [Internals Deep Dive](#part-8-internals-deep-dive)
9. [Debugging Tips](#part-9-debugging-tips)

---

## Part 1: Introduction

### What is a microprocessor?

A microprocessor is the central processing unit of a computer.  It fetches
instructions from memory one by one, decodes what each instruction means, and
executes it — changing the state of registers, flags and memory in the process.
This repetitive cycle is called the **fetch-decode-execute cycle**.

### What is this simulator?

`MicroProcessor.py` is a minimal Python simulation of a microprocessor.  It
models the core concepts — registers, a zero flag, a program counter, and a
small but complete instruction set — without any hardware.  Running a program
means calling `run()` with a plain Python list of integers.

The class is called `MicroProcessor`.  The README calls it a "simplified
microcontroller" — both terms are used informally for small embedded processors.

### Architecture overview

```
┌─────────────┐    ┌─────────────┐
│  Register A │    │  Register B │
│    reg_a    │    │    reg_b    │
└─────────────┘    └─────────────┘
       │                  │
       └────────┬─────────┘
                │
         ┌──────┴──────┐
         │  Zero Flag  │
         │    zero     │
         └─────────────┘
                │
         ┌──────┴──────┐
         │   Program   │
         │   Counter   │
         │     pc      │
         └─────────────┘
```

| Component | Name in code | Initial value | Purpose |
|-----------|-------------|---------------|---------|
| Register A | `self.reg_a` | 0 | General-purpose integer register |
| Register B | `self.reg_b` | 0 | General-purpose integer register |
| Zero Flag  | `self.zero`  | **True** | Set when a result or comparison is zero/equal |
| Program Counter | `self.pc` | 0 | Points to the current instruction byte |

> **Note**: The zero flag starts as `True` when the simulator is first created,
> because registers A and B both start at 0.

### How programs are represented

Programs are flat Python lists of integers.  Instructions always occupy exactly
**two consecutive bytes**: an **opcode** followed by an **argument**.

```
index:   0      1      2      3      4      5
         MOVA   10     ADDA   5      ...    ...
         (op)  (arg)  (op)  (arg)
```

There is no separate "memory" for programs — the program array IS the memory.
The program counter `pc` is just an index into that array.

### How to run the simulator

```bash
python MicroProcessor.py
```

This runs the built-in 5 × 5 multiplication demo.

To write your own program, create a Python file that imports the module:

```python
import sys
sys.path.insert(0, '.')          # or adjust the path as needed
from MicroProcessor import MicroProcessor, MOVA, ADDA

up = MicroProcessor()
up.run([MOVA, 10, ADDA, 5])
```

---

## Part 2: Instruction Set Reference

All instructions use a fixed **2-byte format**: `[opcode, argument]`.
Instructions that do not use the argument (e.g. future extensions) still
consume it to keep the format uniform.

### Summary table

| Mnemonic | Opcode | Operation | Affects ZF? |
|----------|--------|-----------|-------------|
| ADDA | 1 | `A = A + arg` | Yes |
| ADDB | 2 | `B = B + arg` | Yes |
| MOVA | 3 | `A = arg` | Yes |
| MOVB | 4 | `B = arg` | Yes |
| SUBA | 5 | `A = A − arg` (trace quirk — see below) | Yes |
| SUBB | 6 | `B = B − arg` (trace quirk — see below) | Yes |
| CMPA | 7 | `ZF = (A == arg)`, registers unchanged | Yes |
| CMPB | 8 | `ZF = (B == arg)`, registers unchanged | Yes |
| JZ   | 9 | `if ZF: pc += arg` else `pc += 2` | No |
| JNZ  | 10 | `if not ZF: pc += arg` else `pc += 2` | No |

### Detailed descriptions

#### ADDA — Add immediate to A (opcode 1)
```
ADDA n     A = A + n     ZF = (A == 0) after add
```
Example: if `A = 3` and the instruction is `ADDA 4`, then `A` becomes `7`
and `ZF = False`.

#### ADDB — Add immediate to B (opcode 2)
```
ADDB n     B = B + n     ZF = (B == 0) after add
```

#### MOVA — Move immediate into A (opcode 3)
```
MOVA n     A = n     ZF = (n == 0)
```

#### MOVB — Move immediate into B (opcode 4)
```
MOVB n     B = n     ZF = (n == 0)
```

#### SUBA — Subtract immediate from A (opcode 5)

> ⚠️ **Trace output quirk**: SUBA is implemented by calling the same internal
> method as ADDA with a negated argument (`self.add_to_a(-argument)`).  The
> trace line will therefore show **`ADDA -n`** instead of `SUBA n`.
>
> Example: `SUBA 3` when `A = 10` produces the trace line:
> `0002 ADDA -3 \t=> A 7 ZF False`
>
> The arithmetic is correct (A goes from 10 to 7); only the label in the trace
> is misleading.

#### SUBB — Subtract immediate from B (opcode 6)

> ⚠️ **Same trace quirk as SUBA**: the trace prints **`ADDB -n`** instead of
> `SUBB n`.

#### CMPA — Compare immediate with A (opcode 7)
```
CMPA n     ZF = (A == n)     A is NOT modified
```
Sets `ZF = True` when A equals n, `False` otherwise.

#### CMPB — Compare immediate with B (opcode 8)
```
CMPB n     ZF = (B == n)     B is NOT modified
```

#### JZ — Jump if Zero Flag is True (opcode 9)
```
JZ offset     if ZF: pc += offset     else: pc += 2
```
The offset is **relative to the current PC** (the address of the JZ opcode
byte itself).  Use a negative offset to jump backwards.

> **Note**: The trace line always prints the would-be target PC regardless of
> whether the jump is taken.  For example:
> `0004 JZ   6 \t=> ZF False PC 0010`
> Here ZF is False so the jump is NOT taken, but the trace still shows
> `PC 0010` (the address that WOULD have been the destination).

#### JNZ — Jump if Zero Flag is False (opcode 10)
```
JNZ offset     if not ZF: pc += offset     else: pc += 2
```
Same relative addressing and same trace behaviour as JZ.

### Opcode 0 — Infinite loop risk

> ⚠️ **Bug**: When the simulator encounters `instruction == 0`, the code
> executes `pass` and does NOT advance `pc`.  The program counter stays at the
> same address forever, creating an **infinite loop**.  Never place opcode 0 in
> your program.

### Unknown opcodes — Silent NOP

Any opcode that is not recognised (and is not 0) falls through to the `else`
branch in `run()`, which does `pass` then `self.pc += 2`.  The unknown
instruction is silently skipped with no trace output.

---

## Part 3: Reading Trace Output

### The info() header and footer

Every call to `run()` prints a header and footer via `info()`:

```
App: 3 0 4 0 1 1 2 5 7 5 10 -6
A 0 B 0 PC 0000 ZF True
```

- **App:** — the raw program bytes (opcodes and arguments interleaved)
- **A / B** — register values
- **PC** — program counter (4-digit zero-padded decimal)
- **ZF** — zero flag value

### Instruction trace format

Each executed instruction prints one line:

```
PPPP INST ARG \t=> EFFECTS
```

| Field | Meaning |
|-------|---------|
| `PPPP` | Program counter address (4-digit, zero-padded) when instruction started |
| `INST` | Instruction mnemonic (padded to 5 chars) |
| `ARG`  | The argument value |
| `EFFECTS` | Register and/or flag values after execution |

Examples:
```
0000 MOVA 0 	=> A 0 ZF True
0004 ADDA 1 	=> A 1 ZF False
0008 CMPA 5 	=> ZF False
0010 JNZ  -6 	=> ZF False PC 0004
```

### Step-by-step walkthrough: 5 × 5 = 25

Program bytes: `MOVA 0, MOVB 0, ADDA 1, ADDB 5, CMPA 5, JNZ -6`

```
App: 3 0 4 0 1 1 2 5 7 5 10 -6
A 0 B 0 PC 0000 ZF True
0000 MOVA 0 	=> A 0 ZF True     # A = 0 (counter initialised)
0002 MOVB 0 	=> B 0 ZF True     # B = 0 (accumulator initialised)
0004 ADDA 1 	=> A 1 ZF False    # counter: A = 1
0006 ADDB 5 	=> B 5 ZF False    # accumulator: B = 5
0008 CMPA 5 	=> ZF False        # 1 != 5, keep looping
0010 JNZ  -6 	=> ZF False PC 0004   # ZF=False so jump back to 0004
0004 ADDA 1 	=> A 2 ZF False    # A = 2
0006 ADDB 5 	=> B 10 ZF False   # B = 10
0008 CMPA 5 	=> ZF False        # 2 != 5
0010 JNZ  -6 	=> ZF False PC 0004
0004 ADDA 1 	=> A 3 ZF False
0006 ADDB 5 	=> B 15 ZF False
0008 CMPA 5 	=> ZF False
0010 JNZ  -6 	=> ZF False PC 0004
0004 ADDA 1 	=> A 4 ZF False
0006 ADDB 5 	=> B 20 ZF False
0008 CMPA 5 	=> ZF False
0010 JNZ  -6 	=> ZF False PC 0004
0004 ADDA 1 	=> A 5 ZF False
0006 ADDB 5 	=> B 25 ZF False
0008 CMPA 5 	=> ZF True         # 5 == 5, ZF set
0010 JNZ  -6 	=> ZF True PC 0004 # ZF=True so NOT jumping; note: target still printed!
App: 3 0 4 0 1 1 2 5 7 5 10 -6
A 5 B 25 PC 0012 ZF True           # result: B = 25 = 5 × 5
```

Note on the last `JNZ` line: the trace prints `PC 0004` (the would-be target)
even though the jump is NOT taken and the PC advances to 0012.  This is the
JZ/JNZ print-before-check behaviour described in [Part 2](#jnz--jump-if-zero-flag-is-false-opcode-10).

---

## Part 4: Writing Your First Program

### A simple load-and-add program

This program loads the value 10 into register A, then adds 5.

**Source: `examples/tutorial_add.py`**

```python
from MicroProcessor import MicroProcessor, MOVA, ADDA

up = MicroProcessor()
up.run([
    MOVA, 10,   # A = 10
    ADDA, 5,    # A = A + 5 = 15
])
```

Expected output:
```
App: 3 10 1 5
A 0 B 0 PC 0000 ZF True
0000 MOVA 10 	=> A 10 ZF False
0002 ADDA 5 	=> A 15 ZF False
App: 3 10 1 5
A 15 B 0 PC 0004 ZF False
```

### Key observations

1. The header shows `ZF True` because the simulator starts with A=0 (zero).
2. After `MOVA 10`, ZF becomes `False` because 10 ≠ 0.
3. After `ADDA 5`, A = 15 and ZF remains `False`.
4. The PC ends at 0004, which is past the last byte (index 3), so the loop
   exits cleanly.

Run it:
```bash
python examples/tutorial_add.py
```

---

## Part 5: Loops and Conditionals

### How JZ and JNZ work

Jump instructions use **relative offsets**.  The offset is added to the address
of the jump instruction itself.

```
address of JZ instruction + offset = destination address
```

To jump to a previous instruction, use a **negative** offset.
To jump forward (skip instructions), use a **positive** offset.

### Calculating the right offset

Given a program laid out in memory:

```
0000: MOVA  0     (2 bytes)
0002: CMPA  3     (2 bytes)
0004: JZ    6     — offset 6: destination = 0004 + 6 = 0010
0006: ADDA  1     (2 bytes)
0008: JNZ  -6     — offset -6: destination = 0008 + (-6) = 0002
0010: (program ends here)
```

### Counting from 0 to 3

**Source: `examples/tutorial_loop.py`**

```python
from MicroProcessor import MicroProcessor, MOVA, ADDA, CMPA, JZ, JNZ

up = MicroProcessor()
up.run([
    MOVA, 0,    # pc 0000: A = 0  (counter)
    CMPA, 3,    # pc 0002: ZF = (A == 3)?
    JZ,   6,    # pc 0004: if ZF, jump to pc 0010 (end)
    ADDA, 1,    # pc 0006: A++
    JNZ, -6,    # pc 0008: loop back to pc 0002
])
```

Expected output:
```
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
```

### How the loop works

| Iteration | A before CMPA | ZF after CMPA | JZ taken? | JNZ taken? |
|-----------|--------------|---------------|-----------|------------|
| 1 | 0 | False (0≠3) | No | Yes (back to 0002) |
| 2 | 1 | False (1≠3) | No | Yes |
| 3 | 2 | False (2≠3) | No | Yes |
| 4 | 3 | True  (3==3) | Yes (exit) | — |

The `JNZ -6` acts as an unconditional "go back to CMPA" because after
`ADDA 1` the result is always 1, 2, or 3 — never 0 — so ZF is always False
and JNZ always jumps.

---

## Part 6: Multiplication via Repeated Addition

### The algorithm

Multiplication is repeated addition: `A × B = B + B + … + B` (A times).

The simulator uses this pattern:
- Register A counts from 0 up to the **multiplier**
- Register B accumulates by adding the **multiplicand** each iteration
- CMPA checks whether A has reached the multiplier
- JNZ loops back if not yet done

### The built-in 5 × 5 = 25 example

```
loop body (pc 0004–0010):
  ADDA 1    — increment counter
  ADDB 5    — add multiplicand (5) to result
  CMPA 5    — check: have we done this 5 times?
  JNZ -6    — if not, repeat
```

After 5 iterations: A = 5, B = 25.

### Generalising: 4 × 6 = 24

**Source: `examples/tutorial_multiply.py`**

```python
from MicroProcessor import MicroProcessor, MOVA, MOVB, ADDA, ADDB, CMPA, JNZ

up = MicroProcessor()
up.run([
    MOVA, 0,    # counter = 0
    MOVB, 0,    # accumulator = 0
    ADDA, 1,    # counter++
    ADDB, 6,    # accumulator += 6   (multiplicand)
    CMPA, 4,    # done when counter == 4   (multiplier)
    JNZ, -6,    # loop back if not done
])
# Result: A = 4, B = 24
```

To compute any product `M × N`, set:
- `ADDB` argument = N (multiplicand — what to add each time)
- `CMPA` argument = M (multiplier — how many times to add)

---

## Part 7: Advanced Patterns

### Computing subtraction results

Use SUBA (opcode 5) to subtract from A.  Remember the trace quirk: the output
will show `ADDA -n` instead of `SUBA n`.

```python
up.run([MOVA, 10, SUBA, 3])
# Trace: 0002 ADDA -3 \t=> A 7 ZF False
# Result: A = 7
```

### Countdown loops

Count A down from N to 0 using SUBA and JNZ:

```python
from MicroProcessor import MicroProcessor, MOVA, SUBA, CMPA, JNZ

up = MicroProcessor()
up.run([
    MOVA, 5,    # pc 0000: A = 5
    SUBA, 1,    # pc 0002: A--  (trace shows: ADDA -1)
    CMPA, 0,    # pc 0004: ZF = (A == 0)?
    JNZ, -4,    # pc 0006: loop back to pc 0002 while A != 0
])
# Result: A = 0, ZF = True
```

### Nested logic patterns

To implement an "if-then" pattern: use CMPA/CMPB to set ZF, then JZ to skip
the "then" block:

```python
# if A != 7: add 100 to B
from MicroProcessor import MicroProcessor, MOVA, MOVB, CMPA, JZ, ADDB

up = MicroProcessor()
up.run([
    MOVA, 5,    # pc 0000: A = 5
    MOVB, 0,    # pc 0002: B = 0
    CMPA, 7,    # pc 0004: ZF = (A == 7)?
    JZ,   4,    # pc 0006: if A==7, skip the ADDB
    ADDB, 100,  # pc 0008: B += 100   (only reached when A != 7)
                # pc 0010: end
])
# A = 5 != 7, so ADDB runs: B = 100
```

### Computing powers: 2^4 = 16

The current ISA has no register-to-register add (that would require the ADDAB
extension), so we use the identity **2^4 = 4^2 = 4 × 4** and apply the
multiplication loop.

**Source: `examples/tutorial_power.py`**

```python
from MicroProcessor import MicroProcessor, MOVA, MOVB, ADDA, ADDB, CMPA, JNZ

up = MicroProcessor()
up.run([
    MOVA, 0,    # counter
    MOVB, 0,    # accumulator
    ADDA, 1,    # counter++
    ADDB, 4,    # accumulate (add 4 each time)
    CMPA, 4,    # loop 4 times
    JNZ, -6,
])
# Result: B = 16 = 4 × 4 = 2^4
```

> **Limitation**: Without register-to-register operations (see `extensions.md`),
> true iterative doubling is not directly expressible in the base ISA.  See the
> SHLA instruction in the extensions guide for a cleaner approach.

### Computing triangular numbers: T(5) = 15

The Nth triangular number T(N) = 1 + 2 + ... + N = N × (N+1) / 2.

For N = 5: T(5) = 5 × 6 / 2 = 5 × 3 = 15.  We compute 5 × 3 using the
multiplication pattern.

**Source: `examples/tutorial_triangular.py`**

```python
from MicroProcessor import MicroProcessor, MOVA, MOVB, ADDA, ADDB, CMPA, JNZ

up = MicroProcessor()
up.run([
    MOVA, 0,    # counter
    MOVB, 0,    # accumulator
    ADDA, 1,    # counter++
    ADDB, 3,    # add (N+1)/2 = 3 each time
    CMPA, 5,    # loop N = 5 times
    JNZ, -6,
])
# Result: B = 15 = T(5)
```

---

## Part 8: Internals Deep Dive

### The fetch-decode-execute cycle in `run()`

```python
while 0 <= self.pc < len(self.app):
    instruction = self.app[self.pc]       # FETCH opcode
    argument    = self.app[self.pc + 1]   # FETCH argument

    if instruction == ADDA:               # DECODE
        self.add_to_a(argument)           # EXECUTE (also advances pc by 2)
    elif ...
```

Each handler method both executes the operation **and** advances `pc` by 2.
The loop continues until `pc` falls outside the array bounds.

### The flat array memory model

There is no separate instruction memory and data memory.  The program is a
plain Python list.  The PC is simply an index.  This is a
**Harvard-like** simplification — in a real processor there is typically
separate address space for code and data.

### Why pc increments by 2

Every instruction is exactly 2 bytes (opcode + argument), so every successful
instruction handler ends with `self.pc += 2`.  Jump instructions compute the
new PC differently but still consume 2 bytes when the jump is not taken.

### Calling `run()` multiple times

`run()` resets `pc` to 0 but **does not reset registers or the zero flag**.
This means consecutive calls accumulate state:

```python
up = MicroProcessor()
up.run([MOVA, 5])          # A = 5, ZF = False
up.run([ADDA, 3])          # A still 5 from previous run; becomes 8
```

This can be useful for chaining computations but is also a source of bugs.

### Known quirks and edge cases

#### 1. Opcode 0 — infinite loop

```python
while 0 <= self.pc < len(self.app):
    instruction = self.app[self.pc]
    ...
    if instruction == 0:
        pass               # <-- pc is NEVER advanced
```

If opcode 0 appears in the program, the processor hangs forever.  Always avoid
opcode 0 in programs.

#### 2. SUBA / SUBB trace output

`SUBA` calls `self.add_to_a(-argument)`.  The `add_to_a` method prints `ADDA`
in its trace.  The arithmetic is correct but the displayed mnemonic is wrong.

#### 3. JZ / JNZ print before checking

Both jump methods print the trace line (including the computed target address)
**before** evaluating the condition.  The target address shown is always the
address that *would* be jumped to, even when the jump is not taken.

#### 4. Initial ZF is True

`self.zero = True` in `__init__`.  The very first conditional jump in a program
will see ZF = True unless a prior instruction has changed it.

---

## Part 9: Debugging Tips

### Using `info()` to inspect state

`info()` is called automatically at the start and end of `run()`, but you can
call it manually at any point to inspect the current state:

```python
up = MicroProcessor()
up.app = [MOVA, 5, ADDA, 3]
up.pc = 0
up.info()   # prints current A, B, PC, ZF
```

### Common mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Wrong jump offset | Program jumps to wrong address or walks off end | Count bytes carefully; PC of jump + offset = target |
| Opcode 0 in program | Program hangs forever | Never use 0 as an opcode |
| Forgetting `run()` resets only PC | Second `run()` starts with leftover register values | Call `MicroProcessor()` again for a fresh start |
| SUBA trace says ADDA | Confusing trace output | This is a known quirk; the arithmetic is still correct |
| Off-by-one in loop terminator | Loop runs one too many or few times | Test the exit condition carefully with CMPA/CMPB |

### How to trace through programs manually

1. Write out all instructions with their byte addresses (0, 2, 4, …).
2. Draw a table with columns: PC, Instruction, Argument, A, B, ZF.
3. Step through each instruction, updating the table row by row.
4. For jumps, compute `new_pc = current_pc + offset`; check ZF to decide.

Example trace table for `MOVA 0, ADDA 1, CMPA 3, JNZ -4`:

| Step | PC | Instruction | Arg | A | B | ZF |
|------|----|-------------|-----|---|---|----|
| 0 | 0000 | MOVA | 0 | 0 | 0 | True |
| 1 | 0002 | ADDA | 1 | 1 | 0 | False |
| 2 | 0004 | CMPA | 3 | 1 | 0 | False |
| 3 | 0006 | JNZ  | -4 | 1 | 0 | False → jump to 0002 |
| 4 | 0002 | ADDA | 1 | 2 | 0 | False |
| … | … | … | … | … | … | … |

### Cross-references

- To add new instructions to the simulator, see **`extensions.md`**.
- All example programs in this tutorial are in the **`examples/`** folder.
- The built-in demo is at the bottom of **`MicroProcessor.py`** inside the
  `if __name__ == '__main__':` block.
