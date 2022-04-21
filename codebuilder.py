from computils import eight_bit_int_to_hex_string, is_goto_label
from instruction import parse_instruction
from decode import decode_instruction


class CodeBuilder:
    def __init__(self) -> None:
        self.hex_instructions: list[str] = list()
        self.label_name_address_dict: dict[str, str] = dict()

    def __add_new_label(self, label: str) -> None:
        if label in self.label_name_address_dict.keys():
            raise Exception(f"Label {label} já foi usada")

        next_instruction_index = len(self.hex_instructions)
        next_instruction_address = eight_bit_int_to_hex_string(
            next_instruction_index)

        self.label_name_address_dict[label] = next_instruction_address

        return

    def process_line_of_code(self, raw_line_input: str) -> None:
        trimmed_line = raw_line_input.strip()

        if len(trimmed_line) == 0:
            return

        if is_goto_label(trimmed_line):
            # remove ":"
            label = trimmed_line[:-1]
            self.__add_new_label(label)
        else:
            instruction = parse_instruction(trimmed_line)
            hex_output = decode_instruction(instruction)
            self.hex_instructions.extend(hex_output)

        return

    def build_list_of_instructions(self) -> list[str]:
        code_output = list()

        for i in range(len(self.hex_instructions)):
            if self.hex_instructions[i] in self.label_name_address_dict.keys():
                hex_address = self.label_name_address_dict[self.hex_instructions[i]]
                code_output.append(hex_address)
            else:
                code_output.append(self.hex_instructions[i])

        return code_output
