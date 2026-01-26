import json, errorcheck

def create_header_info(instruction_set, lookup_value):
    file_location = "../instructions/" + instruction_set + "/" + instruction_set + ".json"

    with open(file_location, 'r') as file:
        data = json.load(file)
        spacing_list = data["spacing_list"]
        instruction_info = data["instruction_info"]

    try:
        instruction_lookup_array[instruction_lookup_value]
    except KeyError:
        error_message = error_message + "Your instruction is not valid."
        return errorcheck.system_exit(error_message)
    else:
        header_info = {"full_name": instruction_lookup_array[instruction_lookup_value]["full_name"],
                        "short_name": instruction_lookup_array[instruction_lookup_value]["short_name"]}

    header_info.update({"instruction": instruction, "spacing_list": spacing_list, "spacing_label": spacing_label})