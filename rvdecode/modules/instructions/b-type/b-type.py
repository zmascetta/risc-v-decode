from rvdecode.modules.helper import decode as decode, errorcheck as errorcheck, header as header, convert as convert

'''
B-Instruction
 Components: Opcode, Func3, Func7, RS1, RS2, Imm
'''
def decode_instruction(instruction, opcode):
    func3 = decode.get_func3(instruction)
    lookup_value = opcode+func3
    spacing_list = (7, 5, 5, 3, 5, 7)
    spacing_label = "off---| rs2-| rs1-| f3| off-| opcode|\n"

    # Create header dict.
    header_info = header.create_header_info(instruction, spacing_list, spacing_label, "b-type", lookup_value)

    # Create general info dict.
    general_info = {"instruction_type": "B-Type",
                    "source": header_info["source"],
                    "opcode": opcode,
                    "func3": func3}

    # Create rs1 dict.
    rs1_info = convert.register_conversion(decode.get_rs1(instruction))

    # Create rs2 dict.
    rs2_info = convert.register_conversion(decode.get_rs2(instruction))

    # Create offset dicts.

    off_instr_info = {"binary_value": instruction[0:8] + " " + instruction[20:24]}

    final_value = instruction[0:1] + instruction[24:25] + instruction[1:7] + instruction[20:24] + "0"
    off_final_info = {"binary_value": final_value}

    # check if signed or unsigned for correct conversion
    unsigned_list = ("bltu", "bgeu")
    if header_info["short_name"] in unsigned_list:
        off_final_info.update(convert.unsigned_conversion(final_value))
    else:
        off_final_info.update(convert.signed_conversion(final_value))

    # Create assembly text
    assembly_text = decode.make_assembly_code(header_info["short_name"], rs1=rs1_info["alias"], rs2=rs2_info["alias"], imm=off_final_info["decimal_value"])

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                            "general_info": general_info,
                           "rs1_info": rs1_info,
                           "rs2_info": rs2_info,
                           "off_instr_info": off_instr_info,
                           "off_final_info": off_final_info,
                           "assembly_info": assembly_text}

    # offset
    return decoded_instruction