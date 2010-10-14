#!/usr/bin/python

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
	
	
	def get_load_into_register_task(self, reg_num):
		return task.LoadConstantValue(self, reg_num)
	
	
	def get_store_from_register_task(self, reg_num):
		"""
		It is not possible to store a constant (as it should not be changed) so
		calling this method will raise a NotImplemented exception.
		"""
		raise NotImplemented("Cannot store constant Value!")
