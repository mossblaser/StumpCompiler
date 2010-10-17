#!/usr/bin/python

from task  import LoadConstantValue
from value import Value

class Constant(Value):
	"""
	A constant Value, known at compile time to have be a particular number.
	"""
	
	def __init__(self, number):
		# Name this constant automatically based on it's number.
		Value.__init__(self, "CONST_0x%x"%(number))
		
		self.constant = True
		self.volatile = False
		self.number   = number
	
	
	def __repr__(self):
		return "Constant(%d)"%self.number
	
	
	def get_load_into_register_task(self, reg_num):
		return LoadConstantValue(self, reg_num)
	
	
	def get_store_from_register_task(self, reg_num):
		# Constants can't be changed so nothing is done to write the value back to
		# memory.
		return None
