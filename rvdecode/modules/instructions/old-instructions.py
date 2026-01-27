# RV32I instruction set

from rvdecode.modules.helper import decode as decode, errorcheck as errorcheck


INSTRUCTION_TYPES = {"1101111": "J-Type",
                        "1100011": "B-Type",
                        "0110011": "R-Type",
                        "0100011": "S-Type",
                        "0110111": "U-Type",
                        "0010111": "U-Type",
                        "0000011": "I-Type",
                        "0010011": "I-Type"}

def create_header_info(instruction, instruction_type, func3, func7=None):

    if instruction_type == "r_instruction":
        instruction_lookup_value = func3 + func7
        instruction_lookup_array = {
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
        error_message ="Invalid func3 and/or func7."

    elif instruction_type == "i_instruction":
        instruction_lookup_value = func3 + func7
        instruction_lookup_array = {
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
        error_message ="Invalid func3 and/or func7."
    else:
        return

    try:
        instruction_lookup_array[instruction_lookup_value]
    except KeyError:
        error_message = error_message + "Your instruction is not valid."
        return errorcheck.system_exit(error_message)
    else:
        header_info = {"full_name": instruction_lookup_array[instruction_lookup_value]["full_name"],
                        "short_name": instruction_lookup_array[instruction_lookup_value]["short_name"]}

    header_info.update({"instruction": instruction, "spacing_list": spacing_list, "spacing_label": spacing_label})

    spacing_list_reference = {

        "i_type": {"spacing_list": (12, 5, 3, 5, 7), "spacing_label": "imm--------| rs1-| f3| rd--| opcode|\n"},
        "shift": {"spacing_list": (7, 5, 5, 3, 5, 7), "spacing_label": "f7----|shamt| rs1-| f3| rd--| opcode|\n"},
        "s-type": {"spacing_list": (7, 5, 5, 3, 5, 7), "spacing_label": "imm---| rs2-| rs1-| f3| imm-| opcode|\n"},
        "b-type": {"spacing_list": (7, 5, 5, 3, 5, 7), "spacing_label": "imm---| rs2-| rs1-| f3| imm-| opcode|\n"},
        "u-type": {"spacing_list": (20, 5, 7), "spacing_label": "imm----------------| rd--| opcode|\n"},
        "j-type": {"spacing_list": (20, 5, 7), "spacing_label": "imm----------------| rd--| opcode|\n"}, }


    return header_info

# INSTRUCTION FUNCTIONS



