
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
            ('KEYWORD', r'TheStoryOfUs|SpeakNow|ShouldveSaidNo|OrMaybe|EvenSo|ThisIsMeTrying|fearless|guilty|getElementFrom|at|BeginAgain|TheEnd|SparksFly|TheErasTour|in|JoinTheSquad|CastOut|RollCall|MessageInABottle|TheVault|unlock'),  # Keywords
            ('ASSIGN', r'is'),  # Assignment operator
            ('COMPARE_OPERATOR', r'isnt|is|moreThan|lessThan'), # Comparison operators
            ('LOGICAL_OPERATOR', r'and|or'), # Logical operators
            ('LPAREN', r'\('), # Left parenthesis
            ('RPAREN', r'\)'), # Right parenthesis
            ('LBRACKET', r'\['), # Left bracket for Squad
            ('RBRACKET', r'\]'), # Right bracket for Squad
            ('LBRACE', r'\{'), # Left brace for Vault
            ('RBRACE', r'\}'), # Right brace for Vault
            ('COMMA', r','), # Comma for Squad elements
            ('COLON', r':'), # Colon for Vault key-value pairs
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identifiers
            ('STRING', r'"[^"]*"'),  # String literals
            ('NUMBER', r'\d+'),  # Integer literals
            ('ARITHMETIC_OPERATOR', r'[+\-*/]'),  # Arithmetic Operators
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
