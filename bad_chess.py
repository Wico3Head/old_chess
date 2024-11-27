import pygame, sys
pygame.init()

screenWidth, screenHeight = 800, 800
screen = pygame.display.set_mode((screenWidth, screenHeight))
font = pygame.font.SysFont("Courier", 30)
pygame.display.set_caption("Chess")

wKing = pygame.image.load('Assets/whiteKing.png')
bKing = pygame.image.load('Assets/blackKing.png')
wQueen = pygame.image.load('Assets/whiteQueen.png')
bQueen = pygame.image.load('Assets/blackQueen.png')
wBishop = pygame.image.load('Assets/whiteBishop.png')
bBishop = pygame.image.load('Assets/blackBishop.png')
wKnight = pygame.image.load('Assets/whiteKnight.png')
bKnight = pygame.image.load('Assets/blackKnight.png')
wRook = pygame.image.load('Assets/whiteRook.png')
bRook = pygame.image.load('Assets/blackRook.png')
wPawn = pygame.image.load('Assets/whitePawn.png')
bPawn = pygame.image.load('Assets/blackPawn.png')
chessMove = pygame.mixer.Sound('Assets/chessMove.wav')

pieces = {
    "wp": wPawn,
    "bp": bPawn,
    "wr": wRook,
    "br": bRook,
    "wb": wBishop,
    "bb": bBishop,
    "wn": wKnight,
    "bn": bKnight,
    "wq": wQueen,
    "bq": bQueen,
    "wk": wKing,
    "bk": bKing
}

previewColor = (214, 214, 189)
green = (118, 150, 86)
lightYellow = (238, 238, 210)

pos = [[[100 * i, 100 * j] for i in range(8)] for j in range(8)]
previewPos = [[[50 + 100 * i, 50 + 100 * j] for i in range(8)] for j in range(8)]

def main():
    count = 0
    global game, board, checking
    checking = False
    board = [[0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0]]
    game = [["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]

    drawBoard()

    while True:
        count += 1
        move = (-1)**count # -1 is white move, 1 is black move
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        whiteMove() if move < 0 else blackMove()
        check, checkmate, stalemate = mateCheck("w" if move < 0 else "b")

        if check:
            print(('white' if move < 0 else 'black') + ' check')
        
        if checkmate:
            endGame("w" if move < 0 else "b")

def drawBoard():
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                pygame.draw.rect(screen, lightYellow, pygame.Rect(pos[i][j][0], pos[i][j][1], 100, 100))
            elif board[i][j] == 0:
                pygame.draw.rect(screen, green, pygame.Rect(pos[i][j][0], pos[i][j][1], 100, 100)) 
            elif board[i][j] == 2:
                if game[i][j] == "--":
                    pygame.draw.rect(screen, green, pygame.Rect(pos[i][j][0], pos[i][j][1], 100, 100)) 
                    pygame.draw.circle(screen, previewColor, (previewPos[i][j][0], previewPos[i][j][1]), 7)
                else:
                    pygame.draw.rect(screen, green, pygame.Rect(pos[i][j][0], pos[i][j][1], 100, 100)) 
                    pygame.draw.circle(screen, previewColor, (previewPos[i][j][0], previewPos[i][j][1]), 45)
                    pygame.draw.circle(screen, green, (previewPos[i][j][0], previewPos[i][j][1]), 38)
            elif board[i][j] == 3:
                if game[i][j] == "--":
                    pygame.draw.rect(screen, lightYellow, pygame.Rect(pos[i][j][0], pos[i][j][1], 100, 100)) 
                    pygame.draw.circle(screen, previewColor, (previewPos[i][j][0], previewPos[i][j][1]), 7)
                else:
                    pygame.draw.rect(screen, lightYellow, pygame.Rect(pos[i][j][0], pos[i][j][1], 100, 100)) 
                    pygame.draw.circle(screen, previewColor, (previewPos[i][j][0], previewPos[i][j][1]), 45)
                    pygame.draw.circle(screen, lightYellow, (previewPos[i][j][0], previewPos[i][j][1]), 38)

    for i in range(8):
        for j in range(8):
            if game[i][j] != "--":
                screen.blit(pieces[game[i][j]], (pos[i][j][0], pos[i][j][1]))

    pygame.display.update()

def whiteMove():
    moveEnd = False
    resetBoard()

    while not moveEnd:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                column, row = click()
                if board[row][column] < 2:
                    resetBoard()
                    piece = game[row][column]
                    pieceRow = row
                    pieceColumn = column
                    whitePreview(row, column)
                    drawBoard()
                else: 
                    if piece == 'wp' and row == 0:
                        game[row][column] = "wq"
                        game[pieceRow][pieceColumn] = "--"
                    else:
                        game[row][column] = piece
                        game[pieceRow][pieceColumn] = "--"

                    resetBoard()
                    drawBoard()
                    chessMove.play()

                    moveEnd = True

def blackMove():
    moveEnd = False
    resetBoard()

    while not moveEnd:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                column, row = click()
                if board[row][column] < 2:
                    resetBoard()
                    piece = game[row][column]
                    pieceRow = row
                    pieceColumn = column
                    blackPreview(row, column)
                    drawBoard()
                else: 
                    if piece == 'bp' and row == 7:
                        game[row][column] = "bq"
                        game[pieceRow][pieceColumn] = "--"
                    else:
                        game[row][column] = piece
                        game[pieceRow][pieceColumn] = "--"

                    resetBoard()
                    drawBoard()
                    chessMove.play()

                    moveEnd = True

def resetBoard():
    global board
    board = [[0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0]]

def emptyBoard():
    global board
    board = [[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]]

def whitePreview(row, column):
    if game[row][column][0] == "w":
        piece = game[row][column][1]

        if piece == "p":
            if row == 6:
                if game[5][column] == "--":
                    if checking:
                        board[5][column] += 2
                    elif moveCheck((5, column), (row, column), 'wp'):
                        board[5][column] += 2

                    if game[4][column] == "--":
                        if checking:
                            board[4][column] += 2
                        elif moveCheck((4, column), (row, column), 'wp'):
                            board[4][column] += 2
            elif row > 0:
                if game[row - 1][column] == "--":
                    if checking:
                        board[row - 1][column] += 2
                    elif moveCheck((row - 1, column), (row, column), 'wp'):
                        board[row - 1][column] += 2
                        
            if column < 7 and row > 0:
                if game[row - 1][column + 1][0] == "b":
                    if checking:
                        board[row - 1][column + 1] += 2
                    elif moveCheck((row - 1, column + 1), (row, column), 'wp'): 
                        board[row - 1][column + 1] += 2
            if column > 0 and row > 0:
                if game[row - 1][column - 1][0] == "b":
                    if checking:
                        board[row - 1][column - 1] += 2
                    elif moveCheck((row - 1, column - 1), (row, column), 'wp'):
                        board[row - 1][column - 1] += 2
   
        elif piece == "r":
            crossMoves(row, column, "wr")
        elif piece == "b":
            diagonalMoves(row, column, "wb")
        elif piece == "n":
            knightMoves(row, column, "wn")
        elif piece == "q":
            crossMoves(row, column, "wq")
            diagonalMoves(row, column, "wq")
        elif piece == "k":
            for xMove in range(-1, 2):
                for yMove in range(-1, 2):
                    if not xMove == yMove == 0 and 0 <= row + yMove < 8 and 0 <= column + xMove < 8:
                        if game[row + yMove][column + xMove][0] != "w":
                            if checking:
                                board[row + yMove][column + xMove] += 2
                            elif moveCheck((row + yMove, column + xMove), (row, column), 'wk'):
                                board[row + yMove][column + xMove] += 2

def blackPreview(row, column):
    if game[row][column][0] == "b":
        piece = game[row][column][1]

        if piece == "p":
            if row == 1:
                if game[2][column] == "--":
                    if checking:
                        board[2][column] += 2
                    elif moveCheck((2, column), (row, column), 'bp'):
                        board[2][column] += 2

                    if game[3][column] == "--":
                        if checking:
                            board[3][column] += 2
                        if moveCheck((3, column), (row, column), 'bp'):
                            board[3][column] += 2
            elif row < 7:
                if game[row + 1][column] == "--":
                    if checking:
                        board[row + 1][column] += 2
                    elif moveCheck((row + 1, column), (row, column), 'bp'):
                        board[row + 1][column] += 2
                        
            if column < 7 and row < 7:
                if game[row + 1][column + 1][0] == "w":
                    if checking:
                        board[row + 1][column + 1] += 2
                    elif moveCheck((row + 1, column + 1), (row, column), 'bp'):
                        board[row + 1][column + 1] += 2
            if column > 0 and row < 7:
                if game[row + 1][column - 1][0] == "w":
                    if checking:
                        board[row + 1][column - 1] += 2
                    elif moveCheck((row + 1, column - 1), (row, column), 'bp'):
                        board[row + 1][column - 1] += 2
   
        elif piece == "r":
            crossMoves(row, column, "br")
        elif piece == "b":
            diagonalMoves(row, column, "bb")
        elif piece == "n":
            knightMoves(row, column, "bn")
        elif piece == "q":
            crossMoves(row, column, "bq")
            diagonalMoves(row, column, "bq")
        elif piece == "k":
            for xMove in range(-1, 2):
                for yMove in range(-1, 2):
                    if not xMove == yMove == 0 and 0 <= row + yMove < 8 and 0 <= column + xMove < 8:
                        if game[row + yMove][column + xMove][0] != "b":
                            if checking:
                                board[row + yMove][column + xMove] += 2
                            elif moveCheck((row + yMove, column + xMove), (row, column), 'bk'):
                                board[row + yMove][column + xMove] += 2

def crossMoves(row, column, piece):
    flag = False
    count = 0
    while not flag:
        count += 1
        if row + count < 8:
            if not checkSpace((row + count, column), (row, column), piece):
                flag = True
                colorCheck((row + count, column), (row, column), piece)
        else:
            flag = True

    flag = False
    count = 0
    while not flag:
        count += 1
        if row - count >= 0:
            if not checkSpace((row - count, column), (row, column), piece):
                flag = True
                colorCheck((row - count, column), (row, column), piece)
        else: 
            flag = True

    flag = False
    count = 0
    while not flag:
        count += 1
        if column + count < 8:
            if not checkSpace((row, column + count), (row, column), piece):
                flag = True
                colorCheck((row, column + count), (row, column), piece)
        else: 
            flag = True

    flag = False
    count = 0
    while not flag:
        count += 1
        if column - count >= 0:
            if not checkSpace((row, column - count), (row, column), piece):
                flag = True
                colorCheck((row, column - count), (row, column), piece)
        else:
            flag = True

def diagonalMoves(row, column, piece):
    flag = False
    count = 0
    while not flag:
        count += 1
        if row - count >= 0 and column - count >= 0:
            if not checkSpace((row - count, column - count), (row, column), piece):
                flag = True
                colorCheck((row - count, column - count), (row, column), piece)
        else:
            flag = True

    flag = False
    count = 0
    while not flag:
        count += 1
        if row - count >= 0 and column + count < 8:
            if not checkSpace((row - count, column + count), (row, column), piece):
                flag = True
                colorCheck((row - count, column + count), (row, column), piece)
        else:
            flag = True

    flag = False
    count = 0
    while not flag:
        count += 1
        if row + count < 8 and column + count < 8:
            if not checkSpace((row + count, column + count), (row, column), piece):
                flag = True
                colorCheck((row + count, column + count), (row, column), piece)
        else:
            flag = True

    flag = False
    count = 0
    while not flag:
        count += 1
        if row + count < 8 and column - count >= 0:
            if not checkSpace((row + count, column - count), (row, column), piece):
                flag = True
                colorCheck((row + count, column - count), (row, column), piece)
        else:
            flag = True

def knightMoves(row, column, piece):
    color = piece[0]
    if row + 2 < 8 and column + 1 < 8:
        checkSpace((row + 2, column + 1), (row, column), color + "n")
        colorCheck((row + 2, column + 1), (row, column), color + "n")
    if row + 2 < 8 and column - 1 >= 0:
        checkSpace((row + 2, column - 1), (row, column), color + "n")
        colorCheck((row + 2, column - 1), (row, column), color + "n")
    if row - 2 >= 0 and column + 1 < 8:
        checkSpace((row - 2, column + 1), (row, column), color + "n")
        colorCheck((row - 2, column + 1), (row, column), color + "n")
    if row - 2 >= 0 and column - 1 >= 0:
        checkSpace((row - 2, column - 1), (row, column), color + "n")
        colorCheck((row - 2, column - 1), (row, column), color + "n")
    if row + 1 < 8 and column + 2 < 8:
        checkSpace((row + 1, column + 2), (row, column), color + "n")
        colorCheck((row + 1, column + 2), (row, column), color + "n")
    if row + 1 < 8 and column - 2 >= 0:
        checkSpace((row + 1, column - 2), (row, column), color + "n")
        colorCheck((row + 1, column - 2), (row, column), color + "n")
    if row - 1 >= 0 and column + 2 < 8:
        checkSpace((row - 1, column + 2), (row, column), color + "n")
        colorCheck((row - 1, column + 2), (row, column), color + "n")
    if row - 1 >= 0 and column - 2 >= 0:
        checkSpace((row - 1, column - 2), (row, column), color + "n")
        colorCheck((row - 1, column - 2), (row, column), color + "n")

def checkSpace(coords, prevCoords, piece):
    if game[coords[0]][coords[1]] == "--":
        if checking:
            board[coords[0]][coords[1]] += 2
            return True
        elif moveCheck(coords, prevCoords, piece):
            board[coords[0]][coords[1]] += 2
            return True
    return False
    
def colorCheck(coords, prevCoords, piece):
    opposite = 'b' if piece[0] == 'w' else 'w'
    if game[coords[0]][coords[1]][0] == opposite:
        if checking:
            board[coords[0]][coords[1]] += 2
        elif moveCheck(coords, prevCoords, piece):
            board[coords[0]][coords[1]] += 2

def checkCheck(color):
    global checking, board
    check = False 
    checking = True
    opposite = "b" if color == "w" else "w"
    tempBoard = [[board[i][j] for i in range(8)] for j in range(8)]

    emptyBoard()
    for i in range(8):
        for j in range(8):
            whitePreview(i, j) if color == "w" else blackPreview(i, j)
    
    for i in range(8):
        for j in range(8):
            if game[i][j] == opposite + "k" and board[i][j] >= 2:
                check = True

    board = [[tempBoard[i][j] for i in range(8)] for j in range(8)]
    checking = False
    return check

def mateCheck(color):
    global board, game
    check = checkCheck(color)
    checkmate = False
    stalemate = False
    opposite = "b" if color == "w" else "w"
    currentGame = [[game[i][j] for i in range(8)] for j in range(8)]

    if check:
        checkmate = True
        for row in range(8):
            for column in range(8):
                emptyBoard()
                nextMove = []
                if game[row][column][0] == opposite and checkmate:
                    piece = game[row][column]
                    whitePreview(row, column) if color == "b" else blackPreview(row, column)

                    for tempRow in range(8):
                        for tempColumn in range(8):
                            if board[tempRow][tempColumn] == 2:
                                nextMove.append((tempRow, tempColumn))

                    for coords in nextMove:
                        game[coords[0]][coords[1]] = piece
                        game[row][column] = "--"

                        if not checkCheck(color):
                            checkmate = False

                        game = [[currentGame[i][j] for i in range(8)] for j in range(8)]
                        emptyBoard()

    resetBoard()
    return check, checkmate, stalemate

def moveCheck(coords, prevCoords, piece):
    global game
    tempGame = [[game[i][j] for i in range(8)] for j in range(8)]
    opposite = 'b' if piece[0] == 'w' else 'w'

    game[coords[0]][coords[1]] = piece
    game[prevCoords[0]][prevCoords[1]] = '--'

    possible_move = not checkCheck(opposite)
    game = [[tempGame[i][j] for i in range(8)] for j in range(8)]

    return possible_move

def endGame(victor):
    print(('white' if victor == 'w' else 'black') + ' wins')

def click():
    mouse = pygame.mouse.get_pos()
    return mouse[0]//100, mouse[1]//100

def printList(list):
    for row in list:
        print(row)

if __name__ == "__main__":
    main()