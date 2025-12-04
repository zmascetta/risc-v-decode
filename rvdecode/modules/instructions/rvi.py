# RV32I instruction set

from ..helper import decode as decode


class instruction:
    def __init__(self, instruction, opcode):
        self.instruction = instruction
        self.opcode = opcode
        self.instruction_set = "RV32I"


'''
I-Instruction:
This class handles the signed/unsiged NON-SHIFT i-instructions.

Instruction Components:
Opcode
Func3
RS1
RD
Immediate (12-digit, signed/unsigned)

Unsigned instructions: sltiu, sltu, bltu, bgeu, lbu, lhu
'''

class i_instruction(instruction):



    def create_general_info(self, instruction, opcode):
        general_info = {"Instruction Type": "I-Type",
                        "Instruction Set": "RV32I",
                        "Opcode": opcode,
                        "Func3": decode.get_func3(instruction)}

        rs1 = decode.get_rs1(instruction)


        return general_info

    def create_rs1(self, instruction):
        pass

    def create_rd(self, instruction):
        pass

    def get_general_data(self):
        pass

    def decode_instruction(self):
        pass


'''
I-Instruction (Shift):
This separate class handles the shift immediate instructions.

Shift Instruction Components:
Opcode
Func3
SHAMT (6-digit, but SHAMT[5] always equals 0)

Shift Instructions: slli, srli, srai
'''
class i_instruction_shift(instruction):

    def get_general_data(self):
        pass

    def decode_instruction(self):
        pass
