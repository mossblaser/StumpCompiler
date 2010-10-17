#!/usr/bin/python

from machine_state import MachineState

class Function(object):
	"""
	A function which can be called in the program. A function will push all
	registers onto the stack which it changes 
	"""
	
	def __init__(self, system, name, argument_values = None, return_values = None,
	             tasks = None):
		self.system = system
		
		# The name of the function
		self.name = name
		
		# A list of Values representing arguments to the function
		self.argument_values = argument_values or []
		
		# A list of return Values for the function.
		self.return_values = return_values or []
		
		# A list of tasks performed by the function.
		self.tasks = tasks or []
		
		# List of registers that must be loaded/stored at the start and end
		# TODO
	
	
	def allocate_registers(self):
		"""
		Push a MachineState through the tasks inside the function. This will insert
		the relevent loading and storing Tasks into the Task and indirectly ensure
		that the required Values are loaded into registers as they're needed (in a
		hopefully sensible way).
		"""
		self.initial_machine_state = MachineState(self.system)
		
		# Propogate the machine state through the function.
		machine_state = self.initial_machine_state
		for task in self.tasks:
			task.set_initial_machine_state(machine_state)
			machine_state = task.get_final_machine_state()
		
		self.final_machine_state = machine_state
		
		# Make sure that all return values are set in the function
		assert(set(return_values).issubset(self.final_machine_state.written_values))
	
	
	def allocate_stack(self):
		"""
		Allocate stack space as required by this function.
		"""
		
		self.stack = []
		
		# Return values are placed on the bottom of the stack
		self.stack.extend(self.return_values)
		
		# Arguments for the function placed next.
		self.stack.extend(self.argument_values)
		
		# Record the number of stack elements which will have been pushed/reserved
		# on the stack by the call.
		self.initial_stack_offset = len(self.stack)
		
		# Make a list of all local variables used by the function but which aren't
		# part of the arguments/return.
		local_variables = (set(filter((lambda v: not v.local),
		                              self.final_machine_state.read_values
		                              + self.final_machine_state.write_values)
		                      ).difference(self.stack))
		
		# TODO: Don't allocate stack for local_variables that don't get written out
		# of the registers.
		self.stack.extend(local_variables)
		
		# Finally reserve stack space for saving registers
		# TODO
