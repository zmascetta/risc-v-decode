from rvdecode.modules.helper import errorcheck

############
# ASSEMBLY #
############
# for looking up assembly instruction

# "short_name", "full_name", "instruction_set"
ASSEMBLY_LOOKUP = {"0110111": {"short_name":  "lui", "full_name": "load upper immediate"},
                    "0010111": {"short_name":  "auipc", "full_name": "add upper immediate to pc"},
                    "1101111": {"short_name":  "jal", "full_name": "jump and link"},
                    "1100011000": {"short_name":  "beq", "full_name": "branch if equal"},
                    "1100011001": {"short_name":  "bne", "full_name": "branch if not equal"},
                    "1100011100": {"short_name":  "blt", "full_name": "branch if less than"},
                    "1100011101": {"short_name":  "bge", "full_name": "branch if greater than or equal"},
                    "1100011110": {"short_name":  "bltu", "full_name": "branch if less than, unsigned"},
                    "1100011111": {"short_name":  "bgeu", "full_name": "branch if greater than or equal, unsigned"},
                    "0100011000": {"short_name":  "sb", "full_name": "store byte"},
                    "0100011001": {"short_name":  "sh", "full_name": "store halfword"},
                    "0100011010": {"short_name":  "sw", "full_name": "store word"},
}

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