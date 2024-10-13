import random

# Global variables
board = ["-", "-", "-",
         "-", "-", "-",
         "-", "-", "-"]

currentPlayer = "X"
winner = None
gameRunning = True
gameMode = None
difficulty = None

player1_wins = 0
player2_wins = 0
computer_wins = 0
starting_player = "X"

# Print the game board with color coding
def printBoard(board):
    for i in range(0, 9, 3):
        row = ""
        for j in range(3):
            cell = board[i + j]
            if cell == "X":
                row += "\033[91m" + cell + "\033[0m"
            elif cell == "O":
                row += "\033[94m" + cell + "\033[0m"
            else:
                row += cell
            if j < 2:
                row += " | "
        print(row)
        if i < 6:
            print("---------")

# Player input for choosing a move
def playerInput(board):
    inp = int(input(f"Player {currentPlayer}, enter a number (1-9): "))
    if 1 <= inp <= 9 and board[inp-1] == "-":
        board[inp-1] = currentPlayer
    else:
        print("Invalid move. Try again.")

# Check for a win or tie
def checkHorizontal(board):
    global winner
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] != "-":
            winner = board[i]
            return True
    return False

def checkVert(board):
    global winner
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != "-":
            winner = board[i]
            return True
    return False

def checkDiagonal(board):
    global winner
    if (board[0] == board[4] == board[8] != "-") or (board[2] == board[4] == board[6] != "-"):
        winner = board[4]
        return True
    return False

def checkTie(board):
    global gameRunning
    if "-" not in board and winner is None:
        printBoard(board)
        print("The game is a tie!")
        gameRunning = False
        restartGame()

def checkGameWin():
    global gameRunning, player1_wins, player2_wins, computer_wins
    if checkDiagonal(board) or checkHorizontal(board) or checkVert(board):
        printBoard(board)
        print(f"The Winner is {winner}")
        gameRunning = False
        if winner == "X":
            player1_wins += 1
        elif winner == "O":
            if gameMode == "PP":
                player2_wins += 1
            else:
                computer_wins += 1
        displayWinTotals()
        restartGame()

def switchPlayer():
    global currentPlayer
    currentPlayer = "O" if currentPlayer == "X" else "X"

# Evaluates the board for minimax
def evaluate(board):
    if board[0] == board[1] == board[2] != "-":
        return 1 if board[0] == "O" else -1
    elif board[3] == board[4] == board[5] != "-":
        return 1 if board[3] == "O" else -1
    elif board[6] == board[7] == board[8] != "-":
        return 1 if board[6] == "O" else -1
    elif board[0] == board[3] == board[6] != "-":
        return 1 if board[0] == "O" else -1
    elif board[1] == board[4] == board[7] != "-":
        return 1 if board[1] == "O" else -1
    elif board[2] == board[5] == board[8] != "-":
        return 1 if board[2] == "O" else -1
    elif board[0] == board[4] == board[8] != "-":
        return 1 if board[0] == "O" else -1
    elif board[2] == board[4] == board[6] != "-":
        return 1 if board[2] == "O" else -1
    return 0

def minimax(board, depth, isMaximizing):
    score = evaluate(board)
    if score == 1 or score == -1:
        return score
    if "-" not in board:
        return 0

    if isMaximizing:
        bestScore = -float('inf')
        for i in range(9):
            if board[i] == "-":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = "-"
                bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = float('inf')
        for i in range(9):
            if board[i] == "-":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = "-"
                bestScore = min(score, bestScore)
        return bestScore

def hardComputerMove(board):
    bestScore = -float('inf')
    bestMove = None
    for i in range(9):
        if board[i] == "-":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = "-"
            if score > bestScore:
                bestScore = score
                bestMove = i
    if bestMove is not None:
        board[bestMove] = "O"
        print(f"Computer moved at position {bestMove + 1}")

def easyComputerMove(board):
    while currentPlayer == "O":
        position = random.randint(0, 8)
        if board[position] == "-":
            board[position] = "O"
            print(f"Computer moved at position {position + 1}")
            break

def restartGame():
    global board, currentPlayer, winner, gameRunning, starting_player
    restart = input("Play again? (y/n): ").lower()
    if restart == 'y':
        board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
        winner = None
        gameRunning = True
        starting_player = "O" if starting_player == "X" else "X"
        currentPlayer = starting_player
        main()
    else:
        print("Thanks for playing!")

def displayWinTotals():
    if gameMode == "PP":
        print(f"Player 1 (X) Wins: {player1_wins}")
        print(f"Player 2 (O) Wins: {player2_wins}")
    else:
        print(f"Player Wins: {player1_wins}")
        print(f"Computer Wins: {computer_wins}")

def main():
    global gameMode, difficulty
    gameMode = input("Player vs Player (PP) or Player vs Computer (C)? ").upper()
    while gameMode not in ["PP", "C"]:
        gameMode = input("Invalid choice. Please type PP for Player vs Player or C for Player vs Computer: ").upper()

    if gameMode == "C":
        difficulty = input("Choose difficulty: Easy (E) or Hard (H): ").upper()
        while difficulty not in ["E", "H"]:
            difficulty = input("Invalid choice. Please type E for Easy or H for Hard: ").upper()

    while gameRunning:
        printBoard(board)
        if winner:
            break
        if gameMode == "PP" or (gameMode == "C" and currentPlayer == "X"):
            playerInput(board)
        elif gameMode == "C" and currentPlayer == "O":
            if difficulty == "H":
                hardComputerMove(board)
            else:
                easyComputerMove(board)
        checkGameWin()
        checkTie(board)
        switchPlayer()

main()
