#!/usr/bin/python

from value import Constant
from value import Global
from value import Volatile
from value import StackPointer
from value import ProgramCounter

class System(object):
	
	def __init__(self):
		# Keep track of constants used by the program
		self.constants = {}
		
		# All global Values used by the program
		self.global_values = []
		
		# A list of all volatile Values
		self.volatile_values = []
		
		# Create the system register Values
		self.stack_pointer   = StackPointer()
		self.program_counter = ProgramCounter()
	
	
	def __repr__(self):
		return "System()"
	
	
	def get_constant(self, number):
		"""
		Get a constant Value with the given number.
		"""
		if number not in self.constants:
			self.constants[number] = Constant(number)
		
		return self.constants[number]
	
	
	def get_global(self, name = None, initial_value = 0):
		"""
		Define a global variable.
		"""
		value = Global(name, initial_value)
		self.global_values.append(initial_value)
		return value
	
	
	def get_volatile(self, name = None, location = 0):
		"""
		Define a volatile variable.
		"""
		value = Volatile(name, location)
		self.volatile_values.append(value)
		return value
	
	
	def get_sp(self):
		"""
		Get the Stack Pointer Value.
		"""
		return self.stack_pointer
	
	
	def get_pc(self):
		"""
		Get the Program Counter Value.
		"""
		return self.program_counter
