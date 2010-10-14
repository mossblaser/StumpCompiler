#!/usr/bin/python

# Include other modules in this namespace
from load_value import LoadConstantValue

class Task(object):
	"""
	A task is a (possibly complex) "action" that can be performed but which when
	started will always finish at the end. This class is intended to be abstract.
	"""
	
	def __init__(self, subtasks = None):
		"""
		Create a task, optionally specifying a list of subtasks.
		"""
		self.subtasks = subtasks or []
	
	
	def set_initial_machine_state(self, machine_state):
		"""
		Set the initial machine state for this task. This should only be called
		once.
		"""
		
		# Propogate the MachineState through the task's subtasks
		for subtask in self.subtasks:
			subtask.set_initial_machine_state(machine_state)
			machine_state = subtask.get_final_machine_state()
	
	
	def get_final_machine_state(self):
		"""
		Get the machine state after this task has executed.  For this to complete
		successfully the initial machine state must have been passed into this
		task.
		"""
		return self.subtasks[-1].get_final_machine_state()
	
	
	def compile(self):
		"""
		Return a sequence of instructions which will accomplish this task.  For this
		to complete successfully the initial machine state must have been passed
		into this task.
		"""
		instrs = []
		for subtask in self.subtasks:
			instrs.extend(subtask.compile())
		return instrs
	
	
	def __len__(self):
		"""
		Returns the size (in words of program memory) needed to represent this task.
		For this to complete successfully the initial machine state must have been
		passed into this task.
		"""
		return sum(len(subtask) for subtask in self.subtasks)
