#!/usr/bin/python

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
	
	
	def compile(self);
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
	
	
	def compile(self):
		"""
		Generate a load instruction to load the constant from the constant pool.
		"""
		# Ensure that the location being loaded has a memory address
		assert(self.value.location is not None)
		
		addr_reg, offset = self.value.location
		
		return [instruction.Load(self.reg_num, addr_reg, offset_lit = offset)]
	
	
	def __len__(self):
		# It takes one instruction to load a value from the constant pool
		return 1
