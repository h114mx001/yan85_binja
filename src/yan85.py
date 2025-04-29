from binaryninja.architecture import Architecture, RegisterInfo, InstructionInfo, InstructionTextToken, InstructionTextTokenType
from .disass_yan85 import Yan85Disassembler

YAN85_DISASS = Yan85Disassembler()
    
class Yan85(Architecture):
    name = "Yan85"
    address_size = 24           # 24-bit address size   
    default_int_size = 1        # 1-byte integer size
    instr_alignment = 1         # no instruction alignment
    max_instr_length = 3        # maximum instruction length
    regs = {
        # this version of Yan85 has 7 1-byte registers
        "a": RegisterInfo("a", 1),
        "b": RegisterInfo("b", 1),
        "c": RegisterInfo("c", 1),
        "d": RegisterInfo("d", 1),
        "s": RegisterInfo("s", 1),
        "i": RegisterInfo("i", 1),
        "f": RegisterInfo("f", 1),
    }
    stack_pointer = "S"  # Stack pointer register
    
    def get_instruction_info(self, data, addr):
        
        result = InstructionInfo()
        result.length = 3  # Default length for Yan85 instructions
        return result 
    
    def get_instruction_text(self, data, addr):
        global YAN85_DISASS
        (op, arg1, arg2) = YAN85_DISASS.disass(data[addr:addr+3])
        
        result = []
        
        # the first token is the operation 
        result.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, op))
        
        # from now, depend on the op, we have to add different arguments
        
          
        
      
    
    