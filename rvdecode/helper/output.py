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

    # instruction and assembly are both single strings (as opposed to dicts.)
    # they should not follow the print loop for the other data and should be popped
    # the decoded instruction dict.
    # pop instruction and print it, then pop assembly value to print after loop
    instruction_value = decoded_instruction.pop("instruction")
    print_instruction(instruction_value)

    assembly_value = decoded_instruction.pop("assembly")

    for data in decoded_instruction:
        print_data_header(data)
        print_data(decoded_instruction[data])

    # print assembly code
    print_data_header("assembly")
    print(assembly_value)
