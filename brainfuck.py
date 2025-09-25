# 
# ██████   ██████    █████   ███████╗ ██    █  ██████╗ █╗    █╗  █████╗ █╗  █  
# █╔════█╗ █╔════█╗ █╔════█╗ ╚══█╦══╝ █╔█   █╗ █╔════╝ █║    █║ █╔════╝ █║ █╝  
# ██████╔╝ █║    █╝ █║    █║    █║    █║╚█  █║ █║      █║    █║ █║      █║█╝   
# █╔════█  ██████╝  ███████║    █║    █║ █╗ █║ █████╗  █║    █║ █║      ███╗   
# █║    █╗ █╠═══█╗  █╠════█╣    █║    █║  █╗█║ █╠═══╝  █║    █║ █║      █╠═█╗  
# ██████╔╝ █║    █╗ █║    █║ ███████╗ █║   ██║ █║       █████╔╝  █████╗ █║  █╗ 
#  ╚════╝  ╚╝    ╚╝ ╚╝    ╚╝ ╚══════╝ ╚╝   ╚═╝ ╚╝        ╚═══╝    ╚═══╝ ╚╝  ╚╝ 
# 
# Brainfuck interpreter for Python
# Copyright (c) 2025 beayon
# Licensed under the MIT License

import sys
import io
class BrainfuckVM:
    BINARY_CHARCODES = {
        "+": 0b000,
        "-": 0b001,
        ">": 0b010,
        "<": 0b011,
        ".": 0b100,
        ",": 0b101,
        "[": 0b110,
        "]": 0b111,
    }

    def __init__(self,*, maxmem: int = -1, initmem: int = 3000):
        self.mem = bytearray(initmem)
        self.pointer = 0
        self.maxmem = maxmem

    
    def exec(self, code, *, instant_flash:bool = True, stdin: io.TextIOBase = sys.stdin, stdout: io.TextIOBase = sys.stdout):
        self.exec_compiled(self.compile(code), instant_flash=instant_flash, stdin=stdin, stdout=stdout)
    
    def compile(self, code)-> bytes: return bytes(bytearray(i for i in (self.BINARY_CHARCODES.get(c) for c in code) if i != None))

    def exec_compiled(self, bincode: bytes, *, instant_flash:bool = True, stdin: io.TextIOBase = sys.stdin, stdout: io.TextIOBase = sys.stdout):
        code_pointer = 0
        loop_stacks = []
        while True:
            if code_pointer >= len(bincode): break
            opcode = bincode[code_pointer]
            if opcode == 0b000:
                self.mem[self.pointer] = (self.mem[self.pointer] + 1)%256
            elif opcode == 0b001:
                self.mem[self.pointer] = (self.mem[self.pointer] - 1)%256
            elif opcode == 0b010:
                self.pointer += 1
                if self.pointer == len(self.mem):
                    if self.maxmem > self.pointer or self.maxmem < 0:
                        self.mem.append(0)
                    else: self.pointer -= 1
            elif opcode == 0b011:
                self.pointer = max(self.pointer - 1, 0)
            elif opcode == 0b100:
                stdout.write(chr(self.mem[self.pointer]))
                if instant_flash: stdout.flush()
            elif opcode == 0b101:
                val = ord(stdin.read(1))
                self.mem[self.pointer] = val
            elif opcode == 0b110:
                if self.mem[self.pointer] == 0:
                    counter = 1
                    while counter > 0:
                        code_pointer += 1
                        tmp_opcode = bincode[code_pointer]
                        if tmp_opcode == 0b110: counter += 1
                        elif tmp_opcode == 0b111: counter -= 1
                        
                loop_stacks.append(code_pointer)
            elif opcode == 0b111:
                if self.mem[self.pointer] == 0:
                    loop_stacks.pop()
                else:
                    code_pointer = loop_stacks.pop() - 1
            code_pointer += 1
        stdout.flush()