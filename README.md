# MicroProcessor
A simple MicroProcessor demo in Python.

The example calculates 5 times 5 into register B.

The example run log.

```
App: 3 0 4 0 1 1 2 5 7 5 10 -6
A 0 B 0 PC 0000 ZF True
0000 MOVA 0 	=> A 0 ZF True
0002 MOVB 0 	=> B 0 ZF True
0004 ADDA 1 	=> A 1 ZF False
0006 ADDB 5 	=> B 5 ZF False
0008 CMPA 5 	=> ZF False
0010 JNZ  -6 	=> ZF False PC 0004
0004 ADDA 1 	=> A 2 ZF False
0006 ADDB 5 	=> B 10 ZF False
0008 CMPA 5 	=> ZF False
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
0008 CMPA 5 	=> ZF True
0010 JNZ  -6 	=> ZF True PC 0004
App: 3 0 4 0 1 1 2 5 7 5 10 -6
A 5 B 25 PC 0012 ZF True
```

## Output explained

The 'binary' to give to this microprocessor simulator is: `3 0 4 0 1 1 2 5 7 5 10 -6`.

It shows at the start and end the values within the microprocessor: `A 0 B 0 PC 0000 ZF True`
- Register A = 0
- Register B = 0
- Program Counter = 0000
- Zero Flag = True

At the end of the run, value B contains the result of this program: `A 5 B 25 PC 0012 ZF True`.
- Register A = 5
- Register B = 25 (the final result of the program)
- Program Counter = 0012
- Zero Flag = True

In between the execution steps are shown, including loops and effect on the microcontroller.
- `0000 MOVA 0 	=> A 0 ZF True`: the binary starts with `3 0`, in this case it means `MOVA` move `0` into register A. And it shows `=> A 0 ZF True` as result.

A bit further in the execution a comparison of the value in register A with 5 can set or clear the ZF flag (in this microcontroller) `CMPA 5`. 
If register A contains `0` and compared with `5` the ZF is `False`, and if register would contain `5` and is compared with `5`, ZF is `True`. 
Based on the result in `ZF` the next instruction jumps back, or not.
In this case `0010 JNZ  -6 	=> ZF False PC 0004` because ZF is false, it jumps back to program counter `0004`. 

Looking at the last `JNZ -6` in the run log, when `ZF True` it does not jump back but ends the program.

## Simplified

This is a simplified microcontroller with one flag and two registers, and a very limited set of instructions. 
In this case it is looping 5 times, adding 5 in the each loop.
Often an instruction set contains a multiply `MUL` instruction.

