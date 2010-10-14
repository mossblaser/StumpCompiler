#!/usr/bin/python

class LoadValue(Task):
	"""
	Task to load a value into a given register.
	"""
	
	def __init__(self, value, reg_num):
		self.value   = value
		self.reg_num = reg_num
		
		# Todo: e.g. check literal 0 isn't loaded into a non R0 register
		
		Task.__init__(self)
	
	
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
		pass
	
	
	def __len__(self):
		"""
		Calculate the length of the instructions required to load the value.
		"""
		raise NotImplemented()
