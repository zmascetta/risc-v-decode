from . import errorcheck

############
# ASSEMBLY #
############
# for looking up assembly instruction

# "short_name", "full_name", "instruction_set"
ASSEMBLY_LOOKUP = {"0110111": {"short_name":  "lui", "full_name": "load upper immediate", "instruction_set": "RV32I, RV64I"},
                    "0010111": {"short_name":  "auipc", "full_name": "add upper immediate to pc", "instruction_set": "RV32I, RV64I"},
                    "1101111": {"short_name":  "jal", "full_name": "jump and link", "instruction_set": "RV32I, RV64I"},
                    "1100011000": {"short_name":  "beq", "full_name": "branch if equal", "instruction_set": "RV32I, RV64I"},
                    "1100011001": {"short_name":  "bne", "full_name": "branch if not equal", "instruction_set": "RV32I, RV64I"},
                    "1100011100": {"short_name":  "blt", "full_name": "branch if less than", "instruction_set": "RV32I, RV64I"},
                    "1100011101": {"short_name":  "bge", "full_name": "branch if greater than or equal", "instruction_set": "RV32I, RV64I"},
                    "1100011110": {"short_name":  "bltu", "full_name": "branch if less than, unsigned", "instruction_set": "RV32I, RV64I"},
                    "1100011111": {"short_name":  "bgeu", "full_name": "branch if greater than or equal, unsigned", "instruction_set": "RV32I, RV64I"},
                    "0100011000": {"short_name":  "sb", "full_name": "store byte", "instruction_set": "RV32I, RV64I"},
                    "0100011001": {"short_name":  "sh", "full_name": "store halfword", "instruction_set": "RV32I, RV64I"},
                    "0100011010": {"short_name":  "sw", "full_name": "store word", "instruction_set": "RV32I, RV64I"},
                    "01100110000000000": {"short_name":  "add", "full_name": "add", "instruction_set": "RV32I, RV64I"},
                    "01100110000100000": {"short_name":  "sub", "full_name": "subtract", "instruction_set": "RV32I, RV64I"},
                    "01100110010000000": {"short_name":  "sll", "full_name": "shift left logical", "instruction_set": "RV32I, RV64I"},
                    "01100110100000000": {"short_name":  "slt", "full_name": "set if less than", "instruction_set": "RV32I, RV64I"},
                    "01100110110000000": {"short_name":  "sltu", "full_name": "set if less than, unsigned", "instruction_set": "RV32I, RV64I"},
                    "01100111000000000": {"short_name":  "xor", "full_name": "exclusive-OR", "instruction_set": "RV32I, RV64I"},
                    "01100111010000000": {"short_name":  "srl", "full_name": "shift right logical", "instruction_set": "RV32I, RV64I"},
                    "01100111010100000": {"short_name":  "sra", "full_name": "shift right arithmetic", "instruction_set": "RV32I, RV64I"},
                    "01100111100000000": {"short_name":  "or", "full_name": "OR", "instruction_set": "RV32I, RV64I"},
                    "01100111110000000": {"short_name":  "and", "full_name": "AND", "instruction_set": "RV32I, RV64I"},
                    "1100111000": {"short_name":  "jalr", "full_name": "jump and link register", "instruction_set": "RV32I, RV64I"},
                    "0000011000": {"short_name":  "lb", "full_name": "load byte", "instruction_set": "RV32I, RV64I"},
                    "0000011001": {"short_name":  "lh", "full_name": "load halfword", "instruction_set": "RV32I, RV64I"},
                    "0000011010": {"short_name":  "lw", "full_name": "load word", "instruction_set": "RV32I, RV64I"},
                    "0000011100": {"short_name":  "lbu", "full_name": "load byte, unsigned", "instruction_set": "RV32I, RV64I"},
                    "0000011101": {"short_name":  "lhu", "full_name": "load halfword, unsigned", "instruction_set": "RV32I, RV64I"},
                    "0010011000": {"short_name":  "addi", "full_name": "add immediate", "instruction_set": "RV32I, RV64I"},
                    "0010011010": {"short_name":  "slti", "full_name": "set if less than immediate", "instruction_set": "RV32I, RV64I"},
                    "0010011011": {"short_name":  "sltiu", "full_name": "set if less than immediate, unsigned", "instruction_set": "RV32I, RV64I"},
                    "0010011100": {"short_name":  "xori", "full_name": "exclusive-OR immediate", "instruction_set": "RV32I, RV64I"},
                    "0010011110": {"short_name":  "ori", "full_name": "OR immediate", "instruction_set": "RV32I, RV64I"},
                    "0010011111": {"short_name":  "andi", "full_name": "AND immediate", "instruction_set": "RV32I, RV64I"},
                    "00100110010000000": {"short_name":  "slli", "full_name": "shift left logical immediate", "instruction_set": "RV32I, RV64I"},
                    "00100111010000000": {"short_name":  "srli", "full_name": "shift right logical immediate", "instruction_set": "RV32I, RV64I"},
                    "00100111010100000": {"short_name":  "srai", "full_name": "shift right arithmetic immediate", "instruction_set": "RV32I, RV64I"}}

def get_assembly_data(decoded_instruction):
    assembly_data = {"instruction": decoded_instruction["instruction_data"]["instruction"]}

    # lookup instruction with combo of opcode + func3 + func7 (if available)
    assembly_lookup = decoded_instruction["general_data"]["opcode"]

    if "func3" in decoded_instruction["general_data"].keys():
        assembly_lookup += decoded_instruction["general_data"]["func3"]
    if "func7" in decoded_instruction["general_data"].keys():
        assembly_lookup += decoded_instruction["general_data"]["func7"]

    try:
        ASSEMBLY_LOOKUP[assembly_lookup]
    except KeyError:
        error_message = "Invalid func3/func7. Your instruction is not valid."
        errorcheck.system_exit(error_message)
    else:
        assembly_data.update(ASSEMBLY_LOOKUP[assembly_lookup])

    return assembly_data


def make_assembly_code(decoded_instruction):
    assembly_instruction_list = [decoded_instruction["instruction_data"]["short_name"]]
    #rd
    if "rd_data" in decoded_instruction.keys():
        assembly_instruction_list.append(decoded_instruction["rd_data"]["alias"])

    #rs1
    if "rs1_data" in decoded_instruction.keys():
        if decoded_instruction["rs1_data"]["decimal_value"] == 0:
            assembly_instruction_list.append(decoded_instruction["rs1_data"]["name"])
        else:
            assembly_instruction_list.append(decoded_instruction["rs1_data"]["alias"])

    #rs2
    if "rs2_data" in decoded_instruction.keys():
        if decoded_instruction["rs2_data"]["decimal_value"] == 0:
            assembly_instruction_list.append(decoded_instruction["rs2_data"]["name"])
        else:
            assembly_instruction_list.append(decoded_instruction["rs2_data"]["alias"])

    #shamt
    if "shamt_data" in decoded_instruction.keys():
        assembly_instruction_list.append(str(decoded_instruction["shamt_data"]["decimal_value"]))

    #immediate
    if "immediate_data" in decoded_instruction.keys():
        assembly_instruction_list.append(str(decoded_instruction["immediate_data"]["decimal_value"]))

    # add formatting
    # do not add a comma if component is the first or the last component
    length = len(assembly_instruction_list)
    x = 0
    assembly_instruction = ""
    while x < length:
        if x > 0 and x < length - 1:
            assembly_instruction += assembly_instruction_list[x] + ", "
        else:
            assembly_instruction += assembly_instruction_list[x] + " "
        x += 1

    return assembly_instruction