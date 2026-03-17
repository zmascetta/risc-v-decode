from pathlib import Path
import json, typer


def lookup_instruction(instruction_type, lookup_value):
    path = Path(__file__).parent / "instruction_list.json"

    with path.open(mode="r") as file:
        instruction_info = json.load(file)
    try:
        instruction_info[instruction_type][lookup_value]
    except KeyError:
        print("Your instruction is not valid.")
        raise typer.Exit(code=1)
    else:
        return instruction_info[instruction_type][lookup_value]["full_name"], instruction_info[instruction_type][lookup_value]["short_name"], instruction_info[instruction_type][lookup_value]["source"]


def create_header_info(instruction, spacing_list, spacing_label, instruction_type, lookup_value):

    full_name, short_name, source = lookup_instruction(instruction_type, lookup_value)

    instruction_hex = str(hex(int(instruction, 2)))

    return {"instruction": instruction, "instruction_hex": instruction_hex, "spacing_list": spacing_list, "spacing_label": spacing_label, "full_name": full_name, "short_name": short_name, "source": source}