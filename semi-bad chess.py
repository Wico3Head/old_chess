import pygame, sys
pygame.init()

screenWidth, screenHeight = 800, 800
screen = pygame.display.set_mode((screenWidth, screenHeight))
font = pygame.font.SysFont("Courier", 30)
pygame.display.set_caption("Ches")

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
    global game, board
    gameOver = False
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
            if event.type == pygame.QUIT or (gameOver and event.type == pygame.MOUSEBUTTONDOWN):
                pygame.quit()
                sys.exit()

        if not gameOver:
            whiteMove() if move < 0 else blackMove()
            
            check, checkmate = mateCheck("w" if move < 0 else "b")

            if check:
                print("check")
            
            if checkmate:
                print("checkmate")

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
                if board[row][column] == 0 or board[row][column] == 1:
                    resetBoard()
                    piece = game[row][column]
                    pieceRow = row
                    pieceColumn = column
                    whitePreview(row, column)
                    drawBoard()
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
                if board[row][column] == 0 or board[row][column] == 1:
                    resetBoard()
                    piece = game[row][column]
                    pieceRow = row
                    pieceColumn = column
                    blackPreview(row, column)
                    drawBoard()
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
                if game[5][column] == "--" and board[5][column] < 2:
                    board[5][column] += 2
                    if game[4][column] == "--" and board[4][column] < 2:
                        board[4][column] += 2
            elif row > 0:
                if game[row - 1][column] == "--" and board[row - 1][column] < 2:
                    board[row - 1][column] += 2
                        
            if column < 7:
                if game[row - 1][column + 1][0] == "b" and board[row - 1][column + 1] < 2: 
                    board[row - 1][column + 1] += 2
            if column > 0:
                if game[row - 1][column - 1][0] == "b" and board[row - 1][column - 1] < 2:
                    board[row - 1][column - 1] += 2
   
        elif piece == "r":
            crossMoves(row, column, "b")
        elif piece == "b":
            diagonalMoves(row, column, "b")
        elif piece == "n":
            knightMoves(row, column, "b")
        elif piece == "q":
            crossMoves(row, column, "b")
            diagonalMoves(row, column, "b")
        elif piece == "k":
            for xMove in range(-1, 2):
                for yMove in range(-1, 2):
                    if not xMove == yMove == 0 and 0 <= row + yMove < 8 and 0 <= column + xMove < 8:
                        if game[row + yMove][column + xMove][0] != "w" and board[row + yMove][column + xMove] < 2:
                            board[row + yMove][column + xMove] += 2

def blackPreview(row, column):
    if game[row][column][0] == "b":
        piece = game[row][column][1]

        if piece == "p":
            if row == 1:
                if game[2][column] == "--" and board[2][column] < 2:
                    board[2][column] += 2
                    if game[3][column] == "--" and board[3][column] < 2:
                        board[3][column] += 2
            elif row < 7:
                if game[row + 1][column] == "--" and board[row + 1][column] < 2:
                    board[row + 1][column] += 2
                        
            if column < 7:
                if game[row + 1][column + 1][0] == "w" and board[row + 1][column + 1] < 2:
                    board[row + 1][column + 1] += 2
            if column > 0:
                if game[row + 1][column - 1][0] == "w" and board[row + 1][column - 1] < 2:
                    board[row + 1][column - 1] += 2
   
        elif piece == "r":
            crossMoves(row, column, "w")
        elif piece == "b":
            diagonalMoves(row, column, "w")
        elif piece == "n":
            knightMoves(row, column, "w")
        elif piece == "q":
            crossMoves(row, column, "w")
            diagonalMoves(row, column, "w")
        elif piece == "k":
            for xMove in range(-1, 2):
                for yMove in range(-1, 2):
                    if not xMove == yMove == 0 and 0 <= row + yMove < 8 and 0 <= column + xMove < 8:
                        if game[row + yMove][column + xMove][0] != "b" and board[row + yMove][column + xMove] < 2:
                            board[row + yMove][column + xMove] += 2

def crossMoves(row, column, color):
    flag = False
    count = 0
    while not flag:
        count += 1
        if row + count < 8:
            if not checkSpace(row + count, column):
                flag = True
                colorCheck(row + count, column, color)
        else:
            flag = True

    flag = False
    count = 0
    while not flag:
        count += 1
        if row - count >= 0:
            if not checkSpace(row - count, column):
                flag = True
                colorCheck(row - count, column, color)
        else: 
            flag = True

    flag = False
    count = 0
    while not flag:
        count += 1
        if column + count < 8:
            if not checkSpace(row, column + count):
                flag = True
                colorCheck(row, column + count, color)
        else: 
            flag = True

    flag = False
    count = 0
    while not flag:
        count += 1
        if column - count >= 0:
            if not checkSpace(row, column - count):
                flag = True
                colorCheck(row, column - count, color)
        else:
            flag = True

def diagonalMoves(row, column, color):
    flag = False
    count = 0
    while not flag:
        count += 1
        if row - count >= 0 and column - count >= 0:
            if not checkSpace(row - count, column - count):
                flag = True
                colorCheck(row - count, column - count, color)
        else:
            flag = True

    flag = False
    count = 0
    while not flag:
        count += 1
        if row - count >= 0 and column + count < 8:
            if not checkSpace(row - count, column + count):
                flag = True
                colorCheck(row - count, column + count, color)
        else:
            flag = True

    flag = False
    count = 0
    while not flag:
        count += 1
        if row + count < 8 and column + count < 8:
            if not checkSpace(row + count, column + count):
                flag = True
                colorCheck(row + count, column + count, color)
        else:
            flag = True

    flag = False
    count = 0
    while not flag:
        count += 1
        if row + count < 8 and column - count >= 0:
            if not checkSpace(row + count, column - count):
                flag = True
                colorCheck(row + count, column - count, color)
        else:
            flag = True

def knightMoves(row, column, color):
    if row + 2 < 8 and column + 1 < 8:
        checkSpace(row + 2, column + 1)
        colorCheck(row + 2, column + 1, color)
    if row + 2 < 8 and column - 1 >= 0:
        checkSpace(row + 2, column - 1)
        colorCheck(row + 2, column - 1, color)
    if row - 2 >= 0 and column + 1 < 8:
        checkSpace(row - 2, column + 1)
        colorCheck(row - 2, column + 1, color)
    if row - 2 >= 0 and column - 1 >= 0:
        checkSpace(row - 2, column - 1)
        colorCheck(row - 2, column - 1, color)
    if row + 1 < 8 and column + 2 < 8:
        checkSpace(row + 1, column + 2)
        colorCheck(row + 1, column + 2, color)
    if row + 1 < 8 and column - 2 >= 0:
        checkSpace(row + 1, column - 2)
        colorCheck(row + 1, column - 2, color)
    if row - 1 >= 0 and column + 2 < 8:
        checkSpace(row - 1, column + 2)
        colorCheck(row - 1, column + 2, color)
    if row - 1 >= 0 and column - 2 >= 0:
        checkSpace(row - 1, column - 2)
        colorCheck(row - 1, column - 2, color)

def checkSpace(row, column):
    if game[row][column] == "--":
        if board[row][column] < 2:
            board[row][column] += 2
        return True
    return False

def checkCheck(color):
    check = False
    opposite = "b" if color == "w" else "w"

    emptyBoard()
    for i in range(8):
        for j in range(8):
            whitePreview(i, j) if color == "w" else blackPreview(i, j)
    
    for i in range(8):
        for j in range(8):
            if game[i][j] == opposite + "k" and board[i][j] == 2:
                check = True

    resetBoard()
    return check

def mateCheck(color):
    global board, game
    check = checkCheck(color)
    checkmate = False
    stalement = False
    opposite = "b" if color == "w" else "w"

    if check:
        checkmate = True
        currentGame = [[game[i][j] for i in range(8)] for j in range(8)]
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

    return check, checkmate

def colorCheck(row, column, color):
    if game[row][column][0] == color and board[row][column] < 2:
        board[row][column] += 2

def gameOver(color):
    global stop
    stop = True
    print(color + " wins")

def click():
    mouse = pygame.mouse.get_pos()
    return mouse[0]//100, mouse[1]//100

if __name__ == "__main__":
    main()