from rvdecode.modules.helper import decode as decode, errorcheck as errorcheck


'''
R-Instruction
 Components: Opcode, Func3, Func7, RS1, RS2, RD
'''


def r_instruction(instruction, opcode, func3):
    # Create header dict.
    header_info = create_header_info(instruction, "r_instruction")

    func7 = decode.get_func7(instruction)

    decode.instruction_name_lookup()

    # Create general info dict.
    general_info = {"instruction_type": "R-Type",
                    "instruction_set": INSTRUCTION_SET,
                    "opcode": opcode,
                    "func3": func3,
                    "func7": func7}

    # Create rs1 dict.
    rs1_info = decode.register_conversion(decode.get_rs1(instruction))

    # Create rs2 dict.
    rs2_info = decode.register_conversion(decode.get_rs2(instruction))

    # Create rd dict.
    rd_info = decode.register_conversion(decode.get_rd(instruction))

    # Create assembly info
    assembly_info = {"name": header_info["short_name"],
                     "rd": rd_info["alias"],
                     "rs1": rs1_info["alias"],
                     "rs2": rs2_info["alias"]}

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                           "general_info": general_info,
                           "rs1_info": rs1_info,
                           "rs2_info": rs2_info,
                           "rd_info": rd_info,
                           "assembly_info": assembly_info}

    return decoded_instruction
