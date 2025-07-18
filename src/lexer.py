
import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_pos = 0

    def tokenize(self):
        token_specs = [
            ('SKIP', r'\s+'),  # Whitespace
            ('COMMENT', r'DearReader.*'),  # Single-line comments
            ('KEYWORD', r'TheStoryOfUs|SpeakNow'),  # Keywords
            ('ASSIGN', r'is'),  # Assignment operator
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identifiers
            ('STRING', r'"[^"]*"'),  # String literals
            ('NUMBER', r'\d+'),  # Integer literals
            ('OPERATOR', r'[+\-*/]'),  # Operators
        ]

        token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
        
        for match in re.finditer(token_regex, self.source_code):
            token_type = match.lastgroup
            token_value = match.group(token_type)

            if token_type == 'SKIP':
                continue
            elif token_type == 'COMMENT':
                continue
            elif token_type == 'STRING':
                self.tokens.append((token_type, token_value[1:-1]))  # Remove quotes
            else:
                self.tokens.append((token_type, token_value))
        
        return self.tokens
