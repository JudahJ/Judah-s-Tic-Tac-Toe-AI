import random

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, game):
        raise NotImplementedError("Subclass must implement abstract method")

class HumanPlayer(Player):
    def make_move(self, game):
        while True:
            try:
                move = int(input(f"Enter your move for '{self.symbol}' (0-8): "))
                if game.is_valid_move(move):
                    game.make_move(move, self.symbol)
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a number.")

class AIPlayer(Player):
    def __init__(self, symbol, strategy):
        super().__init__(symbol)
        self.strategy = strategy

    def make_move(self, game):
        print(f"{self.symbol}'s AI is thinking...")
        move = self.strategy.determine_move(game)
        if game.is_valid_move(move):
            game.make_move(move, self.symbol)
        else:
            print(f"Error: Invalid move suggested by {self.symbol}'s AI. Defaulting to random move.")
            for i in range(9):
                if game.is_valid_move(i):
                    game.make_move(i, self.symbol)
                    break

class TicTacToe:
    def __init__(self, player1, player2):
        self.board = [' ' for _ in range(9)]
        self.players = [player1, player2]

    def play(self):
        while True:
            for player in self.players:
                self.display_board()
                player.make_move(self)
                if self.check_win(self.board):  # Use self.board instead of game.board
                    self.display_board()
                    print(f"{player.symbol} wins!")
                    return
                if self.is_board_full():
                    self.display_board()
                    print("It's a draw!")
                    return

    def is_valid_move(self, move):
        return self.board[move] == ' ' and 0 <= move <= 8

    def make_move(self, move, symbol):
        self.board[move] = symbol

    def check_win(self, theBoard):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        return any(all(theBoard[i] == symbol for i in combo) for symbol in ['X', 'O'] for combo in win_conditions)

    def is_board_full(self):
        return ' ' not in self.board

    def display_board(self):
        for i in range(0, 9, 3):
            print(f" {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} ")
            if i < 6:
                print("-----------")
        print()
    #Helper function for JudahsCoolAI
    def make_temporary_move(self, move, symbol):
        original_symbol = self.board[move] #Have a place to keep what the original board looks like withouto making a move
        self.board[move] = symbol #This is having the player "move" to a pos on the board. The player doesn't actually move
        is_winning = self.check_win(self.board) #Check if that player move is a winning one
        self.board[move] = original_symbol  # reset it back to its original state
        return is_winning
        
    def checkPlayer(self):
        availableMoves = []
        for i in range(9):
            if self.is_valid_move(i):
                availableMoves.append(i)
        if (len(availableMoves)%2 == 0):
            return 1
        else:
            return 0
    
    


class SimpleAI:
    def determine_move(self, game):
        for i in range(9):
            if game.is_valid_move(i):
                game.board[i] = 'X'  # Assuming this AI plays 'X'
                if game.check_win(game.board):
                    game.board[i] = ' '  # Reset for actual move
                    return i
                game.board[i] = ' '  # Reset for next check
        for i in range(9):
            if game.is_valid_move(i):
                game.board[i] = 'O'  # Check if opponent ('O') could win
                if game.check_win(game.board):
                    game.board[i] = ' '  # Reset for actual move
                    return i
                game.board[i] = ' '  # Reset for next check
        for i in range(9):
            if game.is_valid_move(i):
                return i

class RandomAI:
    def determine_move(self, game):
        possibleMoves = [i for i in range(9) if game.is_valid_move(i)]
        return random.choice(possibleMoves)

#No Look Ahead AI
#CornerAI prioritizes opposite corners, then any corner, then the center, then random move
class CornersAI:
    def determine_move(self, game):
        # Lambda to check if a move is winning
        is_winning_move = lambda symbol, move: (game.is_valid_move(move) and game.make_temporary_move(move, symbol))

        #This'll check for a winning move for both the AI and the opponent
        if (self.symbol == 'X'):
            opponent = 'O'
        else:
            opponent = 'X'
        for symbol in (self.symbol, opponent):  
            for move in range(9):
                if is_winning_move(symbol, move):
                    return move

        # pick corners if u can
        corners = [0,8,2,6]

        for c in range(len(corners)):
            if game.is_valid_move(corners[c])==True:
                return corners[c]

        # pick middle if u can
        if game.is_valid_move(4):
            return 4

        # Pick a random available spot if there's no moves
        possible_moves = [i for i in range(9) if game.is_valid_move(i)]
        return random.choice(possible_moves)

#Priotitizes center then corners then random spots if corners and center is taken. Follows this strat unless there is a winning move.
class JudahsCoolAI:
    def determine_move(self, game):
        # Lambda to check if a move is winning
        is_winning_move = lambda symbol, move: (game.is_valid_move(move) and game.make_temporary_move(move, symbol)) #It doesn't know move and symbol yet until we call it with the values
        
        # pick middle if u can
        if game.is_valid_move(4):
            return 4

        #This'll check for a winning move for both the AI and the opponent and also where you call the lambda
        for symbol in ('O', 'X'):  
            for move in range(9):
                if is_winning_move(symbol, move):
                    return move

        # pick corners if u can
        corners = [i for i in [0, 2, 6, 8] if game.is_valid_move(i)]
        if corners:
            return random.choice(corners)

        # Pick a random available spot if there's no moves
        possible_moves = [i for i in range(9) if game.is_valid_move(i)]
        return random.choice(possible_moves)


#Minimax AI
class NoahJudahMiniMax:

    def determine_move(self, game):
        best_score = float("inf")
        best_move = [] #List of all the best moves
        is_maximizing = None #Decides if we are maximizing or not
        availableMoves = [] #All moves that are available
        score = 0

        AIsym = game.players[game.checkPlayer()].symbol

        if AIsym == 'X':
            is_maximizing = True
        else:
            is_maximizing = False
            best_score = -float("inf")
        
        for i in range(9):
            if game.is_valid_move(i):
                availableMoves.append(i)
                game.board[i] = AIsym  # Assume 'O' is the AI's symbol
                score = self.minimax(game, is_maximizing)
                game.board[i] = ' '  # Undo move
                if is_maximizing and best_score >= score:
                    if score < best_score:
                        best_move = []
                    best_score = score
                    best_move.append(i)
                if not is_maximizing and best_score <= score:
                    if best_score < score:
                        best_move = []
                    best_score = score
                    best_move.append(i)

        if len(best_move) == 0:
            best_move = availableMoves[random.randint(0,len(availableMoves)-1)]
        
        return best_move[random.randint(0,len(best_move)-1)]

    def minimax(self, game, is_maximizing):
        if game.check_win(game.board):
            if is_maximizing:
                return -1  # AI wins
            else:
                return 1  # Opponent wins
        elif game.is_board_full():
            return 0  # Tie
        
        p = game.players[game.checkPlayer()].symbol
        
        if is_maximizing:
            best_score = -float("inf")
            for i in range(9):
                if game.is_valid_move(i):
                    game.board[i] = 'O'  # Opponent's symbol
                    score = self.minimax(game, False)
                    game.board[i] = ' '  # Undo move
                    best_score = max(score, best_score)

            return best_score

        if not is_maximizing:
            best_score = float("inf")
            for i in range(9):
                if game.is_valid_move(i):
                    game.board[i] = 'X'  # AI's symbol
                    score = self.minimax(game, True)
                    game.board[i] = ' '  # Undo move
                    best_score = min(score, best_score)
                    #print(best_score,p,i)
            
            return best_score



#RandomAI to poke holes in other codes.
class SmartRandomAI:
    def determine_move(self, game):
        availableMoves = []
        if (self.symbol == 'X'):
            opponent = 'O'
        else:
            opponent = 'X'
        for i in range(9):
            if game.is_valid_move(i):
                    availableMoves.append(i)
                    game.board[i] = self.symbol # Assuming this AI plays 'X'
                    if game.check_win(game.board)==True:
                        game.board[i] = ' '  # Reset for actual move
                        return i
                    game.board[i] = opponent
                    if game.check_win(game.board)==True:
                        game.board[i] = ' '  # Reset for actual move
                        return i
                    game.board[i] = ' '
        game.board[i] = ' '
        return (availableMoves[random.randint(0,len(availableMoves)-1)])

if __name__ == "__main__":
    player1 = HumanPlayer('O')
    player2 = AIPlayer('X', JudahsMiniMax())
    game = TicTacToe(player1, player2)
    game.play()
