from instruction import Instruction, instruction_hex_prefix_dict
from computils import *


def _decode_two_register_instruction(instruction: Instruction):
    instruction_hex_prefix = instruction_hex_prefix_dict[instruction.name]

    if len(instruction.args) != 2:
        raise Exception(
            f"O comando {instruction.name} aceita exatamente 2 registradores como argumento")

    [register_a, register_b] = instruction.args
    register_a_address = get_register_address(register_a)
    register_b_address = get_register_address(register_b)

    hex_params_suffix = register_parameters_to_hex_number(
        register_a_address, register_b_address)

    complete_instruction = instruction_hex_prefix + hex_params_suffix

    return [complete_instruction]


def _decode_IO_instruction(instruction: Instruction):
    instruction_name_prefix = instruction_hex_prefix_dict[instruction.name]

    io_argument_value = 0

    if instruction.name == 'OUT':
        io_argument_value += 8

    if len(instruction.args) != 2:
        raise Exception("Comando I/O precisa de exatamente 2 argumentos")

    [addr_or_data, register_name] = instruction.args

    if addr_or_data == 'Addr':
        io_argument_value += 4

    io_argument_value += get_register_address(register_name)

    # remove leading '0'
    io_argument_hex_suffix = eight_bit_int_to_hex_string(io_argument_value)[1:]

    final_io_instruction = instruction_name_prefix + io_argument_hex_suffix

    return [final_io_instruction]


def _decode_conditional_jump_instruction(instruction: Instruction):
    instruction_name_preffix = '5'
    flags = instruction.name[1:]
    flag_parameters = set(flags.split())

    argument_value = 0

    if 'C' in flag_parameters:
        argument_value += 8

    if 'A' in flag_parameters:
        argument_value += 4

    if 'E' in flag_parameters:
        argument_value += 2

    if 'Z' in flag_parameters:
        argument_value += 1

    # remove leading '0'
    instruction_args_suffix = eight_bit_int_to_hex_string(argument_value)[1:]

    complete_instruction = [instruction_name_preffix + instruction_args_suffix]
    label_or_address = instruction.args[0]

    return [complete_instruction, label_or_address]


def _decode_uncoditional_jump_instruction(instruction: Instruction):
    instruction_name_hex_prefix = instruction_hex_prefix_dict[instruction.name]

    if instruction.name == 'JMP':
        label_or_address = instruction.args[0]
        return [instruction_name_hex_prefix + '0', label_or_address]

    # Decode jump to register addr
    register_name = instruction.args[0]
    instruction_args_suffix = str(get_register_address(register_name))

    return [instruction_name_hex_prefix + instruction_args_suffix]


def _decode_data_instruction(instruction: Instruction):
    instruction_name_hex_prefix = instruction_hex_prefix_dict["DATA"]

    if len(instruction.args) != 2:
        raise Exception("O comando requer exatamente dois parametros")

    [register_name, number_arg] = instruction.args

    register_address = get_register_address(register_name)
    hex_number_arg = parse_number_argument(number_arg)

    instruction_hex = instruction_name_hex_prefix + str(register_address)

    return [instruction_hex, hex_number_arg]


def decode_instruction(instruction: Instruction) -> list[str]:
    if instruction.name == 'DATA':
        return _decode_data_instruction(instruction)

    elif instruction.name == 'CLF':
        return instruction_hex_prefix_dict['CLF'] + '0'

    elif instruction.name in ['OUT', 'IN']:
        return _decode_IO_instruction(instruction)

    elif instruction.name.startswith("J"):
        if instruction.name not in ["JMP", "JMPR"]:
            return _decode_conditional_jump_instruction(instruction)

        return _decode_uncoditional_jump_instruction(instruction)

    elif instruction.name in instruction_hex_prefix_dict.keys():
        return _decode_two_register_instruction(instruction)

    else:
        raise Exception(
            f"Instrução desconhecida: '{instruction.name}'")
