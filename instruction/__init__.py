#!/usr/bin/python

from load_store import LoadInstruction, StoreInstruction

class Instruction(object):
	"""
	An instruction that can be assembled into native code.
	"""
	
	def __init__(self, label = None, location = None):
		"""
		Create an instruction with the given label and at the specified memory
		location.
		"""
		
		self.label = label
		self.location = location
	
	
	def get_assembly_code(self):
		out = ""
		
		# Set the location of the generated instruction if needed
		if self.location != None:
			out += "org %d\n"
		
		# Add a label to this location.
		if self.label != None:
			out += "%s:\t"
		
		return out
