from rvdecode.modules.helper import decode as decode, errorcheck as errorcheck


'''
S-Instruction:
Components: Opcode, Func3, RS1, RS2
'''
def s_instruction(instruction, opcode, func3):
    # Create header dict.
    header_info = create_header_info(instruction, "s_instruction")

    # func3 is lookup value
    instruction_lookup = {
        "000": {"short_name": "sb", "full_name": "store byte"},
        "001": {"short_name": "sh", "full_name": "store halfword"},
        "010": {"short_name": "sw", "full_name": "store word"}}
    header_info.update(decode.instruction_lookup(func3, instruction_lookup, "Invalid func3."))

    # Create general info dict.
    general_info = {"instruction_type": "S-Type",
                    "instruction_set": INSTRUCTION_SET,
                    "opcode": opcode,
                    "func3": func3}

    # Create rs1 dict.
    rs1_info = decode.register_conversion(decode.get_rs1(instruction))

    # Create rs2 dict.
    rs2_info = decode.register_conversion(decode.get_rs2(instruction))

    # Create assembly info dict
    assembly_info = {"name": header_info["short_name"],
                     "rs1": rs1_info["alias"],
                     "rs2": rs2_info["alias"],
                     }

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                           "general_info": general_info,
                           "rs1_info": rs1_info,
                           "rs2_info": rs2_info,
                           "assembly_info": assembly_info}

    return decoded_instruction