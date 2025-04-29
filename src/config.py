import tomli
from dataclasses import dataclass
from typing import List, Dict
import os 
from binaryninja import log

@dataclass
class Register:
    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0
    s: int = 0
    i: int = 0
    f: int = 0

@dataclass
class Opcode:
    imm: int = 0
    add: int = 0
    stk: int = 0
    stm: int = 0
    ldm: int = 0
    jmp: int = 0
    sys: int = 0

@dataclass
class SyscallTable:
    open: int = 0
    read_code: int = 0
    read_mem: int = 0
    write: int = 0
    sleep: int = 0
    exit: int = 0

@dataclass
class Flags:
    L: int = 0
    G: int = 0
    E: int = 0
    N: int = 0
    Z: int = 0

class Config:
    def __init__(self):
        self.register = Register()
        self.opcode = Opcode()
        self.syscall_table = SyscallTable()
        self.flags = Flags()
        self.op_order: List[int] = [0, 1, 2]
        
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.toml')
        if os.path.exists(config_path):
            self.load_config(config_path)
            log.log_info(f"Config for yan85 opcodes loaded from {config_path}")
        else:
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
    def load_config(self, config_path: str) -> None:
        """Load configuration from TOML file"""
        try:
            with open(config_path, 'rb') as f:
                config_data = tomli.load(f)
            
            # Load registers
            for key, value in config_data.get('registers', {}).items():
                setattr(self.register, key, value)
            
            # Load opcodes
            for key, value in config_data.get('opcode', {}).items():
                setattr(self.opcode, key, value)
            
            # Load syscalls
            for key, value in config_data.get('syscalls', {}).items():
                setattr(self.syscall_table, key, value)
            
            # Load flags
            for key, value in config_data.get('flags', {}).items():
                setattr(self.flags, key, value)
            
            # Load op_order if present
            if 'op_order' in config_data:
                self.op_order = config_data['op_order']
                
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {config_path}")
        except tomli.TOMLDecodeError:
            raise ValueError(f"Invalid TOML format in config file: {config_path}")