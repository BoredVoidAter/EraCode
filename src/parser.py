
class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class VarDeclaration(ASTNode):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

class SpeakNowStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class NumberLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse(self):
        statements = []
        while self.current_token_index < len(self.tokens):
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        token_type, token_value = self.current_token()

        if token_type == 'KEYWORD' and token_value == 'TheStoryOfUs':
            return self.parse_var_declaration()
        elif token_type == 'KEYWORD' and token_value == 'SpeakNow':
            return self.parse_speak_now_statement()
        else:
            raise Exception(f"Unexpected token: {token_type} {token_value}")

    def parse_var_declaration(self):
        self.consume('KEYWORD', 'TheStoryOfUs')
        identifier = self.consume('IDENTIFIER')
        self.consume('ASSIGN', 'is')
        value = self.parse_expression()
        return VarDeclaration(identifier[1], value)

    def parse_speak_now_statement(self):
        self.consume('KEYWORD', 'SpeakNow')
        expression = self.parse_expression()
        return SpeakNowStatement(expression)

    def parse_expression(self):
        return self.parse_arithmetic_expression()

    def parse_arithmetic_expression(self):
        left = self.parse_primary_expression()

        while self.current_token_index < len(self.tokens) and self.current_token()[0] == 'OPERATOR':
            operator = self.consume('OPERATOR')
            right = self.parse_primary_expression()
            left = BinaryExpression(left, operator[1], right)
        return left

    def parse_primary_expression(self):
        token_type, token_value = self.current_token()

        if token_type == 'NUMBER':
            self.advance()
            return NumberLiteral(int(token_value))
        elif token_type == 'STRING':
            self.advance()
            return StringLiteral(token_value)
        elif token_type == 'IDENTIFIER':
            self.advance()
            return Identifier(token_value)
        else:
            raise Exception(f"Unexpected token in expression: {token_type} {token_value}")

    def current_token(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None, None

    def advance(self):
        self.current_token_index += 1

    def consume(self, expected_type, expected_value=None):
        token_type, token_value = self.current_token()
        if token_type == expected_type and (expected_value is None or token_value == expected_value):
            self.advance()
            return token_type, token_value
        else:
            raise Exception(f"Expected {expected_type} {expected_value if expected_value else ''}, got {token_type} {token_value}")
