import sys, random
from PyQt5.QtWidgets import *

import ChoiceWindow


class GameState:
    def __init__(self):
        # 2D board contained in 8x8 list
        # First character represents the color: b - black, w - white
        # Second character represents the type of piece: P - pawn, R - rook, N - knight, B - bishop, Q - queen, K - king
        # -- represents empty field on the board
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]

        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whitePieces = ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wR', 'wN', 'wB', 'wQ', 'wB', 'wN', 'wR']
        self.blackPieces = ['bR', 'bN', 'bB', 'bQ', 'bB', 'bN', 'bR', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP']

        self.whiteMove = True
        self.moveLog = []   # Probably unnecessary for us
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.beginning = True

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'

        if self.board[move.endRow][move.endCol] != '--':
            if self.whiteMove:
                self.blackPieces.remove(self.board[move.endRow][move.endCol])
            else:
                self.whitePieces.remove(self.board[move.endRow][move.endCol])

        self.board[move.endRow][move.endCol] = move.pieceMoved

        self.moveLog.append(move)   # Probably unnecessary for us
        self.whiteMove = not self.whiteMove    # Swap players

        # Update the king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # Pawn promotion
        if move.isPawnPromotion:
            app = QApplication(sys.argv)
            w = ChoiceWindow.ChoiceWindow()
            w.show()
            app.exec_()

            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + w.chosen
            if not self.whiteMove:
                self.whitePieces.remove('wP')
                self.whitePieces.append('w' + w.chosen)
            else:
                self.blackPieces.remove('bP')
                self.blackPieces.append('b' + w.chosen)

    def undoMove(self):
        if len(self.moveLog) != 0:      # Make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteMove = not self.whiteMove     # Switch turns back
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.endRow, move.endCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.endRow, move.endCol)

    def drawBlackPieces(self):
        random.shuffle(self.blackPieces)
        index = 0

        for i in range(8):
            for j in range(8):
                if self.board[i][j][0] == 'b':
                    if self.board[i][j][1] != 'K':
                        self.board[i][j] = self.blackPieces[index]
                        index += 1

    def drawWhitePieces(self):
        random.shuffle(self.whitePieces)
        index = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j][0] == 'w':
                    if self.board[i][j][1] != 'K':
                        self.board[i][j] = self.whitePieces[index]
                        index += 1

    def getValidMoves(self):
        # Randomize piece position on beginning and after each player's move
        if self.beginning:
            self.drawWhitePieces()
            self.drawBlackPieces()
            self.beginning = False
        else:
            if self.whiteMove:
                self.drawBlackPieces()
            else:
                self.drawWhitePieces()

        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:  # Either checkmate or stalemate
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()

        if len(moves) == 0:
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True

        return moves

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if ((0<= j <= 3) and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'P' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <=5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

    def getAllPossibleMoves(self):
        moves = []

        for r in range(len(self.board)):    # Number of rows
            for c in range(len(self.board[r])):     # Number of columns in a row
                currentPlayerColor = self.board[r][c][0]
                if (currentPlayerColor == 'w' and self.whiteMove) or (currentPlayerColor == 'b' and not self.whiteMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)      # Call the appropriate move function based on piece type

        return moves

    # Get all the pawn moves for the pawn located at row, col and add these moves to the list
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whiteMove:  # White pawn moves
            if self.board[r - 1][c] == '--':  # One square pawn advance
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == '--':  # Two square pawn advance
                        moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # Captures to the left
                if self.board[r - 1][c - 1][0] == 'b':  # Enemy piece to capture
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # Captures to the right
                if self.board[r - 1][c + 1][0] == 'b':  # Enemy piece to capture
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:  # Black pawn moves
            if r < 7:  # Added to fix index out of range error
                if self.board[r + 1][c] == '--':  # One square pawn advance
                    if not piecePinned or pinDirection == (1, 0):
                        moves.append(Move((r, c), (r + 1, c), self.board))
                        if r == 1 and self.board[r + 2][c] == '--':  # Two square pawn advance
                            moves.append(Move((r, c), (r + 2, c), self.board))
                if c - 1 >= 0:  # Captures to the left
                    if self.board[r + 1][c - 1][0] == 'w':  # Enemy piece to capture
                        if not piecePinned or pinDirection == (1, -1):
                            moves.append(Move((r, c), (r + 1, c - 1), self.board))
                if c + 1 <= 7:  # Captures to the right
                    if self.board[r + 1][c + 1][0] == 'w':  # Enemy piece to capture
                        if not piecePinned or pinDirection == (1, 1):
                            moves.append(Move((r, c), (r + 1, c + 1), self.board))

        # Get all the rook moves for the rook located at row, col and add these moves to the list

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        if self.whiteMove:
            enemyColor = "b"
        else:
            enemyColor = "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

        # Get all the knight moves for the knight located at row, col and add these moves to the list

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = 'w' if self.whiteMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:  # Not an ally piece (empty or enemy)
                        moves.append(Move((r, c), (endRow, endCol), self.board))

        # Get all the bishop moves for the bishop located at row, col and add these moves to the list

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        if self.whiteMove:
            enemyColor = "b"
        else:
            enemyColor = "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

        # Get all the queen moves for the queen located at row, col and add these moves to the list

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

        # Get all the king moves for the king located at row, col and add these moves to the list

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        if self.whiteMove:
            allyColor = "w"
        else:
            allyColor = "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)

class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSquare, endSquare, currentBoardState):
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = currentBoardState[self.startRow][self.startCol]
        self.pieceCaptured = currentBoardState[self.endRow][self.endCol]
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7):
            self.isPawnPromotion = True
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + "->" + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, column):
        return self.colsToFiles[column] + self.rowsToRanks[row]
