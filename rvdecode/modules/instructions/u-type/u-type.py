from rvdecode.modules.helper import decode as decode, errorcheck as errorcheck, header as header, convert as convert

'''
U-Instruction:
Components: Opcode, RD, Immediate
'''

def decode_instruction(instruction, opcode):
    lookup_value = opcode
    spacing_list = (20, 5, 7)
    spacing_label = "imm----------------| rd--| opcode|\n"

    # Create header dict.
    header_info = header.create_header_info(instruction, spacing_list, spacing_label, "u-type", lookup_value)

    # Create general info dict.
    general_info = {"instruction_type": "U-Type",
                    "source": header_info["source"],
                    "opcode": opcode}

    # Create rd dict.
    rd_info = convert.register_conversion(decode.get_rd(instruction))

    # Create immediate dicts.
    immediate = instruction[0:20]
    up_imm_instr_info = {"binary": immediate}
    up_imm_instr_info.update(convert.unsigned_conversion(immediate))

    immediate = immediate.ljust(32,"0")
    up_imm_final_info = {"binary": immediate}
    up_imm_final_info.update(convert.unsigned_conversion(immediate))

    # Create assembly text
    assembly_text = decode.make_assembly_code(header_info["short_name"], imm=up_imm_instr_info["hex"])

    # Add all dicts to decoded instruction dict
    decoded_instruction = {"header_info": header_info,
                           "general_info": general_info,
                           "rd_info": rd_info,
                           "up_imm_instr_info": up_imm_instr_info,
                           "up_imm_final_info": up_imm_final_info,
                           "assembly_info": assembly_text}

    return decoded_instruction