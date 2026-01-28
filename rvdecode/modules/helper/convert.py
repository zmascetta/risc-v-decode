REGISTER_REFERENCE = {"0": {"alias": "zero", "use": "read-only (0)"},
                      "1": {"alias": "ra", "use": "return address"},
                      "2": {"alias": "sp", "use": "stack pointer"},
                      "3": {"alias": "gp", "use": "global pointer"},
                      "4": {"alias": "tp", "use": "thread pointer"},
                      "5": {"alias": "t0", "use": "temporary"},
                      "6": {"alias": "t1", "use": "temporary"},
                      "7": {"alias": "t2", "use": "temporary"},
                      "8": {"alias": "s0", "use": "saved"},
                      "9": {"alias": "s1", "use": "saved"},
                      "10": {"alias": "a0", "use": "arguments/return values"},
                      "11": {"alias": "a1", "use": "arguments/return values"},
                      "12": {"alias": "a2", "use": "arguments"},
                      "13": {"alias": "a3", "use": "arguments"},
                      "14": {"alias": "a4", "use": "arguments"},
                      "15": {"alias": "a5", "use": "arguments"},
                      "16": {"alias": "a6", "use": "arguments"},
                      "17": {"alias": "a7", "use": "arguments"},
                      "18": {"alias": "s2", "use": "saved"},
                      "19": {"alias": "s3", "use": "saved"},
                      "20": {"alias": "s4", "use": "saved"},
                      "21": {"alias": "s5", "use": "saved"},
                      "22": {"alias": "s6", "use": "saved"},
                      "23": {"alias": "s7", "use": "saved"},
                      "24": {"alias": "s8", "use": "saved"},
                      "25": {"alias": "s9", "use": "saved"},
                      "26": {"alias": "s10", "use": "saved"},
                      "27": {"alias": "s11", "use": "saved"},
                      "28": {"alias": "t3", "use": "temporary"},
                      "29": {"alias": "t4", "use": "temporary"},
                      "30": {"alias": "t5", "use": "temporary"},
                      "31": {"alias": "t6", "use": "temporary"}}

def register_conversion(register_value):
    # convert from bin to dec for lookup
    decimal_value = str(int(register_value, base=2))
    register_data = {"binary_value": register_value,
                        "decimal_value": decimal_value,
                        "name": "x" + decimal_value,
                        "alias": REGISTER_REFERENCE[decimal_value]["alias"],
                        "use": REGISTER_REFERENCE[decimal_value]["use"]
                     }
    return register_data

def twos_complement(immediate, size):
     # get mask with 2^k - 1
     mask = (2 ** size) - 1
     # bitwise xor
     value = mask ^ immediate
     # add 1
     value += 1
     # make value negative
     value = -value

     return value

def unsigned_conversion(immediate):

    immediate_decimal = int(immediate, base=2)
    immediate_data = {"decimal_value": immediate_decimal,
                        "hex_value": hex(immediate_decimal)}
    return immediate_data

def signed_conversion(immediate, size=32):
    # perform twos complement if negative
    if immediate[0:1] == "1":

        immediate = immediate.rjust(32, "1")
        immediate = int(immediate, base=2)
        # get mask with 2^k - 1
        mask = (2 ** size) - 1
        # bitwise xor
        value = mask ^ immediate
        # add 1
        value += 1
        # make value negative
        immediate_decimal = -value
    else:
        immediate_decimal = int(immediate, base=2)

    immediate_data = {"decimal_value": immediate_decimal,
                        "hex_value": hex(immediate_decimal)}
    return immediate_data

def shamt_conversion(shamt):
    shamt_dec = int(shamt, base=2)

    shamt_data = {"binary_value": "shamt",
                    "decimal_value": shamt_dec}

    return shamt_data
