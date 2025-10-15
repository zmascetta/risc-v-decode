HEADER_VALUES = {"rs1_data": "Source Register 1 (rs1)",
                 "rs2_data": "Source Register 2 (rs2)",
                 "rd_data": "Destination Register (rd)",
                 "immediate_data": "Immediate",
                 "general_data": "General Information"}


def format_label(label):
    label = label.replace("_"," ")
    label = label.title()
    return label


def print_instruction(instruction):
    print("INSTRUCTION")
    print(instruction+ "\n")


def print_data(data):
    for label, value in data.items():
        value = str(value)
        print(format_label(label) + ": " + value)
    print()


def print_data_header(data):
    print(HEADER_VALUES[data])


def output_instruction(decoded_instruction):

    instruction_value = decoded_instruction.pop("instruction")
    print_instruction(instruction_value["value"])

    for data in decoded_instruction:
        print_data_header(data)
        print_data(decoded_instruction[data])