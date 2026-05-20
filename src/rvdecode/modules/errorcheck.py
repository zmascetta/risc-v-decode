import re, typer

# check to ensure that either a 32-bit bin instr or 6-bit hex instr has been entered
# will return binary instruction.
def instruction_check(instruction):
    # clear any spaces if passed in with quotes/remove 0x is present
    instruction = instruction.replace(' ', '').replace('0x','')

    # check for 32-bit binary instruction
    binary_check = re.search(
        r"^[0,1]{32}$",
        instruction)

    # check for 6-bit hex instruction
    hex_check = re.search(
        r"^[0-9a-fA-F]{1,8}$",
        instruction)

    # return binary instruction or end program if both checks have failed
    if binary_check is not None:
        return instruction
    elif hex_check is not None:
        instruction = int(instruction, base=16)
        instruction = str(bin(instruction))[2:].zfill(32)
        return instruction
    else:
        print("You did not enter a valid 32-bit binary instruction or a valid hex instructon.")
        raise typer.Exit(code=1)