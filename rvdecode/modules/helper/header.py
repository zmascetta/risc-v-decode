import json

from rvdecode.modules.helper import errorcheck as errorcheck


def lookup_instruction(instruction_type, lookup_value):
    file_location = f"modules/instructions/{instruction_type}/{instruction_type}.json"

    with open(file_location, 'r') as file:
        instruction_info = json.load(file)

    try:
        instruction_info[lookup_value]
    except KeyError:
        error_message = "Your instruction is not valid."
        return errorcheck.system_exit(error_message)
    else:
        return instruction_info[lookup_value]["full_name"], instruction_info[lookup_value]["short_name"], instruction_info[lookup_value]["source"]


def create_header_info(instruction, spacing_list, spacing_label, instruction_type, lookup_value):

    full_name, short_name, source = lookup_instruction(instruction_type, lookup_value)

    instruction_hex = str(hex(int(instruction, 2)))


    return {"instruction": instruction, "instruction_hex": instruction_hex, "spacing_list": spacing_list, "spacing_label": spacing_label, "full_name": full_name, "short_name": short_name, "source": source}