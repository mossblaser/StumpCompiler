#!/usr/bin/python

class Value(object):
	"""
	A notional value used in the program. This class is intended to be abstract.
	"""
	
	def __init__(self, name = None):
		# The Value may have a name, this is mainly useful for debugging purposes.
		self.name = name
		
		# Is the Value a constant, i.e. is it known at compile time.
		self.constant = None
		
		# Is the Value volatile, i.e. Must it be read every time it is used and
		# written back every time it is changed.
		self.volatile = None
		
		# The memory location this Value is stored in memory or None if it is not
		# stored. Memory locations are in the form [addr_reg, offset_lit]
		self.location = None
	
	
	@property
	def local(self):
		"""
		Is this value to be stored in a function's stack?
		"""
		return not (self.constant or self.volatile)
	
	
	def get_load_into_register_task(self, reg_num):
		"""
		Get a Task which will load this Value into the specified register.
		"""
		raise NotImplemented()
	
	
	def get_store_from_register_task(self, reg_num):
		"""
		Get a Task which will store this Value from the specified register.
		"""
		raise NotImplemented()
