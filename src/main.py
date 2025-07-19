from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from module_loader import ModuleLoader

def main():
    module_loader = ModuleLoader()
    try:
        with open("src/main.era", "r") as f:
            code = f.read()
        
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # print("Tokens:", tokens) # For debugging

        parser = Parser(tokens)
        ast = parser.parse()
        # print("AST:", ast) # For debugging

        interpreter = Interpreter(module_loader, "src/main.era")
        interpreter.interpret(ast)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()