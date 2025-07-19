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

DearReader Custom Functions with 'BeginAgain'
BeginAgain greet(name)
    SpeakNow "Hello, " + name + "!"
TheEnd
greet("Swiftie")

BeginAgain add(a, b)
    SparksFly a + b
TheEnd
TheStoryOfUs sum is add(5, 7)
SpeakNow sum

DearReader TheErasTour - Collection Iteration
TheStoryOfUs mySquad is ["Taylor", "Selena", "Gigi"]
TheErasTour member in mySquad fearless
    SpeakNow member
TheEnd

DearReader Expanded 'Squad' Management
JoinTheSquad mySquad "Blake"
SpeakNow mySquad
CastOut mySquad 0
SpeakNow mySquad
TheStoryOfUs squadSize is RollCall mySquad
SpeakNow squadSize

DearReader Interactive Input with 'MessageInABottle'
TheStoryOfUs favoriteSong is "Love Story"
SpeakNow "You like " + favoriteSong + "! Great choice."

DearReader TheVault - Key-Value Data Structures
TheStoryOfUs myVault is TheVault { "artist": "Taylor Swift", "album": "Red" }
SpeakNow unlock "artist" in myVault
unlock "album" in myVault is "Fearless"
SpeakNow unlock "album" in myVault
"""
    run_eracode(code)