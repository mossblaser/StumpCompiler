#!/usr/bin/python

from task import LoadGlobalValue
from task import LoadVolatileValue
from task import StoreGlobalValue
from task import StoreVolatileValue
from value import Value

class Local(Value):
	"""
	A local variable Value, only available within a particular function.
	"""
	
	def __init__(self, name):
		Value.__init__(self, "LOCAL_%s"%(name))
		
		self.constant = False
		self.volatile = False
	
	
	def __repr__(self):
		return "Local(%d)"%self.name.partition("_")[2]
	
	
	def get_load_into_register_task(self, reg_num):
		return LoadConstantValue(self, reg_num)
	
	
	def get_store_from_register_task(self, reg_num):
		return StoreConstantValue(self, reg_num)



class Global(Value):
	"""
	A global variable Value.
	"""
	
	def __init__(self, name, initial_number = 0):
		Value.__init__(self, "GLOBAL_%s"%(name))
		
		self.constant = False
		self.volatile = False
		
		self.initial_number = initial_number
	
	
	def __repr__(self):
		return "Global(%s, %d)"%(repr(self.name.partition("_")[2]),
		                         self.initial_number)
	
	
	def get_load_into_register_task(self, reg_num):
		return LoadGlobalValue(self, reg_num)
	
	
	def get_store_from_register_task(self, reg_num):
		return StoreGlobalValue(self, reg_num)



class Volatile(Value):
	"""
	A volatile memory location.
	"""
	
	def __init__(self, name, location):
		Value.__init__(self, "VOLATILE_%s"%(name))
		
		self.constant = False
		self.volatile = True
		
		self.location = location
	
	
	def __repr__(self):
		return "Volatile(%s, %s)"%(repr(self.name.partition("_")[2]),
		                           self.location)
	
	
	def get_load_into_register_task(self, reg_num):
		return LoadVolatileValue(self, reg_num)
	
	
	def get_store_from_register_task(self, reg_num):
		return StoreVolatileValue(self, reg_num)

