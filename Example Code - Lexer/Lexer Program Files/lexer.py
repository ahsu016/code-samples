# Authors: Eduardo, Alex, Audrey

class Token:
    def __init__(self, token_type, lexeme):
        self.token_type = token_type
        self.lexeme = lexeme

    def __str__(self):
        return f"{self.token_type:<15}{self.lexeme:<15}"


class Lexer:
    KEYWORDS = ['while', 'if', 'elif', 'or', 'else',
                'for', 'try', 'catch', 'switch', 'case', 'return']
    OPERATORS = ['<=', '=', '+', '-', '*', '/', '%', '>', '>=', '!=']
    SEPARATORS = ['(', ')', ';', '{', '}', '[', ']']

    def is_alpha(self, char):
        return char.isalpha() or char == '_'

    def is_digit(self, char):
        return char.isdigit()

    def is_alphanumeric(self, char):
        return self.is_alpha(char) or self.is_digit(char)

    def lexer(self, source_code):
        i = 0
        in_comment = False
        while i < len(source_code):
            while i < len(source_code) and source_code[i].isspace():
                i += 1

            if i >= len(source_code):
                break

            if source_code[i:i+2] == '[*':
                in_comment = True
                i += 2
                continue
            elif source_code[i:i+2] == '*]':
                in_comment = False
                i += 2
                continue

            if in_comment:
                i += 1
                continue

            # Identifying tokens
            start = i
            if self.is_alpha(source_code[i]):  # Identifier or Keyword
                while i < len(source_code) and self.is_alphanumeric(source_code[i]):
                    i += 1
                lexeme = source_code[start:i]
                token_type = 'keyword' if lexeme in self.KEYWORDS else 'identifier'
                yield Token(token_type, lexeme)
            # Numeric or Real
            elif self.is_digit(source_code[i]) or (source_code[i] == '.' and i+1 < len(source_code) and self.is_digit(source_code[i+1])):
                is_real = False
                while i < len(source_code) and (self.is_digit(source_code[i]) or (not is_real and source_code[i] == '.')):
                    is_real = is_real or source_code[i] == '.'
                    i += 1
                token_type = 'real' if is_real else 'integer'
                yield Token(token_type, source_code[start:i])
            else:  # Operator or Separator
                if i + 1 < len(source_code) and source_code[i:i+2] in self.OPERATORS:
                    yield Token('operator', source_code[i:i+2])
                    i += 2
                elif source_code[i] in self.OPERATORS:
                    yield Token('operator', source_code[i])
                    i += 1
                elif source_code[i] in self.SEPARATORS:
                    yield Token('separator', source_code[i])
                    i += 1
                else:
                    print(f"Unknown character: {source_code[i]}")
                    i += 1


def main():
    input1 = 'while (fahr <= upper) a = 23.00; [* this is a sample *]'
    input2 = 'for (dog > 0) dog *= 10; [*This is a comment -> Comparing the identifier with int*] '
    input3 = "if (moo != frog) { \
                        6 + 4; \
                        } \
                        else { \
                            return 5; \
                        }"

    fallback_inputs = [input1, input2, input3]
    input_file_paths = ["input1.txt", "input2.txt", "input3.txt"]
    output_file_path = ['output1.txt', 'output2.txt', 'output3.txt']

    lexer_instance = Lexer()

    for idx, (input_path, output_path) in enumerate(zip(input_file_paths, output_file_path)):
        source_code = fallback_inputs[idx]  # Default to the fallback input
        try:
            with open(input_path, 'r') as file:
                source_code = file.read()  # Overwrite with content from file if it exists
        except FileNotFoundError:
            print(f"{input_path} not found. Using fallback input.")

        with open(output_path, 'w') as file:
            file.write(f"{'Token':<15}{'Lexeme':<15}\n")
            file.write(f"{'-'*30}\n")
            # lexer now takes source_code string instead of input_path
            for token in lexer_instance.lexer(source_code):
                file.write(str(token) + '\n')


if __name__ == "__main__":
    main()
