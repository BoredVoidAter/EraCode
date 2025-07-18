from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def run_eracode(source_code):
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    # print("Tokens:", tokens) # For debugging

    parser = Parser(tokens)
    ast = parser.parse()
    # print("AST:", ast) # For debugging

    interpreter = Interpreter()
    interpreter.interpret(ast)

if __name__ == "__main__":
    # Example Usage:
    code = """
DearReader This is a comment
TheStoryOfUs favoriteAlbum is "1989"
TheStoryOfUs luckyNumber is 13
TheStoryOfUs result is luckyNumber + 22
SpeakNow favoriteAlbum
SpeakNow result
"""
    run_eracode(code)
