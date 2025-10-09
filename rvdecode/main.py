import sys, helper.errorcheck, helper.decode, helper.output


# error check
#   arguments - done
#   valid instr. - done
#
# instr. decode
# overall type - use opcode store type r, i, s, b, u, j
# specific type - use func, store specific, add, addi, etc.
# immediate decode - store, convert to hex and dec
# registers decode - store, convert to ABI
# make assembly line
#
# output

def main():

    # Check for usage errors.
    arguments = sys.argv
    helper.errorcheck.argument_check(arguments)

    # Check a valid instruction has been entered.
    # Returns binary instruction (if hex instruction entered, it will be converted).
    instruction = helper.errorcheck.instruction_check(arguments[1])

    # Decode instruction
    helper.decode.decode(instruction)

if __name__ == "__main__":
    main()