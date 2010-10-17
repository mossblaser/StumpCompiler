#!/usr/bin/python

from value import Value

class SystemRegister(Value):
	"""
	A system register (base class, abstract)
	"""
	
	def __init__(self, *args, **kwargs):
		Value.__init__(self, *args, **kwargs)
		
		self.constant = False
		self.volatile = False
		self.number   = None
	
	@property
	def local(self):
		return False
	
	
	def get_load_into_register_task(self, reg_num):
		raise NotImplemented("System Register is always loaded!")
	def get_store_from_register_task(self, reg_num):
		raise NotImplemented("The System Register never needs to be swapped out.")


class StackPointer(SystemRegister):
	
	def __init__(self):
		SystemRegister.__init__(self, "STACKPOINTER")
	def __repr__(self):
		return "StackPointer()"


class ProgramCounter(SystemRegister):
	
	def __init__(self):
		SystemRegister.__init__(self, "PROGRAMCOUNTER")
	def __repr__(self):
		return "ProgramCounter()"

