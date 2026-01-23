from rvdecode.modules.helper import assembly, errorcheck

# get opcode and instruction set
def get_opcode(instruction):
    opcode = instruction[-7:]

    # fence, ecall, ebreak, or CSR instructions
    invalid_opcodes = ("0001111", "1110011")

    # RV32I opcodes
    rv32i_opcodes = ("1101111", "1100011", "0110011", "0100011", "0110111","0010111", "0000011", "0010011")

    if opcode in invalid_opcodes:
        extra_lines = "ERROR: Invalid opcode. RV-Decode does not support fence, ecall, ebreak, or CSR instructions."
        errorcheck.system_exit(extra_lines)

    if opcode in rv32i_opcodes:
        instruction_set = "RV32I"
    else:
        extra_lines = "ERROR: Invalid opcode. Opcode belongs to an extension that is not currently supported."
        errorcheck.system_exit(extra_lines)

    return opcode, instruction_set



# registers
def get_rs1(instruction):
    return instruction[12:17]

def get_rs2(instruction):
    return instruction[7:12]

def get_rd(instruction):
    rd = instruction[20:25]
    if rd == "00000":
        extra_lines = "ERROR: Attempt to write to x0."
        errorcheck.system_exit(extra_lines)

    return rd

# funcs
def get_func3(instruction):
    return instruction[17:20]

def get_func7(instruction):
    return instruction[0:7]



# identify instruction type via opcode
def get_instruction_type(opcode):
    instruction_reference = {"1101111": "J-Type",
                             "1100011": "B-Type",
                             "0110011": "R-Type",
                             "0100011": "S-Type",
                             "0110111": "U-Type",
                             "0010111": "U-Type",
                             "0000011": "I-Type",
                             "0010011": "I-Type",


    # exit if invalid opcode
    try:
        instruction_type = instruction_reference[opcode]
    except KeyError:
        extra_lines = "ERROR: Opcode in instruction is not valid."
        errorcheck.system_exit(extra_lines)
    else:
        if instruction_type == "error":
            extra_lines = "ERROR: RV-Decode does not support fence, ecall, ebreak, or CSR instructions."
            errorcheck.system_exit(extra_lines)
        else:
            return instruction_type


def create_general_info(type, set, opcode, func3=None, func7=None):
    general_info = {"instruction_type": type,
                    "instruction_set": set,
                    "opcode": opcode}

    if func3 is not None:
        general_info.update({"func3": func3})
    if func7 is not None:
        general_info.update({"func7": func7})

    return general_info