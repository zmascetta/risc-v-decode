from . import errorcheck

#registers
def get_rs1(instruction):
    return instruction[12:17]

def get_rs2(instruction):
    return instruction[7:12]

def get_rd(instruction):
    return instruction[20:25]

# funcs
def get_func3(instruction):
    return instruction[17:20]

def get_func7(instruction):
    return instruction[0:8]

# opcode
def get_opcode(instruction):
    return instruction[25:]

# identify instruction type via opcode
def get_instruction_type(opcode):
    instruction_reference = {"1101111": "J-type",
                             "1100011": "B-Type",
                             "0110011": "R-Type",
                             "0100011": "S-Type",
                             "0110111": "U-Type",
                             "0010111": "U-Type",
                             "0000011": "I-Type",
                             "0010011": "I-Type",
                             "0001111": "I-Type",
                             "1110011": "I-Type"}

    # exit if invalid opcode
    if opcode not in instruction_reference:
        extra_lines = "ERROR: Opcode in instruction is not valid."
        errorcheck.system_exit(extra_lines)

    return instruction_reference[opcode]


# decode functions for each instruction type
# R-Type
def decode_r_instruction(instruction):
    decoded_instruction = {"rs1": get_rs1(instruction),
                            "rs2": get_rs2(instruction),
                            "rd": get_rd(instruction),
                            "func3": get_func3(instruction),
                            "func7": get_func7(instruction)}

    return decoded_instruction


# I-Type
def decode_i_instruction(instruction):
    immediate = instruction[0:12]

    decoded_instruction = {"rs1": get_rs1(instruction),
                           "rd": get_rd(instruction),
                           "immediate": immediate}
    return decoded_instruction


# S-Type
def decode_s_instruction(instruction):
    immediate = instruction[0:8] + instruction[20:25]
    func3 = get_func3(instruction)

    # slli, srli, srai have s-type opcode but instruction resembles r-type.
    if func3 in ("001", "101"):
        decoded_instruction = {"rs1": get_rs1(instruction),
                               # rs2 field is effectively the shift amount for imm. versions of shift instr.
                               "shamt": get_rs2(instruction),
                               "rd": get_rd(instruction),
                               "func3": func3,
                               "func7": get_func7(instruction)}
    else:
        decoded_instruction = {"rs1": get_rs1(instruction),
                               "rs2": get_rs2(instruction),
                               "func3": func3,
                               "immediate": immediate}

    return decoded_instruction


# B-Type
def decode_b_instruction(instruction):
    immediate = instruction[0:0] + instruction[24:25] + instruction[1:7] + instruction[20:24]

    decoded_instruction = {"rs1": get_rs1(instruction),
                            "rs2": get_rs2(instruction),
                            "func3": get_func3(instruction),
                            "immediate": immediate}

    return decoded_instruction


# U-Type
def decode_u_instruction(instruction):
    immediate = instruction[0:20]

    decoded_instruction = {"rd": get_rd(instruction),
                            "immediate": immediate}

    return decoded_instruction


# J-Type
def decode_j_instruction(instruction):
    immediate = instruction[0:1] + instruction[12:20] + instruction[11:12] + instruction[1:11]

    decoded_instruction = {"rd": get_rd(instruction),
                           "immediate": immediate}

    return decoded_instruction


def decode_instruction(instruction):
    opcode = get_opcode(instruction)
    instruction_type = get_instruction_type(opcode)

    if instruction_type == "R-Type":
        decoded_instruction = decode_r_instruction(instruction)
    elif instruction_type == "I-Type":
        decoded_instruction = decode_i_instruction(instruction)
    elif instruction_type == "B-Type":
        decoded_instruction = decode_b_instruction(instruction)
    elif instruction_type == "S-Type":
        decoded_instruction = decode_s_instruction(instruction)
    elif instruction_type == "U-Type":
        decoded_instruction = decode_u_instruction(instruction)
    else:   #J-Type
        decoded_instruction = decode_j_instruction(instruction)

    decoded_instruction.update = {"type": instruction_type, "opcode": opcode}

    return decoded_instruction