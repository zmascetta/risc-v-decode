import sys, re


# check to make sure only 1 arg has been entered
def argument_check(arguments):
    if len(arguments) != 2:
        system_exit()


# check to ensure that either a 32-bit bin instr or 8-bit hex instr has been entered
# will return binary instruction.
def instruction_check(instruction):
    # clear any spaces if passed in with quotes
    instruction = instruction.replace(' ', '')

    if instruction[0:2] == "0x":
        instruction = instruction[2:]

    # check for 32-bit binary instruction
    binary_check = re.search(
        r"^[0,1]{32}$",
        instruction)

    # check for 8-bit hex instruction
    hex_check = re.search(
        r"^[0-9a-fA-F]{8}$",
        instruction)

    # return binary instruction or end program if both checks have failed
    if binary_check is not None:
        return instruction
    elif hex_check is not None:
        instruction = int(instruction, base=16)
        instruction = str(bin(instruction))[2:].zfill(32)
        return instruction
    else:
        system_exit()

# function for exiting system
# accepts additional lines if necessary
def system_exit(extra_lines=None):
    error_message = "Usage:\n" \
                    "\t\033[1mrvdecode\033[0m instruction\n" \
                    "\tInstruction must be a valid 32-bit binary or 8-bit hex instruction."
    if extra_lines is not None:
        error_message += "\n\n\t" + extra_lines
    sys.exit(error_message)