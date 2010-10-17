#!/usr/bin/python

from task import Task

class LoadValue(Task):
	"""
	Task to load a value into a given register.
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
		Return whatever instructions are neccessary to load the value into the
		specified register.
		"""
		raise NotImplemented()
	
	
	def __len__(self):
		"""
		Calculate the length of the instructions required to load the value.
		"""
		raise NotImplemented()



class LoadConstantValue(LoadValue):
	"""
	A task to load a constant into a register.
	"""
	
	def __init__(self, *args, **kwargs):
		LoadValue.__init__(self, *args, **kwargs)
		
		# There's no point in a task to load the constant 0 as it will always be
		# present in R0.
		assert(self.value.number != 0)
	
	
	def __repr__(self):
		return "LoadConstantValue(%s, %s)"%(self.value, self.reg_num)
	
	
	def compile(self):
		raise NotImplemented()
	
	
	def __len__(self):
		raise NotImplemented()



class LoadGlobalValue(LoadValue):
	"""
	A task to load a global variable into a register.
	"""
	
	def __init__(self, *args, **kwargs):
		LoadValue.__init__(self, *args, **kwargs)
	
	
	def __repr__(self):
		return "LoadGlobalValue(%s, %s)"%(self.value, self.reg_num)
	
	
	def compile(self):
		raise NotImplemented()
	
	
	def __len__(self):
		raise NotImplemented()



class LoadVolatileValue(LoadValue):
	"""
	A task to load a volatile variable into a register.
	"""
	
	def __init__(self, *args, **kwargs):
		LoadValue.__init__(self, *args, **kwargs)
	
	
	def __repr__(self):
		return "LoadVolatileValue(%s, %s)"%(self.value, self.reg_num)
	
	
	def compile(self):
		raise NotImplemented()
	
	
	def __len__(self):
		raise NotImplemented()
