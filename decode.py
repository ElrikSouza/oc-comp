from instruction import Instruction, instruction_hex_prefix_dict
from computils import *


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
