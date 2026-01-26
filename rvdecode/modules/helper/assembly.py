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


def make_assembly_code(name, rd=None, rs1=None, rs2=None, shamt=None, imm=None):
    assembly_components = locals()

    assembly_list = []
    for key, val in assembly_components.items():
        if val is not None:
            if key in ("rs1", "rs2") and val == "x0":
                assembly_list.append("0")
            else:
                assembly_list.append(val)

    # add formatting
    # do not add a comma if component is the first or the last component
    length = len(assembly_list)
    x = 0
    assembly_text = ""
    while x < length:
        if x > 0 and x < length - 1:
            assembly_text += assembly_list[x] + ", "
        else:
            assembly_text += assembly_list[x] + " "
        x += 1

    return assembly_text