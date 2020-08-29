from pprint import pprint
from lib.utils import print_div
from lib.utils import print_green
from lib.utils import print_red
from lib.utils import print_yellow
from lib.assembler import Assembler
from lib.loader import Loader


class SimuladorMVN:
    STATES = ["on", "off"]
    STATUS = "status"
    EXIT = "exit"
    ON = "on"
    OFF = "off"
    BOOT = "boot"
    RUN = "run"
    STOP = "stop"
    CLEAR = "clear"
    MEM_SIZE = 4_000
    MNE_TABLE = "mnemonics"
    ASSEMBLER_STATUS = "assembler"
    LOADER_STATUS = "loader"
    HELP = "help"
    state = "off"
    mnemonicos_table = None
    program_name = ""
    program_lines = []
    mem = {}
    run_auto = False
    assembler = None
    loader = None

    def __init__(self, mnemonicos_table):
        self.mnemonicos_table = mnemonicos_table
        self.assembler = Assembler(mnemonicos_table)
        self.loader = Loader(mnemonicos_table)

    def print_program(self):
        line_number = 1
        for line in self.program_lines:
            print(f"line {line_number}. {line}", end="")
            line_number = line_number + 1
        print()

    def load_program(self, program_filepath):
        print(f"loading program {program_filepath}...")
        with open(program_filepath) as program_file:
            self.program_name = program_filepath
            self.program_lines = program_file.readlines()
            self.assembler.load_program_lines(self.program_lines)
            self.assembler.treat_program_lines()
            self.assembler.process_fase_1()
            self.assembler.process_fase_2()
            self.loader.object_code = self.assembler.object_code
            self.loader.load_program()
            self.state = "program_loaded"
            program_file.close()
        print_div()

    def simulator_is_off(self):
        print_red("Simulador MVN off")
        print(f"to turn on: {self.ON}")
        print(f"to exit:    {self.EXIT}")
        print(f"to help:    {self.HELP}")
        print_div()

    def simulator_is_on(self):
        print_green("Simulador MVN on")
        print(f"to print internal status:       {self.STATUS}")
        print(f"to print table of mnemonics:    {self.MNE_TABLE}")
        print(f"to print assembler status:      {self.ASSEMBLER_STATUS}")
        print(f"to print loader status:         {self.LOADER_STATUS}")
        print(f"to load a program:              {self.BOOT}")
        print(f"to run the program in memory:   {self.RUN}")
        print(f"to clear:                       {self.CLEAR}")
        print(f"to help:                        {self.HELP}")
        print(f"to turn off:                    {self.OFF}")
        print_div()

    def cmd_run(self):
        if self.state == "program_loaded":
            self.loader.run()
        else:
            print_red(f"no program in memory")
            print_red(f"to load a program, enter '{self.BOOT}'")
            return

    def cmd_help(self):
        if self.state == "off":
            self.simulator_is_off()
        else:
            self.simulator_is_on()

    def cmd_on(self):
        if self.state == "off":
            self.state = "on"
            self.simulator_is_on()

    def cmd_off(self):
        if self.state != "off":
            self.state = "off"
            self.simulator_is_off()

    def cmd_boot(self):
        program_filename = input("enter program path: ")
        try:
            program_filepath = program_filename
            self.load_program(program_filepath)
        except OSError as e:
            print_red(f"error while opening the file: {e}")
            return

    def cmd_clear(self):
        self.assembler.clear_all()
        self.loader.clear_all()
        self.mem = {}
        self.program_name = ""
        self.program_lines = []
        self.process_end = False

    def cmd_mne_table(self):
        print_green("Table of mnemonics")
        pprint(self.mnemonicos_table)
        print_div()

    def cmd_assembler_status(self):
        self.assembler.print_status()
        print_div()

    def cmd_loader_status(self):
        self.loader.print_status()
        print_div()

    def cmd_status(self):
        print_green("Simulator status")
        print_yellow(f"state:        {self.state}")
        print_yellow(f"program name: {self.program_name}")
        print_yellow(f"program:")
        if self.program_name == "":
            pass
        else:
            self.print_program()
        print_yellow("memory:")
        pprint(self.mem)
        print_div()

    def cmd_invalid(self):
        print_red("invalid command")

    def start(self):
        self.simulator_is_off()
        while True:
            if self.state == "off":
                input_cmd = input(": ")
                if input_cmd == self.EXIT:
                    break
                elif input_cmd == self.ON:
                    self.cmd_on()
                    continue
                elif input_cmd == self.HELP:
                    self.cmd_help()
                    continue
                else:
                    self.cmd_invalid()
                    continue
            else:
                input_cmd = input(": ")
                if input_cmd == self.HELP:
                    self.cmd_help()
                    continue
                elif input_cmd == self.MNE_TABLE:
                    self.cmd_mne_table()
                    continue
                elif input_cmd == self.ASSEMBLER_STATUS:
                    self.cmd_assembler_status()
                    continue
                elif input_cmd == self.LOADER_STATUS:
                    self.cmd_loader_status()
                    continue
                elif input_cmd == self.BOOT:
                    self.cmd_boot()
                    continue
                elif input_cmd == self.OFF:
                    self.cmd_off()
                    continue
                elif input_cmd == self.CLEAR:
                    self.cmd_clear()
                    continue
                elif input_cmd == self.STATUS:
                    self.cmd_status()
                    continue
                elif input_cmd == self.RUN:
                    self.cmd_run()
                    continue
                else:
                    self.cmd_invalid()
                    continue
