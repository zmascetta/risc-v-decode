from rvdecode.modules.helper import decode as decode, errorcheck as errorcheck, header as header, convert as convert

'''
R-Instruction
 Components: Opcode, Func3, Func7, RS1, RS2, RD
'''
def decode_instruction(instruction, opcode):
    func3 = decode.get_func3(instruction)
    func7 = decode.get_func7(instruction)
    lookup_value = opcode+func3+func7
    spacing_list = (7, 5, 5, 3, 5, 7)
    spacing_label = "f7----| rs2-| rs1-| f3| rd--| opcode|\n"

    # Create header dict.
    header_info = header.create_header_info(instruction, spacing_list, spacing_label, "r-type", lookup_value)

    # Create general info dict.
    general_info = {"instruction_type": "R-Type",
                    "instruction_set": header_info["source"],
                    "opcode": opcode,
                    "func3": func3,
                    "func7": func7}

    # Create rs1 dict.
    rs1_info = convert.register_conversion(decode.get_rs1(instruction))

    # Create rs2 dict.
    rs2_info = convert.register_conversion(decode.get_rs2(instruction))

    # Create rd dict.
    rd_info = convert.register_conversion(decode.get_rd(instruction))

    # Create assembly text
    assembly_text = decode.make_assembly_code(header_info["short_name"], rd=rd_info["alias"], rs1=rs1_info["alias"], rs2=rs2_info["alias"])

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                            "general_info": general_info,
                           "rs1_info": rs1_info,
                           "rs2_info": rs2_info,
                           "rd_info": rd_info,
                           "assembly_info": assembly_text}

    return decoded_instruction
