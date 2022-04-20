from operator import le


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

MAX_UNSIGNED_8BIT_INT = 2 ** 8 - 1
MIN_NEGATIVE_8BIT_INT = -1 * 2 ** 7


def eight_bit_int_to_hex_string(number: int) -> str:
    is_number_signed = number < 0
    number_byte = number.to_bytes(
        length=1, byteorder='big', signed=is_number_signed)

    final_hex_representation = number_byte.hex()

    return final_hex_representation


class Instruction:
    def __init__(self, instruction_name: str, args: str) -> None:
        self.instruction_name = instruction_name
        self.args = args


def log_error(error_message: str, line_of_the_error: int = 0) -> None:
    print(f"ERRO (linha {line_of_the_error}): {error_message}")


def to_hex_number_string(number: int):
    hex_number_string = hex(number)

    trimmed_hex_number_string = ''

    if hex_number_string[0] == '-':
        # -0x1 => 1
        trimmed_hex_number_string = hex_number_string[3:]

    else:
        # 0x1 => 1
        trimmed_hex_number_string = hex_number_string[2:]

    return trimmed_hex_number_string.zfill(2)


def binary_str_to_hex_str(binary_number: str) -> str:
    return hex(int(binary_number), 2)


def register_parameters_to_hex_number(register_a_index: int, register_b_index: int) -> str:
    hex_register_address = (register_a_index << 2) + register_b_index
    return eight_bit_int_to_hex_string(hex_register_address)


def decode_IO_instruction():
    return


def parse_instruction(raw_instruction_input: str) -> Instruction:
    split_instruction = raw_instruction_input.split(" ")

    if len(split_instruction) != 2:
        log_error("Instrução deve ter um nome e uma lista de argumentos")
        raise "error"

    [instruction_name, args] = split_instruction

    return Instruction(instruction_name, args)


def get_register_address(register_name: str) -> int:

    if len(register_name) != 2 or register_name[0] != 'R':
        log_error(f"Nome de registrador invalido {register_name}")
        raise "error"

    # ['R', '1'] => 1
    register_address = int(register_name[1])

    if register_address < 0 or register_address > 3:
        log_error("Os registradoores do circuito sao numerados de 0 a 3")
        raise "error"

    return register_address


def parse_number_argument(number_arg: str) -> str:
    if number_arg.startswith('0x'):
        hex_number = number_arg[2:]

        if len(hex_number) > 2:
            log_error("Argumento so pode ter ate 8 bits")
            raise "error"

        if len(hex_number) == 1:
            return '0' + hex_number

        return hex_number

    int_number = int(number_arg)

    if int_number > MAX_UNSIGNED_8BIT_INT or int_number < MIN_NEGATIVE_8BIT_INT:
        log_error("Argumento so pode ter ate 8 bits")
        raise "error"

    return eight_bit_int_to_hex_string(int_number)


def decode_two_register_instruction(instruction: Instruction):
    instruction_hex_prefix = instruction_hex_prefix_dict[instruction.instruction_name]
    register_names = instruction.args.split(',')

    if len(register_names) != 2:
        log_error("o comando aceita exatamente 2 registradores como argumento")
        raise "error"

    [register_a, register_b] = register_names
    register_a_address = get_register_address(register_a)
    register_b_address = get_register_address(register_b)
    hex_params_suffix = register_parameters_to_hex_number(
        register_a_address, register_b_address)

    complete_instruction = instruction_hex_prefix + hex_params_suffix

    return [complete_instruction]


def decode_IO_instruction(instruction: Instruction):
    return


def decode_conditional_jump_instruction(instruction: Instruction):
    return


def decode_uncoditional_jump_instruction(instruction: Instruction):
    return ["40", instruction.args]


def decode_data_instruction(instruction: Instruction):
    instruction_name_hex_prefix = instruction_hex_prefix_dict["DATA"]
    split_data_args = instruction.args.split(',')

    if len(split_data_args) != 2:
        log_error("o comando requer exatamente dois parametros")
        raise "error"

    [register_name, number_arg] = split_data_args

    register_address = get_register_address(register_name)
    hex_number_arg = parse_number_argument(number_arg)

    instruction_hex = instruction_name_hex_prefix + str(register_address)

    return [instruction_hex, hex_number_arg]


def decode_instruction(instruction: Instruction) -> list[str]:
    if instruction.instruction_name == 'DATA':
        return decode_data_instruction(instruction)

    if instruction.instruction_name == 'CLF':
        return instruction_hex_prefix_dict['CLF'] + '0'

    if instruction.instruction_name in ['OUT', 'IN']:
        return decode_IO_instruction(instruction)

    if instruction.instruction_name.startswith("JMP"):
        if instruction.instruction_name != "JMP":
            return decode_conditional_jump_instruction(instruction)

        return decode_uncoditional_jump_instruction(instruction)

    return decode_two_register_instruction(instruction)


def is_goto_label(raw_input: str) -> bool:
    return raw_input[-1] == ':'


def compile(file: list[str]):
    instruction_array: list[str] = list()
    label_memory_addr_dictionary:  dict[str, int] = dict()

    for line in file:
        trimmed_line = line.strip()

        if is_goto_label(trimmed_line):
            print(f"{trimmed_line} label")
            label_memory_addr_dictionary[trimmed_line[:-1]
                                         ] = len(instruction_array)
        else:
            inst = decode_instruction(parse_instruction(trimmed_line))
            instruction_array.extend(inst)
            print(inst)

    for i in range(len(instruction_array)):
        if instruction_array[i] in label_memory_addr_dictionary.keys():
            instruction_array[i] = eight_bit_int_to_hex_string(
                label_memory_addr_dictionary[instruction_array[i]])

    print(label_memory_addr_dictionary)
    print(instruction_array)
