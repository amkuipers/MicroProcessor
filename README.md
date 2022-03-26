# MicroProcessor
A simple MicroProcessor demo in Python.

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
