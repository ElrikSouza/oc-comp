from codebuilder import CodeBuilder
from sys import argv

from computils import eight_bit_int_to_hex_string, log_error


def compile_file(filename: str) -> list[str]:
    code_builder = CodeBuilder()

    with open(filename, 'r') as file_input:
        number_of_lines_read = 1

        for line in file_input:
            try:
                code_builder.process_line_of_code(line)
                number_of_lines_read += 1
            except Exception as error:
                log_error(error.args[0], number_of_lines_read)
                quit()

    instructions = code_builder.build_list_of_instructions()
    return instructions


def create_ram_image(instructions: list[str], output_filename: str) -> None:
    with open(output_filename, 'w') as output_file:
        line_first_address = 0
        output_file.write("v3.0 hex words addressed\n")

        for _ in range(16):
            first_address_of_current_line = eight_bit_int_to_hex_string(
                line_first_address)

            output_file.write(f"{first_address_of_current_line}:")

            for j in range(16):
                current_index = j + line_first_address

                if current_index >= len(instructions):
                    output_file.write(' 00')
                else:
                    output_file.write(f" {instructions[current_index]}")

            line_first_address += 16
            output_file.write('\n')


def main():
    input_filename = argv[1]
    output_filename = argv[2]

    print(f'Lendo arquivo: \033[1;34;40m {input_filename}\033[0;0m...')
    hex_instructions = compile_file(input_filename)

    print(f'Salvando no arquivo: \033[1;34;40m {output_filename}\033[0;0m...')
    create_ram_image(hex_instructions, output_filename)

    print(f'\033[1;36;40mProcesso concluído com sucesso\033[0;0m')


main()
