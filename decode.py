from instruction import Instruction, instruction_hex_prefix_dict
from computils import *


def _decode_two_register_instruction(instruction: Instruction):
    instruction_hex_prefix = instruction_hex_prefix_dict[instruction.instruction_name]
    register_names = instruction.args.split(',')

    if len(register_names) != 2:
        raise Exception(
            "O comando aceita exatamente 2 registradores como argumento")

    [register_a, register_b] = register_names
    register_a_address = get_register_address(register_a)
    register_b_address = get_register_address(register_b)
    hex_params_suffix = register_parameters_to_hex_number(
        register_a_address, register_b_address)

    complete_instruction = instruction_hex_prefix + hex_params_suffix

    return [complete_instruction]


def _decode_IO_instruction(instruction: Instruction):
    instruction_name_prefix = instruction_hex_prefix_dict[instruction.instruction_name]

    io_argument_value = 0

    if instruction.instruction_name == 'OUT':
        io_argument_value += 8

    split_arguments = instruction.args.split(',')

    if len(split_arguments) != 2:
        raise Exception("Comando I/O precisa de exatamente 2 argumentos")

    [addr_or_data, register_name] = split_arguments

    if addr_or_data == 'Addr':
        io_argument_value += 4

    io_argument_value += get_register_address(register_name)

    io_argument_hex_suffix = eight_bit_int_to_hex_string(io_argument_value)

    final_io_instruction = instruction_name_prefix + io_argument_hex_suffix

    return [final_io_instruction]


def _decode_conditional_jump_instruction(instruction: Instruction):
    instruction_name_preffix = '5'
    flags = instruction.instruction_name[1:]
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

    instruction_args_suffix = eight_bit_int_to_hex_string(argument_value)

    complete_instruction = [instruction_name_preffix + instruction_args_suffix]

    return [complete_instruction, instruction.args]


def _decode_uncoditional_jump_instruction(instruction: Instruction):
    instruction_name_hex_prefix = instruction_hex_prefix_dict[instruction.instruction_name]

    if instruction.instruction_name == 'JMP':
        # 40, (label || address)
        return [instruction_name_hex_prefix + '0', instruction.args]

    instruction_args_suffix = str(get_register_address(instruction.args))

    return [instruction_name_hex_prefix + instruction_args_suffix]


def _decode_data_instruction(instruction: Instruction):
    instruction_name_hex_prefix = instruction_hex_prefix_dict["DATA"]
    split_data_args = instruction.args.split(',')

    if len(split_data_args) != 2:
        raise Exception("O comando requer exatamente dois parametros")

    [register_name, number_arg] = split_data_args

    register_address = get_register_address(register_name)
    hex_number_arg = parse_number_argument(number_arg)

    instruction_hex = instruction_name_hex_prefix + str(register_address)

    return [instruction_hex, hex_number_arg]


def decode_instruction(instruction: Instruction) -> list[str]:
    if instruction.instruction_name == 'DATA':
        return _decode_data_instruction(instruction)

    elif instruction.instruction_name == 'CLF':
        return instruction_hex_prefix_dict['CLF'] + '0'

    elif instruction.instruction_name in ['OUT', 'IN']:
        return _decode_IO_instruction(instruction)

    elif instruction.instruction_name.startswith("J"):
        if instruction.instruction_name not in ["JMP", "JMPR"]:
            return _decode_conditional_jump_instruction(instruction)

        return _decode_uncoditional_jump_instruction(instruction)

    elif instruction.instruction_name in instruction_hex_prefix_dict.keys():
        return _decode_two_register_instruction(instruction)

    else:
        raise Exception(
            f"Instrução desconhecida: '{instruction.instruction_name}'")
