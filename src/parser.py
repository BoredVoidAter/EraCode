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

class FunctionDeclaration(ASTNode):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

class FunctionCall(ASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class ReturnStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class TheErasTourLoop(ASTNode):
    def __init__(self, element_variable, squad_variable, body):
        self.element_variable = element_variable
        self.squad_variable = squad_variable
        self.body = body

class JoinTheSquad(ASTNode):
    def __init__(self, squad_name, element):
        self.squad_name = squad_name
        self.element = element

class CastOut(ASTNode):
    def __init__(self, squad_name, index):
        self.squad_name = squad_name
        self.index = index

class RollCall(ASTNode):
    def __init__(self, squad_name):
        self.squad_name = squad_name

class MessageInABottle(ASTNode):
    def __init__(self):
        pass

class VaultDeclaration(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class VaultAccess(ASTNode):
    def __init__(self, vault_name, key):
        self.vault_name = vault_name
        self.key = key

class VaultAssignment(ASTNode):
    def __init__(self, vault_name, key, value):
        self.vault_name = vault_name
        self.key = key
        self.value = value

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
            # Check if it's a variable declaration or a squad declaration or vault declaration
            peek_token_type, peek_token_value = self.peek_token()
            if peek_token_type == 'IDENTIFIER':
                peek_token_type_2, peek_token_value_2 = self.peek_token(2)
                if peek_token_type_2 == 'ASSIGN' and peek_token_value_2 == 'is':
                    peek_token_type_3, peek_token_value_3 = self.peek_token(3)
                    if peek_token_type_3 == 'LBRACKET':
                        return self.parse_squad_declaration()
                    elif peek_token_type_3 == 'KEYWORD' and peek_token_value_3 == 'TheVault':
                        return self.parse_vault_declaration()
                    else:
                        return self.parse_var_declaration()
            raise Exception(f"Unexpected token after TheStoryOfUs: {peek_token_type} {peek_token_value}")
        elif token_type == 'KEYWORD' and token_value == 'SpeakNow':
            return self.parse_speak_now_statement()
        elif token_type == 'KEYWORD' and token_value == 'ShouldveSaidNo':
            return self.parse_if_statement()
        elif token_type == 'KEYWORD' and token_value == 'ThisIsMeTrying':
            return self.parse_while_statement()
        elif token_type == 'KEYWORD' and token_value == 'BeginAgain':
            return self.parse_function_declaration()
        elif token_type == 'KEYWORD' and token_value == 'SparksFly':
            return self.parse_return_statement()
        elif token_type == 'KEYWORD' and token_value == 'TheErasTour':
            return self.parse_the_eras_tour_loop()
        elif token_type == 'KEYWORD' and token_value == 'JoinTheSquad':
            return self.parse_join_the_squad()
        elif token_type == 'KEYWORD' and token_value == 'CastOut':
            return self.parse_cast_out()
        elif token_type == 'KEYWORD' and token_value == 'RollCall':
            return self.parse_roll_call()
        elif token_type == 'KEYWORD' and token_value == 'MessageInABottle':
            return self.parse_message_in_a_bottle()
        elif token_type == 'KEYWORD' and token_value == 'unlock':
            # Check if it's a vault assignment or a vault access
            # Peek at the token after the key and 'in' to see if it's 'is'
            # This requires peeking 4 tokens ahead: unlock (1) key (2) in (3) vault_name (4) is (5)
            # So we need to peek 4 tokens ahead from the current token (unlock)
            if self.peek_token(4)[0] == 'ASSIGN':
                return self.parse_vault_assignment()
            else:
                # If not an assignment, it must be an access, but it's an expression, not a statement
                raise Exception(f"'unlock' used as a statement must be an assignment. For access, use it within an expression.")
        elif token_type == 'IDENTIFIER' and self.peek_token()[0] == 'LPAREN': # Function call
            return self.parse_function_call()
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
        return self.parse_logical_expression()

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
            if self.peek_token()[0] == 'LPAREN': # Function call
                return self.parse_function_call()
            elif self.peek_token()[0] == 'KEYWORD' and self.peek_token()[1] == 'at': # Squad access
                return self.parse_squad_access()
            elif self.peek_token()[0] == 'KEYWORD' and self.peek_token()[1] == 'in': # Vault access
                return self.parse_vault_access()
            self.advance()
            return Identifier(token_value)
        elif token_type == 'KEYWORD' and token_value == 'MessageInABottle':
            self.advance()
            return MessageInABottle()
        elif token_type == 'KEYWORD' and token_value == 'RollCall':
            self.advance()
            squad_name = self.consume('IDENTIFIER')[1]
            return RollCall(squad_name)
        elif token_type == 'KEYWORD' and token_value == 'unlock':
            self.advance()
            key = self.parse_expression()
            self.consume('KEYWORD', 'in')
            vault_name = self.consume('IDENTIFIER')[1]
            return VaultAccess(vault_name, key)
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

    def parse_comparison_expression(self):
        left = self.parse_arithmetic_expression()
        while self.current_token_index < len(self.tokens) and self.current_token()[0] == 'COMPARE_OPERATOR':
            operator = self.consume('COMPARE_OPERATOR')
            right = self.parse_arithmetic_expression()
            left = ComparisonExpression(left, operator[1], right)
        return left

    def parse_logical_expression(self):
        left = self.parse_comparison_expression()
        while self.current_token_index < len(self.tokens) and self.current_token()[0] == 'LOGICAL_OPERATOR':
            operator = self.consume('LOGICAL_OPERATOR')
            right = self.parse_comparison_expression()
            left = LogicalExpression(left, operator[1], right)
        return left

    def parse_if_statement(self):
        self.consume('KEYWORD', 'ShouldveSaidNo')
        condition = self.parse_logical_expression()
        self.consume('KEYWORD', 'fearless')
        then_branch = self.parse_block()

        else_if_branches = []
        while self.current_token()[0] == 'KEYWORD' and self.current_token()[1] == 'OrMaybe':
            self.consume('KEYWORD', 'OrMaybe')
            condition = self.parse_logical_expression()
            self.consume('KEYWORD', 'fearless')
            branch = self.parse_block()
            else_if_branches.append((condition, branch))

        else_branch = None
        if self.current_token()[0] == 'KEYWORD' and self.current_token()[1] == 'EvenSo':
            self.consume('KEYWORD', 'EvenSo')
            self.consume('KEYWORD', 'fearless')
            else_branch = self.parse_block()
        
        self.consume('KEYWORD', 'TheEnd')
        return IfStatement(condition, then_branch, else_if_branches, else_branch)

    def parse_while_statement(self):
        self.consume('KEYWORD', 'ThisIsMeTrying')
        condition = self.parse_logical_expression()
        self.consume('KEYWORD', 'fearless')
        body = self.parse_block()
        self.consume('KEYWORD', 'TheEnd')
        return WhileStatement(condition, body)

    def parse_block(self):
        statements = []
        while not (self.current_token()[0] == 'KEYWORD' and self.current_token()[1] in ['TheEnd', 'OrMaybe', 'EvenSo']):
            statements.append(self.parse_statement())
        return statements

    def parse_squad_declaration(self):
        self.consume('KEYWORD', 'TheStoryOfUs')
        identifier = self.consume('IDENTIFIER')
        self.consume('ASSIGN', 'is')
        self.consume('LBRACKET')
        elements = []
        while not (self.current_token()[0] == 'RBRACKET'):
            elements.append(self.parse_expression())
            if self.current_token()[0] == 'COMMA':
                self.consume('COMMA')
        self.consume('RBRACKET')
        return VarDeclaration(identifier[1], SquadDeclaration(elements))

    def parse_squad_access(self):
        squad_name = self.consume('IDENTIFIER')
        self.consume('KEYWORD', 'at')
        index = self.parse_expression()
        return SquadAccess(squad_name[1], index)

    def parse_function_declaration(self):
        self.consume('KEYWORD', 'BeginAgain')
        name = self.consume('IDENTIFIER')[1]
        parameters = []
        if self.current_token()[0] == 'LPAREN':
            self.consume('LPAREN')
            while self.current_token()[0] == 'IDENTIFIER':
                parameters.append(self.consume('IDENTIFIER')[1])
                if self.current_token()[0] == 'COMMA':
                    self.consume('COMMA')
            self.consume('RPAREN')
        
        body = self.parse_block()
        self.consume('KEYWORD', 'TheEnd')
        return FunctionDeclaration(name, parameters, body)

    def parse_function_call(self):
        name = self.consume('IDENTIFIER')[1]
        self.consume('LPAREN')
        arguments = []
        while self.current_token()[0] != 'RPAREN':
            arguments.append(self.parse_expression())
            if self.current_token()[0] == 'COMMA':
                self.consume('COMMA')
        self.consume('RPAREN')
        return FunctionCall(name, arguments)

    def parse_return_statement(self):
        self.consume('KEYWORD', 'SparksFly')
        expression = self.parse_expression()
        return ReturnStatement(expression)

    def parse_the_eras_tour_loop(self):
        self.consume('KEYWORD', 'TheErasTour')
        element_variable = self.consume('IDENTIFIER')[1]
        self.consume('KEYWORD', 'in')
        squad_variable = self.parse_expression()
        self.consume('KEYWORD', 'fearless')
        body = self.parse_block()
        self.consume('KEYWORD', 'TheEnd')
        return TheErasTourLoop(element_variable, squad_variable, body)

    def parse_join_the_squad(self):
        self.consume('KEYWORD', 'JoinTheSquad')
        squad_name = self.consume('IDENTIFIER')[1]
        element = self.parse_expression()
        return JoinTheSquad(squad_name, element)

    def parse_cast_out(self):
        self.consume('KEYWORD', 'CastOut')
        squad_name = self.consume('IDENTIFIER')[1]
        index = self.parse_expression()
        return CastOut(squad_name, index)

    def parse_roll_call(self):
        self.consume('KEYWORD', 'RollCall')
        squad_name = self.consume('IDENTIFIER')[1]
        return RollCall(squad_name)

    def parse_message_in_a_bottle(self):
        self.consume('KEYWORD', 'MessageInABottle')
        self.consume('LPAREN')
        self.consume('RPAREN')
        return MessageInABottle()

    def parse_vault_declaration(self):
        self.consume('KEYWORD', 'TheStoryOfUs')
        identifier = self.consume('IDENTIFIER')
        self.consume('ASSIGN', 'is')
        self.consume('KEYWORD', 'TheVault')
        self.consume('LBRACE') # Assuming LBRACE and RBRACE for vault
        elements = []
        while not (self.current_token()[0] == 'RBRACE'):
            key = self.parse_expression()
            self.consume('COLON') # Assuming COLON for key-value separator
            value = self.parse_expression()
            elements.append((key, value))
            if self.current_token()[0] == 'COMMA':
                self.consume('COMMA')
        self.consume('RBRACE')
        return VarDeclaration(identifier[1], VaultDeclaration(elements))

    def parse_vault_access(self):
        key = self.parse_expression()
        self.consume('KEYWORD', 'in')
        vault_name = self.consume('IDENTIFIER')[1]
        return VaultAccess(vault_name, key)

    def parse_vault_assignment(self):
        self.consume('KEYWORD', 'unlock')
        key = self.parse_expression()
        self.consume('KEYWORD', 'in')
        vault_name = self.consume('IDENTIFIER')[1]
        self.consume('ASSIGN', 'is')
        value = self.parse_expression()
        return VaultAssignment(vault_name, key, value)