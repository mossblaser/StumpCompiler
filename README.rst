StumpCompiler
=============

IMPORTANT NOTE: I have no idea how compilers in the real world work: I've never
researched them or tried to learn about standard practices. This project is an
experiment to see how many real-world compiler design techniques I reinvent
myself without seeing how real compilers work. In short, please don't tell me if
I'm doing something stupid or less than efficient unless it will result in the
generated code being incorrect.

A naive compiler for the STUMP CPU. No language is yet defined or available, at
present I am working on the 'middle-end' of the compiler and so there's nothing
much to see here (especially as most of the design and specification are in a
notebook on my desk...). Also, I don't intend to make a serious effort to make
this compiler produce optimal code. I may experiment with some primative
optimisations however.

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


Possible Compile Process
========================

'Front-end'

1.  Tokenize Source File
2.  Turn tokenized source into internal representation which is a more abstract
    form of the language. This may include language constructs such as
    non-1-word-integer types etc.
3.  [Possible optimisation opportunity.]
4.  Simplify into a more primative representation which contains very basic
    constructs, all values simplified to one-word data types, no more
    complicated flow control than a function.
5.  [Possible optimisation opportunity.]

'Middle-end'

6.  Allocate registers throughout execution of all functions, inserting the
    required load/store steps [optimisation step].
7.  Decide if (and what) local variables should be kept on the stack during each
    function's execution based on step 4.
8.  Decide what constants and global variables need to defined.
9.  [Possible optimisation opportunity.]

'Back-end'

10. Allocate memory and layout for constants, globals, functions.
11. Generate a function table. [At this point all Values and function calls
    should have a real address in memory (or relative to the stack).]
12. Flatten Tasks into real instructions.
13. Generate startup code (i.e. register setup and jump into main).
14. [Possible optimisation opportunity.]
15. Assemble.
16. ???
17. Profit!
