
from parser import VarDeclaration, SpeakNowStatement, NumberLiteral, StringLiteral, BinaryExpression, Identifier

class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, ast):
        for statement in ast.statements:
            self.execute_statement(statement)

    def execute_statement(self, statement):
        if isinstance(statement, VarDeclaration):
            self.execute_var_declaration(statement)
        elif isinstance(statement, SpeakNowStatement):
            self.execute_speak_now_statement(statement)
        else:
            raise Exception(f"Unknown statement type: {type(statement)}")

    def execute_var_declaration(self, statement):
        value = self.evaluate_expression(statement.value)
        self.variables[statement.identifier] = value

    def execute_speak_now_statement(self, statement):
        value = self.evaluate_expression(statement.expression)
        print(value)

    def evaluate_expression(self, expression):
        if isinstance(expression, NumberLiteral):
            return expression.value
        elif isinstance(expression, StringLiteral):
            return expression.value
        elif isinstance(expression, Identifier):
            if expression.name in self.variables:
                return self.variables[expression.name]
            else:
                raise Exception(f"Undefined variable: {expression.name}")
        elif isinstance(expression, BinaryExpression):
            left = self.evaluate_expression(expression.left)
            right = self.evaluate_expression(expression.right)
            if expression.operator == '+':
                return left + right
            elif expression.operator == '-':
                return left - right
            elif expression.operator == '*':
                return left * right
            elif expression.operator == '/':
                return left / right
            else:
                raise Exception(f"Unknown operator: {expression.operator}")
        else:
            raise Exception(f"Unknown expression type: {type(expression)}")
