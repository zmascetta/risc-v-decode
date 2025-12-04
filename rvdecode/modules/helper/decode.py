from rvdecode.modules.helper import assembly, errorcheck


##########
# DECODE #
##########
# These functions are used for decoding the instruction into its component parts.

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

# immediate
# this function produces up to 3 values:
# 1. "value_in_instruction" - this is exactly how the value appears in the instruction (full-width binary)
# 2. "bitshifted_value" - if the value appears in the instruction with its bits out of order
#    (b or j type), this shifts the bits into the actual order
# 3. "final_value" - this is the final, full-width binary value, including zero shifts or appended bits
def get_immediate(instruction, instruction_type, size):
    if instruction_type == "I-Type":
        immediate_data = {"value_in_instruction": instruction[0:12],
                            "final_value": instruction[0:12]}

    elif instruction_type == "S-Type":
        immediate_data = {"value_in_instruction": instruction[0:8] + " " + instruction[20:25],
                            "final_value": instruction[0:8] + instruction[20:25]}

    elif instruction_type == "B-Type":
        bitshifted_value = instruction[0:1] + instruction[24:25] + instruction[1:7] + instruction[20:25]
        final_value = bitshifted_value + "0"
        bitshifted_value = bitshifted_value[0:7] + " " + bitshifted_value[7:12]

        immediate_data ={"value_in_instruction": instruction[0:7] + " " + instruction[20:25],
                            "bitshifted_value": bitshifted_value,
                            "final_value": final_value}

    elif instruction_type == "U-Type":
        immediate_data = {"value_in_instruction": instruction[0:21],
                            "final_value": instruction[0:21].ljust(32,"0")}

    else: #J-Type
        bitshifted_value = instruction[0:1] + instruction[12:20] + instruction[11:12] + instruction[1:11]

        immediate_data = {"value_in_instruction": instruction[0:21],
                            "bitshifted_value": bitshifted_value,
                            "final_value": bitshifted_value + "0"}

    return immediate_data

# funcs
def get_func3(instruction):
    return instruction[17:20]

def get_func7(instruction):
    return instruction[0:7]

# opcode
def get_opcode(instruction):
    return instruction[25:]

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
                             "0001111": "error",
                             "1110011": "error"}

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


##############
# CONVERSION #
##############
#
# These functions are for converting the binary values of the components into
# values which are either more useful and/or easier to read.

REGISTER_REFERENCE = {"0": {"name": "x0", "alias": "zero", "use": "read-only (0)"},
                      "1": {"name": "x1", "alias": "ra", "use": "return address"},
                      "2": {"name": "x2", "alias": "sp", "use": "stack pointer"},
                      "3": {"name": "x3", "alias": "gp", "use": "global pointer"},
                      "4": {"name": "x4", "alias": "tp", "use": "thread pointer"},
                      "5": {"name": "x5", "alias": "t0", "use": "temporary"},
                      "6": {"name": "x6", "alias": "t1", "use": "temporary"},
                      "7": {"name": "x7", "alias": "t2", "use": "temporary"},
                      "8": {"name": "x8", "alias": "s0", "use": "saved"},
                      "9": {"name": "x9", "alias": "s1", "use": "saved"},
                      "10": {"name": "x10", "alias": "a0", "use": "arguments/return values"},
                      "11": {"name": "x11", "alias": "a1", "use": "arguments/return values"},
                      "12": {"name": "x12", "alias": "a2", "use": "arguments"},
                      "13": {"name": "x13", "alias": "a3", "use": "arguments"},
                      "14": {"name": "x14", "alias": "a4", "use": "arguments"},
                      "15": {"name": "x15", "alias": "a5", "use": "arguments"},
                      "16": {"name": "x16", "alias": "a6", "use": "arguments"},
                      "17": {"name": "x17", "alias": "a7", "use": "arguments"},
                      "18": {"name": "x18", "alias": "s2", "use": "saved"},
                      "19": {"name": "x19", "alias": "s3", "use": "saved"},
                      "20": {"name": "x20", "alias": "s4", "use": "saved"},
                      "21": {"name": "x21", "alias": "s5", "use": "saved"},
                      "22": {"name": "x22", "alias": "s6", "use": "saved"},
                      "23": {"name": "x23", "alias": "s7", "use": "saved"},
                      "24": {"name": "x24", "alias": "s8", "use": "saved"},
                      "25": {"name": "x25", "alias": "s9", "use": "saved"},
                      "26": {"name": "x26", "alias": "s10", "use": "saved"},
                      "27": {"name": "x27", "alias": "s11", "use": "saved"},
                      "28": {"name": "x28", "alias": "t3", "use": "temporary"},
                      "29": {"name": "x29", "alias": "t4", "use": "temporary"},
                      "30": {"name": "x30", "alias": "t5", "use": "temporary"},
                      "31": {"name": "x31", "alias": "t6", "use": "temporary"}}

def register_conversion(register_value):
    # convert from bin to dec for lookup
    decimal_value = str(int(register_value, base=2))
    register_data = {"binary_value": register_value,
                        "decimal_value": decimal_value,
                        "name": REGISTER_REFERENCE[decimal_value]["name"],
                        "alias": REGISTER_REFERENCE[decimal_value]["alias"],
                        "use": REGISTER_REFERENCE[decimal_value]["use"]
                     }
    return register_data

def twos_complement(immediate, size):
     # get mask with 2^k - 1
     mask = (2 ** size) - 1
     # bitwise xor
     value = mask ^ immediate
     # add 1
     value += 1
     # make value negative
     value = -value

     return value

def unsigned_immediate_conversion(immediate):

    immediate_decimal = int(immediate, base=2)
    immediate_data = {"decimal_value": immediate_decimal,
                        "hex_value": hex(immediate_decimal)}
    return immediate_data

def signed_immediate_conversion(immediate, size=32):
    # perform twos complement if negative
    if immediate[0:1] == "1":
        # get mask with 2^k - 1
        mask = (2 ** size) - 1
        # bitwise xor
        value = mask ^ immediate
        # add 1
        value += 1
        # make value negative
        value = -value
    else:
        immediate_decimal = int(immediate, base=2)

    immediate_data = {"decimal_value": immediate_decimal,
                        "hex_value": hex(immediate_decimal)}
    return immediate_data

def shamt_conversion(shamt):
    shamt_dec = int(shamt, base=2)

    shamt_data = {"binary_value": "shamt",
                    "decimal_value": shamt_dec}

    return shamt_data

##########
# DECODE #
##########
# this function will create a (mostly) 2D dictionary.
# each component of the instruction will have a corresponding dictionary that contains
# the detailed information for that component. there is also a "general" dict. for general info.
# the final entry in the dict. is "assembly", which holds a string value of the assembly code.
def decode_instruction(instruction):
    # these checks identify which instruction types need which components
    # written out in tuples to allow for more instruction types to be added
    rs1_check = ("R-Type", "I-Type", "I-Type (Shift)", "S-Type", "B-Type")
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

    # initialize the decoded instruction dict.
    decoded_instruction = {"instruction_data": {"instruction": instruction}}

    # initialize the "general" dict. with opcode and instr. type values
    general_data = {"opcode": opcode,
                    "instruction_type": instruction_type}

    # func3 and func7 do not need conversion
    # their values are extracted then added to the general_data dict.
    #FUNC3
    if instruction_type in func3_check:
        general_data.update({"func3": get_func3(instruction)})

    #FUNC7
    if instruction_type in func7_check:
        general_data.update({"func7": get_func7(instruction)})

    # add the final "general" dict. to decoded instr. dict
    decoded_instruction.update({"general_data": general_data})

    # get assembly data
    decoded_instruction.update({"instruction_data": assembly.get_assembly_data(decoded_instruction)})

    # each of the components follows the same flow:
    # a "decode" function (get_xxx) takes the full binary instruction and extracts the field from it.
    # this binary value is then passed to a "conversion" function (xxx_conversion) that converts it/provides more info.
    # the conversion functions returns a dictionary, which is added to the decoded_instruction dict.
    #RS1
    if instruction_type in rs1_check:
        decoded_instruction.update({"rs1_data": register_conversion(get_rs1(instruction))})

    #RS2
    if instruction_type in rs2_check:
        decoded_instruction.update({"rs2_data": register_conversion(get_rs2(instruction))})

    #RD
    if instruction_type in rd_check:
        decoded_instruction.update({"rd_data": register_conversion(get_rd(instruction))})

    #SHAMT
    # shamt occupies same space as rs2
    if instruction_type == shamt_check:
        decoded_instruction.update({"shamt_data": shamt_conversion(get_rs2(instruction))})

    #IMMEDIATE
    if instruction_type in imm_check:
        immediate_data = get_immediate(instruction, instruction_type, 32)
        immediate_data.update(immediate_conversion(immediate_data["final_value"], decoded_instruction["instruction_data"]["short_name"], 32))
        decoded_instruction.update({"immediate_data": immediate_data})

    #ASSEMBLY
    # update imm if necessary
    # make assembly instruction
    decoded_instruction.update({"assembly": assembly.make_assembly_code(decoded_instruction)})

    return decoded_instruction