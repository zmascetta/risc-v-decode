from rvdecode.modules.helper import assembly, errorcheck

# get opcode and instruction set
def get_opcode(instruction):
    return instruction[-7:]

# "source" refers to the ISA or the extension that the instruction comes from.
# i've chosen to call it this because it is easier to lump "base ISA" and "extension" together
# instead of trying to reference both of them.
# (e.g., calling the function get_isa_or_ext, using a variable called "isa_or_ext", etc.)
def get_source(opcode):
    # RV32I opcodes
    rv32i_opcodes = ("1101111", "1100011", "0110011", "0100011", "0110111","0010111", "0000011", "0010011")

    if opcode in rv32i_opcodes:
        source = "RV32I"
    else:
        extra_lines = "ERROR: Invalid opcode. Opcode belongs to an extension that is not currently supported. NOTE, RV-Decode does not support fence, ecall, ebreak, or CSR instructions."
        errorcheck.system_exit(extra_lines)

    return source

# identify instruction type via opcode
def get_instruction_type(opcode, instruction_list):
    try:
        instruction_type = instruction_list[opcode]
    except KeyError:
        extra_lines = "ERROR: Opcode in instruction is not valid."
        errorcheck.system_exit(extra_lines)
    else:
        return instruction_type

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


def create_general_info(type, source, opcode, func3=None, func7=None):
    general_info = {"instruction_type": type,
                    "source": source,
                    "opcode": opcode}

    if func3 is not None:
        general_info.update({"func3": func3})
    if func7 is not None:
        general_info.update({"func7": func7})

    return general_info