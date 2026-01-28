from rvdecode.modules.helper import decode as decode, errorcheck as errorcheck, header as header, convert as convert

'''
S-Instruction:
Components: Opcode, Func3, RS1, RS2, Offset
'''
def decode_instruction(instruction, opcode):
    func3 = decode.get_func3(instruction)
    lookup_value = opcode+func3
    spacing_list = (7, 5, 5, 3, 5, 7)
    spacing_label = "off---| rs2-| rs1-| f3| off-| opcode|\n"

    # Create header dict.
    header_info = header.create_header_info(instruction, spacing_list, spacing_label, "s-type", lookup_value)

    # Create general info dict.
    general_info = {"instruction_type": "S-Type",
                    "source": header_info["source"],
                    "opcode": opcode,
                    "func3": func3}

    # Create rs1 dict.
    rs1_info = convert.register_conversion(decode.get_rs1(instruction))

    # Create rs2 dict.
    rs2_info = convert.register_conversion(decode.get_rs2(instruction))

    # Create offset dict
    offset = instruction[0:8] + instruction[20:25]
    off_info = {"binary": offset}
    off_info.update(convert.signed_conversion(offset))

    # Create assembly text
    assembly_text = decode.make_assembly_code(header_info["short_name"], rs1=rs1_info["alias"], rs2=rs2_info["alias"], imm=off_info["decimal"])

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                           "general_info": general_info,
                           "rs1_info": rs1_info,
                           "rs2_info": rs2_info,
                           "off_info": off_info,
                           "assembly_info": assembly_text}

    return decoded_instruction