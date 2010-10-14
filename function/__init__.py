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
		self.argument_values = argument_values or {}
		
		# A list of return Values for the function.
		self.return_values = return_values or {}
		
		# A list of tasks performed by the function.
		self.tasks = tasks or []
	
	
	def allocate_registers(self):
		self.initial_machine_state = MachineState(self.system)
		
		# Propogate the machine state through the function.
		machine_state = self.initial_machine_state
		for task in self.tasks:
			task.set_initial_machine_state(machine_state)
			machine_state = task.get_final_machine_state()
		
		self.final_machine_state = machine_state
