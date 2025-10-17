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


def print_instruction(instruction_data, instruction_type):
    header = format_label(instruction_data["full_name"]) + " (" + instruction_data["short_name"] + ")"
    instruction = instruction_data["instruction"]
    print(header + "\n" + instruction + "\n")



    if instruction_type == "R-Type":
        instruction = instruction[0:7] + " " + instruction[7:12] + " " + instruction[12:17] + " " + instruction[17:20] + " " + instruction[20:25] + " " + instruction[25:]
        label = "f7----| rs2-| rs1-| f3| rd--| opcode|\n"
    elif instruction_type == "I-Type":
        instruction = instruction[0:12] + " " + instruction[12:17] + " " + instruction[17:20] + " " + instruction[20:25] + " " + instruction[25:]
        label = "imm--------| rs1-| f3| rd--| opcode|\n"
    elif instruction_type == "S-Type" or instruction_type == "B-Type":
        instruction = instruction[0:7] + " " + instruction[7:12] + " " + instruction[12:17] + " " + instruction[17:20] + " " + instruction[20:25] + " " + instruction[25:]
        label = "imm---| rs2-| rs1-| f3| imm-| opcode|"
    else:
        instruction = instruction[0:20] + " " + instruction[20:25] + " " + instruction[25:]
        label = "imm----------------| rd--| opcode|"

    print(label + instruction + "\n")


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
