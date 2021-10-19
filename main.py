import pygame
import ChessEngine

WYSOKOSC = SZEROKOSC = 512
ILEPOL = 8
WIELKOSCPOLA = WYSOKOSC // ILEPOL
FIGURY = {}
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


def wczytywanieFigur():
    figury = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for figura in figury:
        FIGURY[figura] = pygame.image.load("Images/" + figura + ".png")

def main():
    pygame.init()
    screen = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Szachy')
    screen.fill(pygame.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False    # Flag variable for when a move is made
    wczytywanieFigur()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False

    while running:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if not gameOver:
                    loc = pygame.mouse.get_pos()
                    col = loc[0]//WIELKOSCPOLA
                    row = loc[1]//WIELKOSCPOLA
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2 and playerClicks[0] != ():
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False

        if moveMade:
            animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False

        stanGry(screen, gs, validMoves, sqSelected)

        if gs.checkmate == True:
            gameOver = True
            if gs.whiteMove:
                drawText(screen, 'Black wins by checkmate', WYSOKOSC)
                drawText(screen, 'Press "r" key to restart the game', WYSOKOSC + 50)
            else:
                drawText(screen, 'White wins by checkmate', WYSOKOSC)
                drawText(screen, 'Press "r" key to restart the game', WYSOKOSC + 50)
        elif gs.stalemate == True:
            gameOver = True
            drawText(screen, 'Stalemate', WYSOKOSC)
            drawText(screen, 'Press "r" key to restart the game', WYSOKOSC + 50)

        clock.tick(15)
        pygame.display.flip()

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteMove else 'b'):     # sqSelected is a piece that can be moved
            # Highlight selected square
            s = pygame.Surface((WIELKOSCPOLA, WIELKOSCPOLA))
            s.set_alpha(100)    # Transparency value -> 0 transparent; 255 opaque
            s.fill(pygame.Color('blue'))
            screen.blit(s, (c * WIELKOSCPOLA, r * WIELKOSCPOLA))

            # Highlight moves from that square
            s.fill(pygame.Color('yellow'))

            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (WIELKOSCPOLA * move.endCol, WIELKOSCPOLA * move.endRow))

def stanGry(screen, gs, validMoves, sqSelected):
    tworzeniePlanszy(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    tworzenieFigur(screen, gs.board)

def tworzeniePlanszy(screen):
    global colors
    myfont = pygame.font.SysFont('constantia', 15)
    colors = [pygame.Color("gray"), pygame.Color("dark gray")]
    for w in range(ILEPOL):
        for s in range(ILEPOL):
            kolor = colors[((w+s) % 2)]
            pygame.draw.rect(screen, kolor, pygame.Rect(s*WIELKOSCPOLA, w*WIELKOSCPOLA,WIELKOSCPOLA,WIELKOSCPOLA))
            if w != 7:
                if s == 0:
                    textsurface = myfont.render(str(8 - w), True, (0, 0, 0))
                    screen.blit(textsurface,
                               pygame.Rect(s * WIELKOSCPOLA, w * WIELKOSCPOLA, WIELKOSCPOLA, WIELKOSCPOLA))
            else:
                if s == 0:
                    textsurface = myfont.render(str(8 - w), True, (0, 0, 0))
                    screen.blit(textsurface,
                               pygame.Rect(s * WIELKOSCPOLA, w * WIELKOSCPOLA, WIELKOSCPOLA, WIELKOSCPOLA))
                    textsurface = myfont.render(LETTERS[s], True, (0, 0, 0))
                    screen.blit(textsurface,
                               pygame.Rect(s * WIELKOSCPOLA + 55, w * WIELKOSCPOLA + 45, WIELKOSCPOLA, WIELKOSCPOLA))
                else:
                    textsurface = myfont.render(LETTERS[s], True, (0, 0, 0))
                    screen.blit(textsurface,
                               pygame.Rect(s * WIELKOSCPOLA + 55, w * WIELKOSCPOLA + 45, WIELKOSCPOLA, WIELKOSCPOLA))

def tworzenieFigur(screen, plansza):
    for w in range(ILEPOL):
        for s in range(ILEPOL):
            figura = plansza [w][s]
            if figura != "--":
                screen.blit(FIGURY[figura],pygame.Rect(s*WIELKOSCPOLA, w*WIELKOSCPOLA, WIELKOSCPOLA, WIELKOSCPOLA))

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount =(abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c =(move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        tworzeniePlanszy(screen)
        tworzenieFigur(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pygame.Rect(move.endCol * WIELKOSCPOLA, move.endRow*WIELKOSCPOLA, WIELKOSCPOLA, WIELKOSCPOLA)
        pygame.draw.rect(screen, color,endSquare)
        if move.pieceCaptured != '--':
            screen.blit(FIGURY[move.pieceCaptured], endSquare)
        screen.blit(FIGURY[move.pieceMoved], pygame.Rect(c*WIELKOSCPOLA, r*WIELKOSCPOLA, WIELKOSCPOLA, WIELKOSCPOLA))
        pygame.display.flip()
        clock.tick(60)

def drawText(screen, text, height):
    font = pygame.font.SysFont('constantia', 28, True, False)
    textObject = font.render(text, 0, pygame.Color('Black'))
    textLocation = pygame.Rect(0, 0, SZEROKOSC, WYSOKOSC).move(SZEROKOSC/2 - textObject.get_width()/2, height/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    #textObject = font.render(text, 0, pygame.Color('Black'))
    #screen.blit(textObject, textLocation.move(2, 2))


if __name__ == "__main__":
    main()