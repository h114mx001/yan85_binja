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
    stack_pointer = "s"  # Stack pointer register
    
    def get_instruction_info(self, data, addr):
        
        result = InstructionInfo()
        result.length = 3  # Default length for Yan85 instructions
        return result 
    
    def get_instruction_text(self, data, addr):
        """ 
        parse the instruction insn. Assuming that it is well-formed
        """
        global YAN85_DISASS
        (op, arg1, arg2) = YAN85_DISASS.disass(data[addr:addr+3])
        
        result = []
        
        # the first token is the operation 
        result.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, op))
        
        # for the next two arguments, actually yan85 is not that tricky. 
        
        if op == "imm":
            # register 
            result.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, arg1))
            # int byte
            result.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, arg2))
        elif op == "add":
            # register 1
            result.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, arg1))
            # register 2
            result.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, arg2))
        elif op == "stk":
            if arg1 == 0:
                # stk 0 A -> push a
                result.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, "0"))
                result.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, arg2))
                result.append(InstructionTextToken(InstructionTextTokenType.CommentToken, "push " + arg2))
            else:
                # stk A 0 -> pop a
                result.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, arg1))
                result.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, "0"))
                result.append(InstructionTextToken(InstructionTextTokenType.CommentToken, "pop " + arg1))
        elif op == "stm":
            # stm [A] B 
            result.append(InstructionTextTokenType.BeginMemoryOperandToken, "[")
            result.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, arg1))
            result.append(InstructionTextTokenType.EndMemoryOperandToken, "]")
            
            result.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, arg2))        
      
        elif op == "ldm":
            result.append(InstructionTextTokenType.RegisterToken, arg1)
            result.append(InstructionTextTokenType.BeginMemoryOperandToken, "[")
            result.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, arg2))
            result.append(InstructionTextTokenType.EndMemoryOperandToken, "]")
            
        elif op == "cmp":
            # cmp A B
            result.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, arg1))
            result.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, arg2))
        elif op == "jmp":            
            if arg1 == 0:
                # jmp 0 A -> jmp a
                result.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, "0"))
                result.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, arg2))
            else: 
                
            