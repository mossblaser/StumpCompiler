#!/usr/bin/python

from task import Task

class StoreValue(Task):
	"""
	Task to store a value from a given register.
	"""
	
	def __init__(self, value, reg_num):
		Task.__init__(self)
		
		self.value   = value
		self.reg_num = reg_num
	
	
	def set_initial_machine_state(self, machine_state):
		"""
		This step basically does nothing as this Task doesn't need other values
		loading/storing (as it is actually doing the loading/storing itself).
		"""
		self.machine_state = machine_state
	
	
	def get_final_machine_state(self):
		"""
		As no change to the machine state is made, return the initial state.
		"""
		return self.machine_state
	
	
	def compile(self):
		"""
		Return whatever instructions are neccessary to store the value into the
		specified register.
		"""
		raise NotImplemented()
	
	
	def __len__(self):
		"""
		Calculate the length of the instructions required to store the value.
		"""
		raise NotImplemented()



class StoreGlobalValue(StoreValue):
	"""
	A task to store a global variable from a register.
	"""
	
	def __init__(self, *args, **kwargs):
		StoreValue.__init__(self, *args, **kwargs)
	
	
	def __repr__(self):
		return "StoreGlobalValue(%s, %s)"%(self.value, self.reg_num)
	
	
	def compile(self):
		raise NotImplemented()
	
	
	def __len__(self):
		raise NotImplemented()



class StoreVolatileValue(StoreValue):
	"""
	A task to store a volatile variable from a register.
	"""
	
	def __init__(self, *args, **kwargs):
		StoreValue.__init__(self, *args, **kwargs)
	
	
	def __repr__(self):
		return "StoreVolatileValue(%s, %s)"%(self.value, self.reg_num)
	
	
	def compile(self):
		raise NotImplemented()
	
	
	def __len__(self):
		raise NotImplemented()

