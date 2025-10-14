from . import errorcheck

# registers
def get_rs1(instruction):
    return instruction[12:17]

def get_rs2(instruction):
    return instruction[7:12]

def get_rd(instruction):
    return instruction[20:25]

# immediate
def get_immediate(instruction, instruction_type, size):
    if instruction_type == "I-Type":
        immediate = instruction[0:12]
    elif instruction_type == "S-Type":
        immediate = instruction[0:8] + instruction[20:25]
    elif instruction_type == "B-Type":
        immediate = instruction[0:0] + instruction[24:25] + instruction[1:7] + instruction[20:24]
    elif instruction_type == "U-Type":
        immediate = instruction[0:20]
    else: #J-Type
        immediate = instruction[0:1] + instruction[12:20] + instruction[11:12] + instruction[1:11]

    return immediate

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


def decode_instruction(instruction):
    # checks identify which instruction types need which components
    # written out in lists to allow for more instruction types to be added
    rs1_check = ("R-Type", "I-Type", "I-Type (Shift)", "S-Type", "B-Type", )
    rs2_check = ("R-Type", "S-Type", "B-Type")
    rd_check = ("R-Type", "I-Type", "I-Type (Shift)", "U-Type", "J-Type")
    shamt_check = ("I-Type (Shift)")
    imm_check = ("I-Type", "S-Type", "B-Type", "U-Type", "J-Type")
    func3_check = ("R-Type", "I-Type", "I-Type (Shift)", "S-Type", "B-Type")
    func7_check = ("R-Type", "I-Type (Shift)")

    # get opcode and instruction type
    opcode = get_opcode(instruction)
    instruction_type = get_instruction_type(opcode)

    # account for different instruction composition for I-Type shift instructions
    if instruction_type == "I-Type":
        func3 = get_func3(instruction)
        if func3 in ("001", "101"):
            instruction_type = "I-Type (Shift)"

    # initialize decoded instruction dict. with opcode and instr. type values
    decoded_instruction = {"opcode": opcode,
                           "instruction_type": instruction_type}

    #RS1
    if instruction_type in rs1_check:
        decoded_instruction.update = {"rs1": get_rs1(instruction)}

    #RS2
    if instruction_type in rs2_check:
        decoded_instruction.update = {"rs2": get_rs2(instruction)}

    #RD
    if instruction_type in rd_check:
        decoded_instruction.update = {"rd": get_rd(instruction)}

    #SHAMT
    # shamt occupies same space as rs2
    if instruction_type in shamt_check:
        decoded_instruction.update = {"shamt": get_rs2(instruction)}

    #IMMEDIATE
    if instruction_type in imm_check:
        decoded_instruction.update = {"immediate": get_immediate(instruction, instruction_type, 32)}

    #FUNC3
    if instruction_type in func3_check:
        decoded_instruction.update = {"func3": get_func3(instruction)}

    #FUNC7
    if instruction_type in func7_check:
        decoded_instruction.update = {"func7": get_func7(instruction)}

    return decoded_instruction