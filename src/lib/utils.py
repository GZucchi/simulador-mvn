class Bcolors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"


def print_green(text):
    print(f"{Bcolors.GREEN}{text}{Bcolors.END}")


def print_red(text):
    print(f"{Bcolors.RED}{text}{Bcolors.END}")


def print_yellow(text):
    print(f"{Bcolors.YELLOW}{text}{Bcolors.END}")


def print_div():
    print("------------------------------")


def load_mnemonics_table(mnemonics_filepath):
    mnemonics_file = open(mnemonics_filepath)
    mnemonics_table = {}
    mnemonics_lines = mnemonics_file.readlines()
    for line in mnemonics_lines:
        line_components = line.split(";")
        mnemonic = line_components[0]
        opcode = line_components[1]
        name = line_components[2]
        mnemonics_table[mnemonic] = {}
        mnemonics_table[mnemonic]["opcode"] = opcode
        mnemonics_table[mnemonic]["name"] = name
    mnemonics_file.close()
    return mnemonics_table


def load_instructions_table(instructions_filepath):
    with open(instructions_filepath) as instructions_file:
        instruction_table = {}
        instructions_lines = instructions_file.readlines()
        for line in instructions_lines[1:]:
            [mnemonic, opcode, size, instruction, iclass, optype] = line.split(";")
            instruction_table[mnemonic] = {}
            instruction_table[mnemonic]["opcode"] = opcode
            instruction_table[mnemonic]["size"] = int(size)
            instruction_table[mnemonic]["instruction"] = instruction
            instruction_table[mnemonic]["class"] = iclass.replace("\n", "")
            instruction_table[mnemonic]["optype"] = optype.replace("\n", "")
        instructions_file.close()

    return instruction_table


ascii_table = {
    "a": "41",
    "b": "42",
    "c": "43",
    "d": "44",
    "e": "45",
    "f": "46",
    "g": "47",
    "h": "48",
    "i": "49",
    "j": "4a",
    "k": "4b",
    "l": "4c",
    "m": "4d",
    "n": "4e",
    "o": "4f",
    "p": "51",
    "q": "52",
    "r": "53",
    "s": "54",
    "t": "55",
    "u": "56",
    "v": "56",
    "w": "57",
    "x": "58",
    "y": "59",
    "z": "5a",
}


def int2_2hex(val_int):
    val_hex = hex(val_int).replace("0x", "")
    if len(val_hex) == 1:
        val_hex = "0" + val_hex
    elif len(val_hex) == 2:
        pass
    else:
        raise ("invalid conversion int2_2hex")
    return val_hex


def int2_3hex(val_int):
    val_hex = hex(val_int).replace("0x", "")
    if len(val_hex) == 1:
        val_hex = "00" + val_hex
    elif len(val_hex) == 2:
        val_hex = "0" + val_hex
    elif len(val_hex) == 3:
        pass
    else:
        raise ("invalid conversion int2_3hex")
    return val_hex


def add_hex_address(val_hex, increment):
    val = int(val_hex, 16) + increment
    address = int2_3hex(val)
    return address
