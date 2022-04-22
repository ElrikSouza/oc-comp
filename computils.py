MAX_UNSIGNED_8BIT_INT = 2 ** 8 - 1
MIN_NEGATIVE_8BIT_INT = -1 * 2 ** 7


def eight_bit_int_to_hex_string(number: int) -> str:
    is_number_signed = number < 0
    number_byte = number.to_bytes(
        length=1, byteorder='big', signed=is_number_signed)

    final_hex_representation = number_byte.hex()

    return final_hex_representation


def log_error(error_message: str, line_number=0) -> None:
    print(
        f"\033[1;31;40m ERRO (Linha {line_number}): {error_message} \033[0;0m")


def is_goto_label(raw_input: str) -> bool:
    return raw_input[-1] == ':'


def parse_number_argument(number_arg: str) -> str:
    if number_arg.startswith('0x'):
        hex_number = number_arg[2:]

        if len(hex_number) > 2:
            raise Exception("Argumento so pode ter ate 8 bits")

        if len(hex_number) == 1:
            return '0' + hex_number

        return hex_number

    int_number = int(number_arg)

    if int_number > MAX_UNSIGNED_8BIT_INT or int_number < MIN_NEGATIVE_8BIT_INT:
        raise Exception("Argumento so pode ter ate 8 bits")

    return eight_bit_int_to_hex_string(int_number)


def get_register_address(register_name: str) -> int:

    if len(register_name) != 2 or register_name[0] != 'R':
        raise Exception(f"Nome de registrador invalido {register_name}")

    # ['R', '1'] => 1
    register_address = int(register_name[1])

    if register_address < 0 or register_address > 3:
        raise Exception("Os registradoores do circuito sao numerados de 0 a 3")

    return register_address


def register_parameters_to_hex_number(register_a_index: int, register_b_index: int) -> str:
    hex_register_address = (register_a_index << 2) + register_b_index

    # remove the leading zero
    return eight_bit_int_to_hex_string(hex_register_address)[1:]
