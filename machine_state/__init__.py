#!/usr/bin/python

from task import Task

# General purpose registers. (e.g. not R0, SP or PC)
gp_reg_nums = range(1,6)

class MachineState(object):
	"""
	A store of state at a given stage in a function's execution, specifically what
	values are stored in what registers. The machine state provides an interface
	for tasks to convert a set of Values into registers. This object is immutable!
	"""
	
	def __init__(self, system, registers = None, flags_set = False,
	             read_values = None, written_values = None):
		"""
		Create a new MachineState. This is usually only done either by another
		MachineState or a function.
		
		Takes a System and optionally a list of values contained in registers and
		the status of the flags. These optional values are only intended to be
		passed in by this class.
		"""
		self.system = system
		
		# Elements indexed by the register numbers which contain a pair of values,
		# the first of which is the number of "machine states ago" the value was set
		# and the second of which is a Value object representing the value currently
		# stored in the register.
		self.registers = registers or (
			[0, system.get_constant(0)], # R0
			[0, None],                   # R1
			[0, None],                   # R2
			[0, None],                   # R3
			[0, None],                   # R4
			[0, None],                   # R5
			[0, system.get_sp()],        # SP
			[0, system.get_pc()]         # PC
		)
		
		# The set of all Values that have been read/written to at this machine
		# state.
		self.read_values    = read_values or set()
		self.written_values = written_values or set()
		
		# A dictionary mapping values to register numbers.
		self.value_to_register = {}
		for reg_num, (age, value) in enumerate(self.registers):
			self.value_to_register[value] = reg_num
		
		self.flags_set = flags_set
	
	
	def get_register(self, registers, required_values = None):
		"""
		Return the most suitable register to use to load a value. Accepts a register
		list and list of Value objects which mustn't be unloaded from a register in
		order to get a register to use. If there is an unused register, that is
		used, otherwise it uses the register that has been set the longest (and
		which doesn't contain a value on the passed blacklist) and unloads that so
		that the register is ready for the new value.
		
		Returns a register number to use and a list of tasks needed in order to
		make the register avalable to use.
		
		Note: It is expected that there is not already a register in the register
		bank containing the required Value. If there is, then this function's output
		may be impossible (e.g. assigning a none R0 register for a constant 0) or
		may be non-optimal (resulting in two registers holding the same Value).
		"""
		
		# Try to find a free register
		for reg_num, (age, value) in enumerate(self.registers):
			if value is None:
				return reg_num
		
		# Try to find the oldest register whose value can be swapped to memory
		# within the general purpose registers. (e.g. not R0, SP or PC)
		oldest_reg_num = None
		for reg_num in gp_reg_nums:
			reg_age, reg_value = registers[reg_num]
			
			# Test that this register is not blacklisted
			if reg_value not in required_values:
				# Remember this register if it is the oldest seen so-far
				if oldest_reg_num == None or registers[oldest_reg_num][0] < reg_age:
					oldest_reg_num = oldest_reg_num
		
		assert(oldest_reg_num is not None)
		
		oldest_reg_value = registers[oldest_reg_num]
		
		return (oldest_reg_num,
		        oldest_reg_value.get_store_from_register_task(oldest_reg_num))
	
	
	def values_to_reg_nums(self, read_values, write_values, flags_set = False):
		"""
		This function is designed to be used when turning a task into a single
		instruction.
		
		Takes two lists of Values, one which contains Values to be read from and
		the other Values to write to. Also takes whether the flags will be set
		during the instruction's execution.
		
		This process will return:
		  * A new MachineState which represents the state of the machine after the
		    requested registers have been read/written to.
		  * A list of registers corresponding to the read values.
		  * A list of registers corresponding to the write values.
		  * A task which must be executed before the instruction to populate the
		    registers requested with the values needed.
		  * A task which must be executed after the instruction to write-back the
		    values.
		
		Note that the two Tasks returned may be empty (as the value may already be
		in a register or may not require immediately writing back into memory).
		These Tasks also already have been passed a machine state so calling
		set_initial_machine_state on them has no effect.
		"""
		# Ensure there are enough registers for the number of values requested
		assert(len(read_values + write_values) < len(gp_reg_nums))
		
		read_reg_nums = []
		write_reg_nums = []
		
		pre_tasks = []
		post_tasks = []
		
		# Note if the flags have been set either previously or during this
		# instruction.
		flags_set = self.flags_set or flags_set
		
		# Make a copy of the register list where all the register ages have been
		# increased. This will form the new MachineState.
		registers = [register[:] for register in self.registers]
		
		# Find out what register each read-Value will be available in and what Tasks
		# need doing to load them.
		for value in read_values:
			if value in self.value_to_register:
				# Get the register already used to store this Value
				read_reg_nums.append(self.value_to_register[value])
			else:
				# Get a suitable register for the value, freeing up one if neccessary.
				reg_num, reg_freeing_task = self.get_register(read_values + write_values)
				pre_tasks.append(reg_freeing_task)
				read_reg_nums.append(reg_num)
				
				# Load the Value into the allocated register
				reg_loading_task = value.get_load_into_register_task(reg_num)
				pre_tasks.append(reg_loading_task)
			
			# Update the new MachineState
			registers[reg_num] = [0, value]
		
		# Find out what register each Value written will be available in and what
		# Tasks need doing to store them after or make space before them.
		for value in write_values:
			if value in self.value_to_register:
				# Note: it is assumed that if a Value is already in a register then it
				# must be non-valotile and so doesn't need writing back to memory
				# afterwards.
				
				# Get the register already used to store this Value, if possible
				write_reg_nums.append(self.value_to_register[value])
				
				# Update the new MachineState
				registers[reg_num] = [0, value]
			else:
				# Get a suitable register for the value, freeing up one if neccessary.
				reg_num, reg_freeing_task = self.get_register(read_values + write_values)
				pre_tasks.append(reg_freeing_task)
				write_reg_nums.append(reg_num)
				
				if value.volatile:
					# Volotile values must be written back to memory (and the value in the
					# register afterwards must be discarded).
					reg_writing_task = value.get_store_from_register_task(reg_num)
					post_tasks.append(reg_writing_task)
					registers[reg_num] = [0, None]
				else:
					# Update the new MachineState to indicate that the Value in the
					# register was updated (but don't write back to memory).
					registers[reg_num] = [0, value]
		
		# TODO: Make a task object which is specifically designed for these tasks
		# which do not need to have a MachineState passed through them before
		# compiling.
		pre_task  = Task(pre_tasks)
		post_task = Task(post_tasks)
		
		# Generate the new machine state, recording accesses to read and written
		# Values.
		new_machine_state = MachineState(self.system, tuple(registers), flags_set,
		                                 self.read_values.union(read_values),
		                                 self.written_values.union(written_values))
		
		return (new_machine_state,
		        read_reg_nums, write_reg_nums,
		        pre_task, post_task)
	
	
	def get_rejoin_state(self, other):
		"""
		Return the MachineState after this MachineState and another MachineState may
		have executed (e.g. at the end of an if-statement where this MachineState
		was the True condition and the other was the Else condition.). This
		MachineState will contain only Values which were present in both input
		MachineStates and will assume that both events may have occurred (e.g.
		merging the read_values and written_values sets and OR-ing the flags_set.
		"""
		# Make a copy of the register list of this MachineState which will be
		# modified to hold the intersection.
		registers = [register[:] for register in self.registers]
		
		# Check each register of this and the other machine state. Only keep Values
		# which are the same, otherwise assume that the register is free.
		for reg_num, register in enumerate(other.registers):
			if registers[reg_num][1] != register[1]:
				registers[reg_num] = [max(registers[reg_num][0], register[0]), None]
		
		# Merge the list of possibly read/written Values
		read_values = self.read_values.intersection(other.read_values)
		written_values = self.written_values.intersection(other.written_values)
		
		flags_set = self.flags_set or other.flags_set
		
		return MachineState(self.system, tuple(registers), flags_set,
		                    read_values, written_values)
	
	
	def get_task_to_reach_state(self, target):
		"""
		Return a task which will take this MachineState and result in the target
		machine state being reached. This may be useful after a block in an
		if-statement (for example) where the MachineState needs to be set to the
		union of all the possible exits from the block (e.g. the rejoin state).
		"""
		
		# Do an (incomplete) check to see if it is possible to reach the target
		# state
		assert(self.read_values.issubset(target.read_values))
		assert(self.write_values.issubset(target.write_values))
		assert(self.flags_set == target.flags_set)
		
		tasks = []
		
		for reg_num, (target_age, target_value) for enumerate(target.registers):
			age, value = self.register[reg_num]
			
			if target_value != value:
				# We can't deduce steps from one state to another where the target is
				# not an empty register. This shouldn't happen if the target state was
				# created by get_rejoin_state.
				assert(target_value == None)
				
				tasks.append(register.get_store_from_register_task(reg_num))
		
		
		# TODO: Make a task object which is specifically designed for these tasks
		# which do not need to have a MachineState passed through them before
		# compiling.
		return Task(tasks)
