instruction_hex_prefix_dict: dict[str, str] = {
    "LOAD": "0",
    "STORE": "1",
    "DATA": "2",
    "JMPR": "3",
    "JMP": "4",
    "CLF": "6",
    "OUT": "7",
    "IN": "7",
    "ADD": "8",
    "SHR": "9",
    "SHL": "A",
    "NOT": "B",
    "AND": "C",
    "OR": "D",
    "XOR": "E",
    "COMP": "F"
}


class Instruction:
    def __init__(self, instruction_name: str, args: list[str]) -> None:
        self.name = instruction_name
        self.args = args


def parse_instruction(raw_instruction_input: str) -> Instruction:
    split_instruction = raw_instruction_input.split(" ")

    if len(split_instruction) != 2:
        raise Exception("Instrução deve ter um nome e uma lista de argumentos")

    [instruction_name, args] = split_instruction
    arg_list = args.split(',')

    return Instruction(instruction_name, arg_list)
