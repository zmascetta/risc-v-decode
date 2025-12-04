# RV32I instruction set

from ..helper import decode as decode, errorcheck as errorcheck


class Instruction:
    def __init__(self, instruction, opcode):
        self.instruction = instruction
        self.opcode = opcode
        self.instruction_set = "RV32I"


'''
I-Instruction:
Handles the signed/unsigned NON-SHIFT i-instructions.
Instruction Components: Opcode, Func3, RS1, RD, Immediate (12-digit, signed/unsigned)
Unsigned instructions: sltiu, sltu, lbu, lhu
'''
class IInstruction:

    def decode_instruction(self, instruction, opcode):

        func3 = decode.get_func3(instruction)

        # Create header dict.
        header_info = {"instruction": instruction,
                        "spacing_list": (12, 5, 3, 5, 7),
                        "label": "imm--------| rs1-| f3| rd--| opcode|\n"}

        instruction_lookup_value = opcode + func3
        i_instruction_lookup = {
                    "1100111000": {"short_name":  "jalr", "full_name": "jump and link register"},
                    "0000011000": {"short_name":  "lb", "full_name": "load byte"},
                    "0000011001": {"short_name":  "lh", "full_name": "load halfword"},
                    "0000011010": {"short_name":  "lw", "full_name": "load word"},
                    "0000011100": {"short_name":  "lbu", "full_name": "load byte, unsigned"},
                    "0000011101": {"short_name":  "lhu", "full_name": "load halfword, unsigned"},
                    "0010011000": {"short_name":  "addi", "full_name": "add immediate"},
                    "0010011010": {"short_name":  "slti", "full_name": "set if less than immediate"},
                    "0010011011": {"short_name":  "sltiu", "full_name": "set if less than immediate, unsigned"},
                    "0010011100": {"short_name":  "xori", "full_name": "exclusive-OR immediate"},
                    "0010011110": {"short_name":  "ori", "full_name": "OR immediate"},
                    "0010011111": {"short_name":  "andi", "full_name": "AND immediate"}}
        try:
            i_instruction_lookup[instruction_lookup_value]
        except KeyError:
            error_message = "Invalid func3. Your instruction is not valid."
            errorcheck.system_exit(error_message)
        else:
            header_info.update(i_instruction_lookup[instruction_lookup_value])

        # Create general info dict.
        general_info = {"instruction_type": "I-Type",
                        "instruction_set": "RV32I",
                        "opcode": opcode,
                        "func3": func3}

        # Create rs1 dict.
        rs1_info = decode.register_conversion(decode.get_rs1(instruction))

        # Create rd dict.
        rd_info = decode.register_conversion(decode.get_rd(instruction))

        # Create imm. dict.
        immediate = instruction[0:12]
        imm_info = {"binary_value": "immediate"}
        if header_info["short_name"] in ("sltiu", "sltu", "lbu", "lhu"):
            imm_info.update(decode.unsigned_immediate_conversion(immediate))
        else:
            imm_info.update(decode.signed_immediate_conversion(immediate))

        # Create assembly info dict
        assembly_info = {"name": header_info["short_name"],
                         "rd": rd_info["alias"],
                         "rs1": rs1_info["alias"],
                         "imm": imm_info["decimal_value"]}

        # Add all dicts to decoded instruction dict
        decoded_instruction = {"header_info": header_info,
                               "general_info": general_info,
                               "rs1_info": rs1_info,
                               "rd_info": rd_info,
                               "assembly_info": assembly_info}

        return decoded_instruction


'''
I-Instruction (Shift):
This separate class handles the shift immediate instructions.

Shift Instruction Components:
Opcode
Func3
SHAMT (6-digit, but SHAMT[5] always equals 0)

Shift Instructions: slli, srli, srai


                    "00100110010000000": {"short_name":  "slli", "full_name": "shift left logical immediate"},
                    "00100111010000000": {"short_name":  "srli", "full_name": "shift right logical immediate"},
                    "00100111010100000": {"short_name":  "srai", "full_name": "shift right arithmetic immediate"}
'''
class IInstructionShift:

    def get_general_data(self):
        pass

    def decode_instruction(self):
        pass
