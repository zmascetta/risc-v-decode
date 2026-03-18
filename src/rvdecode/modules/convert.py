REGISTER_REFERENCE = {"0": {"alias": "zero", "use": "read-only (0)"},
                      "1": {"alias": "ra", "use": "return address"},
                      "2": {"alias": "sp", "use": "stack pointer"},
                      "3": {"alias": "gp", "use": "global pointer"},
                      "4": {"alias": "tp", "use": "thread pointer"},
                      "5": {"alias": "t0", "use": "temporary"},
                      "6": {"alias": "t1", "use": "temporary"},
                      "7": {"alias": "t2", "use": "temporary"},
                      "8": {"alias": "fp", "use": "saved, frame pointer"},
                      "9": {"alias": "s1", "use": "saved register"},
                      "10": {"alias": "a0", "use": "function argument/return "},
                      "11": {"alias": "a1", "use": "function argument/return value"},
                      "12": {"alias": "a2", "use": "function argument"},
                      "13": {"alias": "a3", "use": "function argument"},
                      "14": {"alias": "a4", "use": "function argument"},
                      "15": {"alias": "a5", "use": "function argument"},
                      "16": {"alias": "a6", "use": "function argument"},
                      "17": {"alias": "a7", "use": "function argument"},
                      "18": {"alias": "s2", "use": "saved register"},
                      "19": {"alias": "s3", "use": "saved register"},
                      "20": {"alias": "s4", "use": "saved register"},
                      "21": {"alias": "s5", "use": "saved register"},
                      "22": {"alias": "s6", "use": "saved register"},
                      "23": {"alias": "s7", "use": "saved register"},
                      "24": {"alias": "s8", "use": "saved register"},
                      "25": {"alias": "s9", "use": "saved register"},
                      "26": {"alias": "s10", "use": "saved register"},
                      "27": {"alias": "s11", "use": "saved register"},
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

def twos_complement(value, size):
     # get mask with 2^k - 1
     mask = (2 ** size) - 1
     # bitwise xor
     value = mask ^ value
     # add 1
     value += 1
     # make value negative
     value = -value

     return value

def unsigned_conversion(value):
    value_decimal = int(value, base=2)
    value_data = {"decimal": value_decimal,
                        "hex": hex(value_decimal)}
    return value_data

def signed_conversion(value, size=32):
    # perform twos complement if negative
    if value[0:1] == "1":

        value = value.rjust(32, "1")
        value = int(value, base=2)
        # get mask with 2^k - 1
        mask = (2 ** size) - 1
        # bitwise xor
        value = mask ^ value
        # add 1
        value += 1
        # make value negative
        value_decimal = -value
    else:
        value_decimal = int(value, base=2)

    value_data = {"decimal": value_decimal,
                        "hex": hex(value_decimal)}
    return value_data
