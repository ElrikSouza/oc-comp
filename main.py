from codebuilder import CodeBuilder
from sys import argv


def compile_file(filename: str) -> list[str]:
    code_builder = CodeBuilder()

    with open(filename, 'r') as file_input:
        for line in file_input:
            code_builder.process_line_of_code(line)

    instructions = code_builder.build_list_of_instructions()
    return instructions


def create_ram_image(instructions: list[str], output_filename: str) -> None:
    with open(output_filename, 'w') as output_file:
        output_file.write()
