#!/usr/bin/python

"""
A test program for the MachineState object. At each stage the new machine state
is printed after a number of actions are performed and a message indicating what
action has been carried out.
"""

from system        import System
from machine_state import MachineState

s = System()
m = MachineState(s)

def values_to_reg_nums(*args):
	print ">>> m.values_to_reg_nums(%s)"%(",".join(repr(a) for a in args))
	global m
	ms, rd, wrt, pre, post = m.values_to_reg_nums(*args)
	print "read regs: %s\nwrite regs: %s\npre: %s\npost: %s"%(rd, wrt, pre, post)
	return ms

print m

print "=" * 80
print "Reading constant 0"
m = values_to_reg_nums([s.get_constant(0)], [], False, False)
print m

print "=" * 80
print "Reading a constant twice."
m = values_to_reg_nums([s.get_constant(1), s.get_constant(1)], [], False, False)
print m

print "=" * 80
print "Reading two differrent constants."
m = values_to_reg_nums([s.get_constant(2), s.get_constant(3)], [], False, False)
print m


test_global = s.get_global("test_global")


print "=" * 80
print "Reading a Global."
m = values_to_reg_nums([test_global], [], False, False)
print m


print "=" * 80
print "Writing a Global."
m = values_to_reg_nums([], [test_global], False, False)
print m


test_volatile = s.get_volatile("test_volatile", 0xFF00)


print "=" * 80
print "Reading a Volatile. (Make sure that the register is clobbered)"
m = values_to_reg_nums([test_volatile], [], False, False)
print m


print "=" * 80
print "Writing a Volatile."
m = values_to_reg_nums([], [test_volatile], False, False)
print m


global1 = s.get_global("global1")
global2 = s.get_global("global2")
global3 = s.get_global("global3")
global4 = s.get_global("global4")
global5 = s.get_global("global5")


print "=" * 80
print "Populate all the registers"
m = values_to_reg_nums([global1], [], False, False)
print m


print "=" * 80
print "Take-over an old register"
m = values_to_reg_nums([global2], [], False, False)
print m


print "=" * 80
print "Take-over remaining constants"
m = values_to_reg_nums([global3, global4], [], False, False)
print m


print "=" * 80
print "Take-over register requiring swapping back to memory"
m = values_to_reg_nums([global5], [], False, False)
print m




print "=" * 80
print "Set flags"
m = values_to_reg_nums([], [], True, False)
print m

print "=" * 80
print "Read flags"
m = values_to_reg_nums([], [], False, True)
print m

print "=" * 80
print "Do nothing"
m = values_to_reg_nums([], [], False, False)
print m

print "=" * 80
print "Set flags again"
m = values_to_reg_nums([], [], True, False)
print m
