""" 
    Disassembler for Yan85. Got from: https://github.com/flex0geek/Disassembler-Assembler-yan85/blob/main/disass_yan85.py
    Adapted a little bit to work with config profile.
"""

from .config import Config
    
class Yan85Disassembler:
    def __init__(self):
        self.config = Config()
        self.registers = vars(self.config.register)
        self.operations = vars(self.config.opcode)
        self.syscalls = vars(self.config.syscall_table)
        self.jmp_ops = vars(self.config.flags)
        
    # def chunkstring(self, string, length):
    #     return list(string[0+i:length+i] for i in range(0, len(string), length))

    def regs(self, val):
        for k, v in self.registers.items():
            if v == val:
                return k
            
    def imm(self, arg1, arg):
        op = 'imm'
        val = arg
        arg1 = self.regs(arg1)
        return op, arg1, hex(val)

    def add(self, arg1, arg2):
        op = 'add'
        arg1 = self.regs(arg1)
        arg2 = self.regs(arg2)
        return op, arg1, arg2

    def stk(self, arg1, arg2):
        op = 'stk'
        for k, v in self.registers.items():
            if arg2 != 0: # stk 0 A -> push a
                if arg2 == v:
                    arg2 = k
                    return op, arg1, arg2
            else: # stk A 0 -> pop a
                if arg1 == v:
                    arg1 = k
                    return op, arg1, arg2

    def stm(self, arg1, arg2):
        op = 'stm'
        arg1 = self.regs(arg1)
        arg2 = self.regs(arg2)
        return op, arg1, arg2

    def ldm(self, arg1, arg2):
        op = 'ldm'
        arg1 = self.regs(arg1)
        arg2 = self.regs(arg2)
        return op, arg1, arg2

    def jmp(self, arg1, arg2):
        for k, v in self.jmp_ops.items():
            if v == arg1:
                arg1 = k
        op = 'jmp'
        arg2 = self.regs(arg2)
        return op, arg1, arg2
            
    def syscall(self, arg1, arg2):
        for k, v in self.syscalls.items():
            if v == arg1:
                arg1 = hex(v)
        op = 'sys'
        arg2 = self.regs(arg2)
        return op, arg1, arg2

    def disass(self, opcode):
        if len(opcode) % 3 != 0:
            print("Opcode is not correct, maybe there is a wrong bytes")
            exit()
        else:
            op, arg1, arg2 = opcode
            for k, v in self.operations.items():
                if op == v:
                    if k == 'imm':
                        return self.imm(arg1, arg2)
                    elif k == 'add':
                        return self.add(arg1, arg2)
                    elif k == 'stk':
                        return self.stk(arg1, arg2)
                    elif k == 'stm':
                        return self.stm(arg1, arg2)
                    elif k == 'ldm':
                        return self.ldm(arg1, arg2)
                    elif k == 'jmp':
                        return self.jmp(arg1, arg2)
                    elif k == 'sys':
                        return self.syscall(arg1, arg2)

    # def process_instructions(self, opcode_bytes):
    #     instructions = self.chunkstring(opcode_bytes, 3)
    #     print("[+] Length of Instructions: "+str(len(instructions)))
    #     for instruction in instructions:
    #         op, arg1, arg2 = self.disass(instruction)

    #         if op == 'stk':
    #             if arg1 == 0:
    #                 print(op.upper(), arg1, arg2, '\t\t\t# push')
    #             elif arg2 == 0:
    #                 print(op.upper(), arg1, arg2, '\t\t\t# pop')
    #         elif op == "stm":
    #             print(op.upper(), "*"+arg1, arg2)
    #         elif op == "ldm":
    #             print(op.upper(), arg1, "*"+arg2)
    #         else:
    #             print(op.upper(), arg1, arg2)
