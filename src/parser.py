
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

class BooleanLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class ComparisonExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class LogicalExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class IfStatement(ASTNode):
    def __init__(self, condition, then_branch, else_if_branches, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_if_branches = else_if_branches # List of (condition, branch) tuples
        self.else_branch = else_branch

class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class SquadDeclaration(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class SquadAccess(ASTNode):
    def __init__(self, squad_name, index):
        self.squad_name = squad_name
        self.index = index

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
            # Check if it's a variable declaration or a squad declaration
            # Peek at the next token to differentiate
            peek_token_type, peek_token_value = self.peek_token()
            if peek_token_type == 'IDENTIFIER':
                # After identifier, check for 'is' or '['
                peek_token_type_2, peek_token_value_2 = self.peek_token(2)
                if peek_token_type_2 == 'ASSIGN' and peek_token_value_2 == 'is':
                    return self.parse_var_declaration()
                elif peek_token_type_2 == 'LBRACKET':
                    return self.parse_squad_declaration()
            raise Exception(f"Unexpected token after TheStoryOfUs: {peek_token_type} {peek_token_value}")
        elif token_type == 'KEYWORD' and token_value == 'SpeakNow':
            return self.parse_speak_now_statement()
        elif token_type == 'KEYWORD' and token_value == 'ShouldveSaidNo':
            return self.parse_if_statement()
        elif token_type == 'KEYWORD' and token_value == 'ThisIsMeTrying':
            return self.parse_while_statement()
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

        while self.current_token_index < len(self.tokens) and self.current_token()[0] == 'ARITHMETIC_OPERATOR':
            operator = self.consume('ARITHMETIC_OPERATOR')
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

    def peek_token(self, offset=1):
        peek_pos = self.current_token_index + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return None, None

    def consume(self, expected_type, expected_value=None):
        token_type, token_value = self.current_token()
        if token_type == expected_type and (expected_value is None or token_value == expected_value):
            self.advance()
            return token_type, token_value
        else:
            raise Exception(f"Expected {expected_type} {expected_value if expected_value else ''}, got {token_type} {token_value}")
