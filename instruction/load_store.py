#!/usr/bin/python

class LoadStore(Instruction):
	"""
	Load/Store a value from memory into a register. An abstract class.
	"""
	
	def __init__(self, reg_num, addr_reg, offset_reg = None, offset_lit = None, *args, **kwargs):
		Instruction.__init__(self, *args, **kwargs)
		
		self.reg_num    = reg_num
		self.addr_reg   = addr_reg
		self.offset_reg = offset_reg
		self.offset_lit = offset_lit
