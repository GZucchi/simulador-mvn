from pprint import pprint
from lib.utils import print_green
from lib.utils import print_red
from lib.utils import print_yellow
from lib.utils import ascii_table
from lib.utils import int2_3hex


class Assembler:
    state = "parado"
    mnemonics_table = {}
    symbols_table = {}
    constants_table = {}
    crossref_table = {}
    program_lines = []
    program_lines_detailed = {}
    object_code = {}
    mem = {}
    ic = 0
    nb_org = 0

    def __init__(self, mnemonics_table):
        self.mnemonics_table = mnemonics_table
        return

    def clear_all(self):
        self.symbols_table = {}
        self.program_lines_detailed = {}
        self.object_code = {}
        self.mem = {}
        self.ic = 0

    def load_program_lines(self, program_lines):
        self.clear_all()
        self.program_lines = program_lines

    def print_status(self):
        print_green("Assembler status")
        # print_yellow("table of mnemonics")
        # pprint(self.mnemonics_table)
        # print_yellow("program lines detailed:")
        # pprint(self.program_lines_detailed)
        print_yellow("table of symbols:")
        pprint(self.symbols_table)
        # print_yellow("table of constants:")
        # pprint(self.constants_table)
        # print_yellow("table of cross references:")
        # pprint(self.crossref_table)
        print_yellow("memory:")
        pprint(self.mem)
        print_yellow("object code:")
        pprint(self.object_code)

    def treat_program_lines(self):
        print_yellow("assembler: treating program lines ...")
        i = 1
        for line in self.program_lines:
            # print(f"line {i} ...")
            label = ""
            mnemonic = ""
            operand = ""
            comment = ""

            # verify if line has comment
            label_code_comment = line.split(";", 1)
            len_code_comment = len(label_code_comment)
            label_code = label_code_comment[0]
            if len_code_comment == 2:
                comment = label_code_comment[1]

            # verify if line has label
            label_code_list = label_code.split(":")
            len_label_code_list = len(label_code_list)
            if len_label_code_list == 1:
                code = label_code_list[0]
            elif len_label_code_list == 2:
                label = label_code_list[0]
                code = label_code_list[1]
            else:
                print_red(f"{i}. {line}")
                raise BaseException("incompatible label")

            # get components (label, mnemonic, operand) of the code line
            code_list = code.split()
            len_code_list = len(code_list)
            if len_code_list == 0:
                pass
            elif len_code_list == 1:
                mnemonic = code_list[0]
            elif len_code_list == 2:
                mnemonic = code_list[0]
                operand = code_list[1]
            else:
                print_red(f"line {i}. {line}")
                raise BaseException("incompatible code")

            ignore = False
            if (label == "") and (mnemonic == "") and (operand == ""):
                ignore = True

            self.program_lines_detailed[i] = {}
            self.program_lines_detailed[i]["ignore"] = ignore
            self.program_lines_detailed[i]["label"] = label
            self.program_lines_detailed[i]["mnemonic"] = mnemonic
            self.program_lines_detailed[i]["operand"] = operand
            self.program_lines_detailed[i]["comment"] = comment
            i += 1

    def treat_label(self, label, line_nb):
        if label != "":
            if label in self.symbols_table.keys():
                if self.symbols_table[label]["defined"]:
                    raise BaseException("label multiple definition")
                else:
                    self.symbols_table[label]["address"] = self.ic
                    self.symbols_table[label]["defined"] = True
            else:
                self.symbols_table[label] = {}
                self.symbols_table[label]["address"] = self.ic
                self.symbols_table[label]["defined"] = True

    def process_fase_1(self):
        print_yellow("assembler: fase 1 ...")
        self.state = "fase1"
        for line_nb, line in self.program_lines_detailed.items():
            # print(f"line {line_nb}. {line}")
            if line["ignore"]:
                continue

            self.treat_label(line["label"], line_nb)

            # treat mnemonic
            mnemonic = line["mnemonic"]
            if mnemonic == "":
                continue
            if mnemonic not in self.mnemonics_table.keys():
                raise BaseException("invalid mnemonic")

            # treat operand
            operand = line["operand"]
            operand_is_symbol = operand.isalpha()
            if operand_is_symbol and operand not in self.symbols_table.keys():
                self.symbols_table[operand] = {}
                self.symbols_table[operand]["defined"] = False

            ic_hex = int2_3hex(self.ic)
            ic_p_1_hex = int2_3hex(self.ic + 1)

            # is a pseudo instruction ?
            if self.mnemonics_table[mnemonic]["class"] == "pseudo":
                if mnemonic == "ORG":
                    self.ic = int(operand, 16)
                    continue
                elif mnemonic == "DATA":
                    self.mem[ic_hex] = {}
                    self.mem[ic_hex] = "??"
                    self.ic += 1
                    continue
                elif mnemonic == "BLOC":
                    self.ic += int(operand, 16)
                    continue
                elif mnemonic == "END":
                    self.state = "fase2"
                    break
                else:
                    raise BaseException("undefined pseudo instruction")
            elif self.mnemonics_table[mnemonic]["class"] == "instruction":
                self.mem[ic_hex] = {}
                self.mem[ic_hex] = self.mnemonics_table[mnemonic]["opcode"] + "?"
                if self.mnemonics_table[mnemonic]["size"] == 2:
                    self.mem[ic_p_1_hex] = {}
                    self.mem[ic_p_1_hex] = "??"
                self.ic += self.mnemonics_table[mnemonic]["size"]
            else:
                raise BaseException("undefined mnemonic class")

    def process_fase_2(self):
        print_yellow("assembler: fase 2 ...")
        self.nb_org = 0
        if self.state == "fase2":
            for line_nb, line in self.program_lines_detailed.items():
                # print(f"line {line_nb}. {line}")
                if line["ignore"]:
                    continue
                ic_hex = int2_3hex(self.ic)
                ic_p_1_hex = int2_3hex(self.ic + 1)

                # treat mnemonic
                mnemonic = line["mnemonic"]
                if mnemonic == "":
                    continue
                if mnemonic not in self.mnemonics_table.keys():
                    raise BaseException("invalid mnemonic")

                # treat operand
                operand = line["operand"]
                if "0x" in operand:  # operand is an absolute address in hexadecimal notation
                    operand = operand.replace("0x", "")

                # treat mnemonic
                if self.mnemonics_table[mnemonic]["class"] == "pseudo":
                    if mnemonic == "ORG":
                        self.ic = int(operand, 16)
                        ic_hex = int2_3hex(self.ic)
                        if self.nb_org == 0:
                            self.nb_org = 1
                        else:
                            self.nb_org += 1
                        self.object_code[self.nb_org] = ["0" + ic_hex[0], ic_hex[1:]]
                        continue
                    elif mnemonic == "DATA":
                        if len(operand) == 3 and operand[0] == '"' and operand[2] == '"' and operand[1].isalpha():
                            operand = ascii_table[operand[1]]
                        if len(operand) == 1:
                            operand = "0" + operand
                        self.mem[ic_hex] = operand
                        self.object_code[self.nb_org].append(operand)
                        self.ic += 1
                        continue
                    elif mnemonic == "BLOC":
                        self.ic += int(operand, 16)
                        continue
                    elif mnemonic == "END":
                        self.state = "fase2-completed"
                        break
                    else:
                        raise BaseException("undefined pseudo instruction")
                elif self.mnemonics_table[mnemonic]["class"] == "instruction":
                    if "+" in operand:  # treat operand expression
                        operand_split = operand.split("+")
                        operand_values = []
                        for x in operand_split:
                            if x in self.symbols_table.keys():
                                symbol = x
                                symbol_address = self.symbols_table[symbol]["address"]
                                operand_values.append(symbol_address)
                            elif x.isnumeric():
                                operand_values.append(int(x))
                            else:
                                raise BaseException("invalid operand")
                        operand = sum(operand_values)
                        operand = int2_3hex(operand)
                    elif operand in self.symbols_table.keys():  # operand is a symbol
                        symbol = operand
                        operand = self.symbols_table[symbol]["address"]
                        operand = int2_3hex(operand)
                    else:
                        print_red("TODO")
                    byte = self.mem[ic_hex].replace("?", operand[0])
                    self.mem[ic_hex] = byte
                    self.object_code[self.nb_org].append(byte)
                    if self.mnemonics_table[mnemonic]["size"] == 2:
                        byte = operand[1:]
                        self.mem[ic_p_1_hex] = byte
                        self.object_code[self.nb_org].append(byte)
                    self.ic += self.mnemonics_table[mnemonic]["size"]
                else:
                    raise BaseException("undefined mnemonic class")
        else:
            raise BaseException("cannot build object code")
