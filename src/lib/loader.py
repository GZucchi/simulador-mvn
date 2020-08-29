from pprint import pprint
from lib.utils import print_green
from lib.utils import print_red
from lib.utils import print_yellow
from lib.utils import print_div
from lib.utils import int2_2hex
from lib.utils import add_hex_address


class Loader:
    ac = 0
    ic = 0
    mnemonicos_table = None
    mem = {}
    object_code = {}

    def __init__(self, mnemonicos_table):
        self.mnemonicos_table = mnemonicos_table

    def clear_all(self):
        self.ac = 0
        self.ic = 0
        self.mem = {}

    def print_status(self):
        print_green("Loader status")
        print_yellow("memory:")
        pprint(self.mem)
        print_yellow("object_code:")
        pprint(self.object_code)

    def process_JUMP(self):
        """ jump inconditional """
        operand = self.mem[self.ic][1] + self.mem[add_hex_address(self.ic, 1)]
        self.ic = operand

    def process_JUMPZ(self):
        """ jump if zero """
        operand = self.mem[self.ic][1] + self.mem[add_hex_address(self.ic, 1)]
        if self.ac == "00":
            self.ic = operand
        else:
            self.ic = add_hex_address(self.ic, self.mnemonicos_table["JUMPZ"]["size"])

    def process_JUMPN(self):
        """ jump if negative """
        operand = self.mem[self.ic][1] + self.mem[add_hex_address(self.ic, 1)]
        if int(self.ac) < 0:
            self.ic = operand
        else:
            self.ic = add_hex_address(self.ic, self.mnemonicos_table["JUMPN"]["size"])

    def process_ADD(self):
        """ add """
        # print_yellow("add")
        operand = self.mem[self.ic][1] + self.mem[add_hex_address(self.ic, 1)]
        aux_int = int(self.mem[operand], 16)
        ac_int = int(self.ac, 16) + aux_int
        self.ac = int2_2hex(ac_int)
        self.ic = add_hex_address(self.ic, self.mnemonicos_table["SUB"]["size"])

    def process_SUB(self):
        """ subtract """
        operand = self.mem[self.ic][1] + self.mem[add_hex_address(self.ic, 1)]
        aux_int = int(self.mem[operand], 16)
        ac_int = int(self.ac, 16) - aux_int
        self.ac = int2_2hex(ac_int)
        self.ic = add_hex_address(self.ic, self.mnemonicos_table["SUB"]["size"])

    def process_MUL(self):
        """ multiply """
        operand = self.mem[self.ic][1] + self.mem[add_hex_address(self.ic, 1)]
        self.ac = self.ac * operand
        self.ic = self.ic + self.mnemonicos_table["MUL"]["size"]

    def process_DIV(self):
        """ divide """
        operand = self.mem[self.ic][1] + self.mem[add_hex_address(self.ic, 1)]
        self.ac = self.ac / operand
        self.ic = self.ic + self.mnemonicos_table["DIV"]["size"]

    def process_LOAD(self):
        """ load from memory """
        operand = self.mem[self.ic][1] + self.mem[add_hex_address(self.ic, 1)]
        self.ac = self.mem[operand]
        self.ic = add_hex_address(self.ic, self.mnemonicos_table["LOAD"]["size"])

    def process_STORE(self):
        """ move to memory """
        operand = self.mem[self.ic][1] + self.mem[add_hex_address(self.ic, 1)]
        if operand not in self.mem.keys():
            self.mem[operand] = {}
        self.mem[operand] = self.ac
        self.ic = add_hex_address(self.ic, self.mnemonicos_table["STORE"]["size"])

    def process_CALL(self):
        """ subroutine call """
        # TODO
        print_red("subroutine call")

    def process_RTN(self):
        """ return from subroutine """
        print_yellow("return from subroutine")

    def process_STOP(self):
        """ stop machine """
        self.program_end = True

    def process_READ(self):
        """ read data """
        operand = self.mem[self.ic][1] + self.mem[add_hex_address(self.ic, 1)]
        self.ac = operand
        self.ic = self.ic + self.mnemonicos_table["READ"]["size"]

    def process_WRITE(self):
        """ write data """
        self.ic = self.ic + self.mnemonicos_table["WRITE"]["size"]

    def process_PD(self):
        """ print acumulator """
        print_green(f"{self.ac}")
        self.ic = add_hex_address(self.ic, self.mnemonicos_table["PD"]["size"])

    def process_instruction(self, opcode):
        if opcode == self.mnemonicos_table["JUMP"]["opcode"]:
            self.process_JUMP()
        elif opcode == self.mnemonicos_table["JUMPZ"]["opcode"]:
            self.process_JUMPZ()
        elif opcode == self.mnemonicos_table["JUMPN"]["opcode"]:
            self.process_JUMPN()
        elif opcode == self.mnemonicos_table["ADD"]["opcode"]:
            self.process_ADD()
        elif opcode == self.mnemonicos_table["SUB"]["opcode"]:
            self.process_SUB()
        elif opcode == self.mnemonicos_table["MUL"]["opcode"]:
            self.process_MUL()
        elif opcode == self.mnemonicos_table["DIV"]["opcode"]:
            self.process_DIV()
        elif opcode == self.mnemonicos_table["LOAD"]["opcode"]:
            self.process_LOAD()
        elif opcode == self.mnemonicos_table["STORE"]["opcode"]:
            self.process_STORE()
        elif opcode == self.mnemonicos_table["CALL"]["opcode"]:
            self.process_CALL()
        elif opcode == self.mnemonicos_table["RTN"]["opcode"]:
            self.process_RTN()
        elif opcode == self.mnemonicos_table["STOP"]["opcode"]:
            self.process_STOP()
        elif opcode == self.mnemonicos_table["READ"]["opcode"]:
            self.process_READ()
        elif opcode == self.mnemonicos_table["WRITE"]["opcode"]:
            self.process_READ()
        elif opcode == self.mnemonicos_table["PD"]["opcode"]:
            self.process_PD()
        else:
            raise BaseException("undefined instruction")

    def load_program(self):
        if len(self.object_code) == 0:
            raise BaseException("undefined object code")
        else:
            for _, fita in self.object_code.items():
                # fita = ["xx", "xx", "xx", ...]
                address = fita[0][1] + fita[1]
                for byte in fita[2:]:
                    self.mem[address] = byte
                    address = add_hex_address(address, 1)

    def run(self):
        self.program_end = False
        self.ic = self.object_code[1][0][1] + self.object_code[1][1]

        while True:
            run_auto_input = input("execute program automatically? (y/n): ")
            if run_auto_input == "y":
                run_auto = True
                break
            elif run_auto_input == "n":
                run_auto = False
                break
            else:
                continue

        print("running the program ... ")
        while True:
            if self.program_end:
                print_green("program was executed successfully")
                break

            opcode = self.mem[self.ic][0]

            if not run_auto:
                input("press any key to execute instruction: ")
                self.process_instruction(opcode)
                print_div()
            else:
                self.process_instruction(opcode)
