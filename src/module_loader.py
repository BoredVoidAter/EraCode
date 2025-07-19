import os
from lexer import Lexer
from parser import Parser

class ModuleLoader:
    def __init__(self):
        self.loaded_modules = {}

    def load_module(self, filepath, interpreter, current_dir):
        # Construct absolute path for the module file
        absolute_filepath = os.path.abspath(os.path.join(current_dir, filepath))

        if absolute_filepath in self.loaded_modules:
            return self.loaded_modules[absolute_filepath]

        with open(absolute_filepath, 'r') as f:
            code = f.read()

        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Use the provided interpreter instance for the module
        interpreter.interpret(ast)

        # Store the module's exported variables and functions
        self.loaded_modules[absolute_filepath] = interpreter.variables.copy(), interpreter.functions.copy()
        return self.loaded_modules[absolute_filepath]
