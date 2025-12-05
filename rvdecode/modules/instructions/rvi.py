# RV32I instruction set

from ..helper import decode as decode, errorcheck as errorcheck

INSTRUCTION_SET = "RV32I"

SPACING_LIST = {
        "r_type": {"spacing_list": (7, 5, 5, 3, 5, 7), "label": "f7----| rs2-| rs1-| f3| rd--| opcode|\n"},
        "i_type": {"spacing_list": (12, 5, 3, 5, 7), "label": "imm--------| rs1-| f3| rd--| opcode|\n"},
        "shift": {"spacing_list": (7, 5, 5, 3, 5, 7), "label": "f7----|shamt| rs1-| f3| rd--| opcode|\n"},
        "s-type": {"spacing_list": (7, 5, 5, 3, 5, 7), "label": "imm---| rs2-| rs1-| f3| imm-| opcode|\n"},
        "b-type": {"spacing_list": (7, 5, 5, 3, 5, 7), "label": "imm---| rs2-| rs1-| f3| imm-| opcode|\n"},
        "u-type": {"spacing_list": (20, 5, 7), "label": "imm----------------| rd--| opcode|\n"},
        "j-type": {"spacing_list": (20, 5, 7), "label": "imm----------------| rd--| opcode|\n"},}

def create_header_info(instruction, instruction_type):
    header_info = {"instruction": instruction,
                    "spacing_list": SPACING_LIST[instruction_type]["spacing_list"],
                    "label": SPACING_LIST[instruction_type]["label"],}
    return header_info

# INSTRUCTION FUNCTIONS
'''
R-Instruction
 Components: Opcode, Func3, Func7, RS1, RS2, RD
'''
def r_instruction(instruction, opcode, func3):
    
    # Create header dict.
    header_info = create_header_info(instruction, "r_instruction")

    func7 = decode.get_func7(instruction)
    instruction_lookup_value = func3 + func7
    instruction_lookup = {
        "0000000000": {"short_name": "add", "full_name": "add"},
        "0000100000": {"short_name": "sub", "full_name": "subtract"},
        "0010000000": {"short_name": "sll", "full_name": "shift left logical"},
        "0100000000": {"short_name": "slt", "full_name": "set if less than"},
        "0110000000": {"short_name": "sltu", "full_name": "set if less than, unsigned"},
        "1000000000": {"short_name": "xor", "full_name": "exclusive-OR"},
        "1010000000": {"short_name": "srl", "full_name": "shift right logical"},
        "1010100000": {"short_name": "sra", "full_name": "shift right arithmetic"},
        "1100000000": {"short_name": "or", "full_name": "OR"},
        "1110000000": {"short_name": "and", "full_name": "AND"}
        }
    try:
        instruction_lookup[instruction_lookup_value]
    except KeyError:
        error_message = "Invalid func3 and/or func7. Your instruction is not valid."
        errorcheck.system_exit(error_message)
    else:
        header_info.update(instruction_lookup[instruction_lookup_value])

    # Create general info dict.
    general_info = {"instruction_type": "R-Type",
                    "instruction_set": INSTRUCTION_SET,
                    "opcode": opcode,
                    "func3": func3,
                    "func7": func7}

    # Create rs1 dict.
    rs1_info = decode.register_conversion(decode.get_rs1(instruction))

    # Create rs2 dict.
    rs2_info = decode.register_conversion(decode.get_rs2(instruction))

    # Create rd dict.
    rd_info = decode.register_conversion(decode.get_rd(instruction))

    # Create assembly info dict
    assembly_info = {"name": header_info["short_name"],
                     "rd": rd_info["alias"],
                     "rs1": rs1_info["alias"],
                     "rs2": rs2_info["alias"]}

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                           "general_info": general_info,
                           "rs1_info": rs1_info,
                           "rs2_info": rs2_info,
                           "rd_info": rd_info,
                           "assembly_info": assembly_info}

    return decoded_instruction

'''
I-Instruction
Handles the signed/unsigned NON-SHIFT i-instructions.
Components: Opcode, Func3, RS1, RD, Immediate (12-digit, signed/unsigned)
Unsigned instructions: sltiu, sltu, lbu, lhu
'''
def i_instruction(instruction, opcode, func3):

    # Create header dict.
    header_info = create_header_info(instruction,"i_type")

    instruction_lookup_value = opcode + func3
    instruction_lookup = {
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
        instruction_lookup[instruction_lookup_value]
    except KeyError:
        error_message = "Invalid func3. Your instruction is not valid."
        errorcheck.system_exit(error_message)
    else:
        header_info.update(instruction_lookup[instruction_lookup_value])

    # Create general info dict.
    general_info = {"instruction_type": "I-Type",
                    "instruction_set": INSTRUCTION_SET,
                    "opcode": opcode,
                    "func3": func3}

    # Create rs1 dict.
    rs1_info = decode.register_conversion(decode.get_rs1(instruction))

    # Create rd dict.
    rd_info = decode.register_conversion(decode.get_rd(instruction))

    # Create imm. dict.
    immediate = instruction[0:12]
    imm_info = {"binary_value": immediate}
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
                           "imm_info": imm_info,
                           "assembly_info": assembly_info}

    return decoded_instruction


'''
I-Instruction (Shift):
Separate i-instruction function to handle the shift immediate instructions.
Components: Opcode, Func3, Func7, RS1, RD, SHAMT (6-digit, but SHAMT[5] always equals 0)
'''
def i_instruction_shift(instruction, opcode, func3):

    # Create header dict.
    header_info = create_header_info(instruction, "i_instruction")

    func7 = decode.get_func7(instruction)
    instruction_lookup_value = func3 + func7
    instruction_lookup = {
                "0010000000": {"short_name": "slli", "full_name": "shift left logical immediate"},
                "1010000000": {"short_name": "srli", "full_name": "shift right logical immediate"},
                "1010100000": {"short_name": "srai", "full_name": "shift right arithmetic immediate"}}
    try:
        instruction_lookup[instruction_lookup_value]
    except KeyError:
        error_message = "Invalid func3 and/or func7. Your instruction is not valid."
        errorcheck.system_exit(error_message)
    else:
        header_info.update(instruction_lookup[instruction_lookup_value])

    # Create general info dict.
    general_info = {"instruction_type": "I-Type (Shift)",
                    "instruction_set": INSTRUCTION_SET,
                    "opcode": opcode,
                    "func3": func3,
                    "func7": func7}

    # Create rs1 dict.
    rs1_info = decode.register_conversion(decode.get_rs1(instruction))

    # Create rd dict.
    rd_info = decode.register_conversion(decode.get_rd(instruction))

    # Create shamt dict.
    shamt = instruction[8:15]
    shamt_info = {"binary_value": shamt}
    shamt_info.update(decode.unsigned_immediate_conversion(shamt))

    # Create assembly info dict
    assembly_info = {"name": header_info["short_name"],
                     "rd": rd_info["alias"],
                     "rs1": rs1_info["alias"],
                     "imm": shamt_info["decimal_value"]}

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                           "general_info": general_info,
                           "rs1_info": rs1_info,
                           "rd_info": rd_info,
                           "shamt_info": shamt_info,
                           "assembly_info": assembly_info}

    return decoded_instruction
