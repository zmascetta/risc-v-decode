HEADER_VALUES = {"rs1_data": "Source Register 1 (rs1)",
                    "rs2_data": "Source Register 2 (rs2)",
                    "rd_data": "Destination Register (rd)",
                    "shamt_data": "Shift Amount",
                    "immediate_data": "Immediate",
                    "general_data": "General Information",
                    "assembly": "Assembly Code"}


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

def print_instruction(instruction_data, instruction_type):
    header = format_label(instruction_data["full_name"]) + " (" + instruction_data["short_name"] + ")"
    instruction = instruction_data["instruction"]
    print(header + "\n" + instruction + "\n")

    if instruction_type == "R-Type":
        spacing_list = (7, 5, 5, 3, 5, 7)
        label = "f7----| rs2-| rs1-| f3| rd--| opcode|\n"
    elif instruction_type == "I-Type":
        spacing_list = (12, 5, 3, 5, 7)
        label = "imm--------| rs1-| f3| rd--| opcode|\n"
    elif instruction_type == "S-Type" or instruction_type == "B-Type":
        spacing_list = (7, 5, 5, 3, 5, 7)
        label = "imm---| rs2-| rs1-| f3| imm-| opcode|"
    else:
        spacing_list = (20, 5, 7)
        label = "imm----------------| rd--| opcode|"

    print(label)
    print_spaced_instruction(instruction, spacing_list)


def print_data(data):
    for label, value in data.items():
        value = str(value)
        print(format_label(label) + ": " + value)
    print()


def print_data_header(data):
    print(HEADER_VALUES[data])


def output_instruction(decoded_instruction):

    # get instruction set from instruction_set dict and add it to the general_data dict.
    updated_general_data = {"instruction_set": decoded_instruction["instruction_data"]["instruction_set"]}
    updated_general_data.update(decoded_instruction["general_data"])
    decoded_instruction["general_data"] = updated_general_data

    # pop instruction data from decoded_instruction.
    # instruction_data has specific printing needs and shouldn't be printed using the general loop.
    instruction_data = decoded_instruction.pop("instruction_data")
    print_instruction(instruction_data, updated_general_data["instruction_type"])

    # pop assembly - it is just a string and doesn't ned the general oop either.
    assembly_value = decoded_instruction.pop("assembly")

    # loop for printing all the data
    for data in decoded_instruction:
        print_data_header(data)
        print_data(decoded_instruction[data])

    # print assembly code
    print_data_header("assembly")
    print(assembly_value)
