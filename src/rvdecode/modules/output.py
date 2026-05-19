from rich import print
from . import console

HEADER_VALUES = {"rs1_info": "Source Register 1 (rs1)",
                    "rs2_info": "Source Register 2 (rs2)",
                    "rd_info": "Destination Register (rd)",
                    "shamt_info": "Shift Amount",
                    "imm_info": "Immediate",
                    "u_imm_instr_info": "Value In Instruction",
                    "u_imm_final_info": "Final Value (Zero Extended)",
                    "off_info": "Offset",
                    "b_off_instr_info": "Value In Instruction",
                    "b_off_final_info": "Final Value (Position Corrected And Zero Extended)",
                    "general_info": "General Information",
                    "assembly_info": "Assembly Code",
                 }


def format_label(label):
    label = label.replace("_"," ")
    label = label.title()
    return label

# function to print a spaced instruction
# takes in the instruction and the "spacing_list"
# spacing_list = where to insert the spaces, or how many digits to group together
def print_spaced_instruction(instruction, spacing_list):
    insert_space = spacing_list[0] - 1
    spacing_total = len(spacing_list) - 1

    x = 0
    y = 1
    length = len(instruction)
    while x < length:
        if x == insert_space:
            print(instruction[x] + " ", end="")
            if y < spacing_total:
                insert_space = insert_space + spacing_list[y]
            y += 1
            x += 1
        else:
            print(instruction[x], end="")
            x += 1
    print("\n")

def print_header(header_info):
    print(
        f'''[b][u]{header_info["full_name"].title()} ({header_info["short_name"]})[/b][/u]
{header_info["instruction"]}
{header_info["instruction_hex"]}
    [b]\n{header_info["spacing_label"]}[/b]''',end="")
    print_spaced_instruction(header_info["instruction"], header_info["spacing_list"])

def print_data(data):
    for label, value in data.items():
        value = str(value)
        print(format_label(label) + ": ", end="")
        console.console.print(value, style="cyan bold")
    print()

def print_data_header(data):
    if data is "off_instr_info" or data is "u_imm_instr_info":
        console.console.print("Offset", style="bold underline")
        console.console.print(f"{HEADER_VALUES[data]}", style="bold")
    elif data is "off_final_info" or data is "u_imm_final_info":
        console.console.print(f"{HEADER_VALUES[data]}", style="bold")
    else:
        console.console.print(f"{HEADER_VALUES[data]}", style="bold underline")


def output_instruction(decoded_instruction):
    # print header info, store assembly text, remove both so other dicts. can be looped through
    print_header(decoded_instruction["header_info"])
    decoded_instruction.pop("header_info")
    assembly_text = decoded_instruction["assembly_info"]
    decoded_instruction.pop("assembly_info")

    # loop for printing remaining data
    for data in decoded_instruction:
        print_data_header(data)
        print_data(decoded_instruction[data])

    # print assembly
    console.console.print("Assembly Code", style="bold underline")
    console.console.print(assembly_text)