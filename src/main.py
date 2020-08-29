from lib.utils import load_instructions_table
from lib.simulator import SimuladorMVN


def main():
    mnemonics_table = load_instructions_table("../config/instructions.csv")
    simulator = SimuladorMVN(mnemonics_table)
    simulator.start()


if __name__ == "__main__":
    main()
