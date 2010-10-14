StumpCompiler
=============

A naive compiler for the STUMP CPU. No language is yet defined or available, at
present I am working on the 'middle-end' of the compiler and so there's nothing
much to see here (especially as most of the design and specification are in a
notebook on my desk...)

Terminology (So Far)
====================

+-----------------------+-----------------------------------------------------+
| Value                 | A notional value, this may be a variable, a         |
|                       | constant etc. (not a specific number).              |
+-----------------------+-----------------------------------------------------+
| Task                  | A (possibly complex) series of operations which     |
|                       | starts at a given point and executes until a final  |
|                       | point (i.e. single entry, single exit).             |
+-----------------------+-----------------------------------------------------+
| MachineState          | The contents and age of the values in the STUMP's   |
|                       | general purpose registers at a given point of       |
|                       | execution of a function. Each Task in a function    |
|                       | has an initial MachineState and a final             |
|                       | MachineState.                                       |
+-----------------------+-----------------------------------------------------+
| Function              | A block of code with a single entry and multiple    |
|                       | exits and takes a number of arguments and produces  |
|                       | a return value. These arguments are stored on the   |
|                       | stack. Any registers (including condition codes)    |
|                       | that may be clobbered by execution of the function  |
|                       | are saved and restored on the function's start and  |
|                       | end.                                                |
+-----------------------+-----------------------------------------------------+
| Stack                 | A stack pointer is stored in R6 which is used to    |
|                       | support a full-decending software-stack.            |
+-----------------------+-----------------------------------------------------+
| ???                   | A task which wouldn't change the MachineState, for  |
|                       | example one produced by the MachineState to load or |
|                       | store a Value from memory to a register.            |
+-----------------------+-----------------------------------------------------+
