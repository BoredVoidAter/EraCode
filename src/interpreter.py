import os
from parser import VarDeclaration, SpeakNowStatement, NumberLiteral, StringLiteral, BinaryExpression, Identifier, IfStatement, WhileStatement, SquadDeclaration, SquadAccess, FunctionDeclaration, FunctionCall, ReturnStatement, TheErasTourLoop, JoinTheSquad, CastOut, RollCall, MessageInABottle, VaultDeclaration, VaultAccess, VaultAssignment, DearJohnStatement, AllTooWellExpression, BlankSpaceLiteral, CallItWhatYouWantStatement, ChooseYourPlayerStatement
from module_loader import ModuleLoader

class Interpreter:
    def __init__(self, module_loader=None, current_file=None):
        self.variables = {}
        self.functions = {}
        self.module_loader = module_loader if module_loader else ModuleLoader()
        self.current_file = current_file

    def interpret(self, ast):
        for statement in ast.statements:
            self.execute_statement(statement)

    def execute_statement(self, statement):
        if isinstance(statement, VarDeclaration):
            self.execute_var_declaration(statement)
        elif isinstance(statement, SpeakNowStatement):
            self.execute_speak_now_statement(statement)
        elif isinstance(statement, IfStatement):
            self.execute_if_statement(statement)
        elif isinstance(statement, WhileStatement):
            self.execute_while_statement(statement)
        elif isinstance(statement, FunctionDeclaration):
            self.execute_function_declaration(statement)
        elif isinstance(statement, FunctionCall):
            self.execute_function_call(statement)
        elif isinstance(statement, ReturnStatement):
            return self.execute_return_statement(statement)
        elif isinstance(statement, TheErasTourLoop):
            self.execute_the_eras_tour_loop(statement)
        elif isinstance(statement, JoinTheSquad):
            self.execute_join_the_squad(statement)
        elif isinstance(statement, CastOut):
            self.execute_cast_out(statement)
        elif isinstance(statement, RollCall):
            self.execute_roll_call(statement)
        elif isinstance(statement, MessageInABottle):
            return self.execute_message_in_a_bottle(statement)
        elif isinstance(statement, VaultDeclaration):
            self.execute_vault_declaration(statement)
        elif isinstance(statement, VaultAssignment):
            self.execute_vault_assignment(statement)
        elif isinstance(statement, DearJohnStatement):
            self.execute_dear_john_statement(statement)
        elif isinstance(statement, CallItWhatYouWantStatement):
            self.execute_call_it_what_you_want_statement(statement)
        elif isinstance(statement, ChooseYourPlayerStatement):
            self.execute_choose_your_player_statement(statement)
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
        elif isinstance(expression, SquadDeclaration):
            return [self.evaluate_expression(e) for e in expression.elements]
        elif isinstance(expression, SquadAccess):
            squad = self.variables[expression.squad_name]
            index = self.evaluate_expression(expression.index)
            return squad[index]
        elif isinstance(expression, FunctionCall):
            return self.execute_function_call(expression)
        elif isinstance(expression, RollCall):
            return self.execute_roll_call(expression)
        elif isinstance(expression, MessageInABottle):
            return self.execute_message_in_a_bottle(expression)
        elif isinstance(expression, VaultDeclaration):
            vault = {}
            for key_expr, value_expr in expression.elements:
                key = self.evaluate_expression(key_expr)
                value = self.evaluate_expression(value_expr)
                vault[key] = value
            return vault
        elif isinstance(expression, VaultAccess):
            vault = self.variables[expression.vault_name]
            key = self.evaluate_expression(expression.key)
            return vault[key]
        elif isinstance(expression, BlankSpaceLiteral):
            return None
        elif isinstance(expression, AllTooWellExpression):
            return self.execute_all_too_well_expression(expression)
        else:
            raise Exception(f"Unknown expression type: {type(expression)}")

    def execute_if_statement(self, statement):
        if self.evaluate_expression(statement.condition):
            for s in statement.then_branch:
                self.execute_statement(s)
        else:
            executed_else_if = False
            for condition, branch in statement.else_if_branches:
                if self.evaluate_expression(condition):
                    for s in branch:
                        self.execute_statement(s)
                    executed_else_if = True
                    break
            if not executed_else_if and statement.else_branch:
                for s in statement.else_branch:
                    self.execute_statement(s)

    def execute_while_statement(self, statement):
        while self.evaluate_expression(statement.condition):
            for s in statement.body:
                self.execute_statement(s)

    def execute_function_declaration(self, statement):
        self.functions[statement.name] = statement

    def execute_function_call(self, statement):
        func_declaration = self.functions[statement.name]
        
        # Save current scope
        original_variables = self.variables.copy()
        
        # Create new scope for function
        self.variables = {}
        for i, param in enumerate(func_declaration.parameters):
            self.variables[param] = self.evaluate_expression(statement.arguments[i])

        return_value = None
        for s in func_declaration.body:
            result = self.execute_statement(s)
            if isinstance(result, ReturnStatement):
                return_value = self.evaluate_expression(result.expression)
                break
        
        # Restore original scope
        self.variables = original_variables
        return return_value

    def execute_return_statement(self, statement):
        return statement # Return the statement itself to be handled by the caller

    def execute_the_eras_tour_loop(self, statement):
        squad = self.evaluate_expression(statement.squad_variable)
        if not isinstance(squad, list):
            raise Exception(f"TheErasTour can only iterate over Squads (lists). Got: {type(squad)}")
        
        original_variables = self.variables.copy()
        for element in squad:
            self.variables[statement.element_variable] = element
            for s in statement.body:
                self.execute_statement(s)
        self.variables = original_variables

    def execute_join_the_squad(self, statement):
        squad = self.variables[statement.squad_name]
        if not isinstance(squad, list):
            raise Exception(f"JoinTheSquad can only be used with Squads (lists). Got: {type(squad)}")
        element = self.evaluate_expression(statement.element)
        squad.append(element)

    def execute_cast_out(self, statement):
        squad = self.variables[statement.squad_name]
        if not isinstance(squad, list):
            raise Exception(f"CastOut can only be used with Squads (lists). Got: {type(squad)}")
        index = self.evaluate_expression(statement.index)
        if not isinstance(index, int):
            raise Exception(f"CastOut index must be an integer. Got: {type(index)}")
        if index < 0 or index >= len(squad):
            raise Exception(f"Index out of bounds for CastOut: {index}")
        squad.pop(index)

    def execute_roll_call(self, statement):
        squad = self.variables[statement.squad_name]
        if not isinstance(squad, list):
            raise Exception(f"RollCall can only be used with Squads (lists). Got: {type(squad)}")
        return len(squad)

    def execute_message_in_a_bottle(self, statement):
        return input()

    def execute_vault_declaration(self, statement):
        vault = {}
        for key_expr, value_expr in statement.value.elements:
            key = self.evaluate_expression(key_expr)
            value = self.evaluate_expression(value_expr)
            vault[key] = value
        self.variables[statement.identifier] = vault

    def execute_vault_assignment(self, statement):
        vault = self.variables[statement.vault_name]
        if not isinstance(vault, dict):
            raise Exception(f"Cannot assign to a non-Vault type: {type(vault)}")
        key = self.evaluate_expression(statement.key)
        value = self.evaluate_expression(statement.value)
        vault[key] = value

    def execute_dear_john_statement(self, statement):
        data = self.evaluate_expression(statement.data)
        filepath = self.evaluate_expression(statement.filepath)
        with open(filepath, 'w') as f:
            f.write(str(data))

    def execute_all_too_well_expression(self, expression):
        filepath = self.evaluate_expression(expression.filepath)
        with open(filepath, 'r') as f:
            content = f.read()
        return content

    def execute_call_it_what_you_want_statement(self, statement):
        module_filepath = self.evaluate_expression(statement.filepath)
        # Get the directory of the current file being interpreted
        current_file_dir = os.path.dirname(os.path.abspath(self.current_file))
        module_variables, module_functions = self.module_loader.load_module(module_filepath, self, current_file_dir)
        
        # Import the specified function or variable
        if statement.name in module_functions:
            self.functions[statement.name] = module_functions[statement.name]
        elif statement.name in module_variables:
            self.variables[statement.name] = module_variables[statement.name]
        else:
            raise Exception(f"'TheManor' does not contain {statement.name}")

    def execute_choose_your_player_statement(self, statement):
        variable_value = self.evaluate_expression(statement.variable)
        executed_case = False
        for case_value_expr, case_body in statement.cases:
            case_value = self.evaluate_expression(case_value_expr)
            if variable_value == case_value:
                for s in case_body:
                    self.execute_statement(s)
                executed_case = True
                break
        if not executed_case and statement.default_case:
            for s in statement.default_case:
                self.execute_statement(s)
