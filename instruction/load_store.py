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



class Load(LoadStore):
	
	def get_assembly_code(self):
		out = LoadStore.get_assembly_code(self)
		out += "ld r%d, [r%d, %s]\n"%(
			self.reg_num,
			self.addr_reg,
			"r%d"%self.offset_reg if offset_reg else "#%d"%self.offset_lit
		)
