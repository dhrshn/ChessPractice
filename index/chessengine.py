""" 
This class is responsible for storing all the information about the current state
 of a chess game. It will also be responsible for the valid moves at the current state.
It will also keep a move log.
"""

class GameState():
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.whiteToMove = True
        self.moveLog = []

        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []


        self.moveFunctions = {
            'p':self.getPawnMoves,
            'N':self.getKnightMoves,
            'B':self.getBishopMoves,
            'R':self.getRookMoves,
            'Q':self.getQueenMoves,
            'K':self.getKingMoves
        }   


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)# log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swamp player
        #update the kings location if moved
        if move.pieceMoved == "wk":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        '''
        makeMove takes a move as a perameter and executes it (this will not work for castling, pawn promotion, and en-passant)
        '''
        
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #swaps players
            #update the kings location if moved
        if move.pieceMoved == "wk":
            self.whiteKingLocation = (move.startRow, move.startCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.startRow, move.startCol)
            '''
            Undo the last move
            '''
            
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.inCheck:
            if len(self.checks) == 1: #only check, block check or move king
                #to block a check you must move a piece into one of the squares between the enemy piece and king
                check = self.checks[0]# check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] #enemy piece causing the check
                validSquares = [] #squares that pieces can move to
                #if knight, must capture knight or move king, other pieces can be blocked
                if pieceChecking[1]== 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3]*i) #check[2] and check[3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: #once you get to piece and checks 
                            break
                    #get rid of any moves that dont block the check or move king
                    for i in range(len(moves) -1, -1, -1): #go through backwards when you are removing from a list iterating
                        if moves[i].pieceMoved[1] != 'K':#move doesnt move king so it must block or capture
                            if not (moves[i].endRow, moves[i].endCol) in validSquares: #move doesnt block check or capture piece
                                moves.remove(moves[i])
            else: #double check king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else: #not in check soo all moves are fine
            moves = self.getAllPossibleMoves()
        
        return moves
    


    def checkForPinsAndChecks(self):
        pins = [] #squares where the allied pinned piece is and direction pinned from
        checks = [] #squares where enemy is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        #check outward from king for pins and checks, keep track of pins
        #directions are left up right down / up-left up-right down-left down-right
        directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1))
        for j in range(8):
            d = directions[j]
            possiblePin = () #reset possible pins
            for i in range(1,8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':                                                    
                        if possiblePin == (): #1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: #2nd allied piece, so no pin or check in this directon
                            break
                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]
                        # 5 possibility here in this complex conditional 
                        #1. orthogonally away from king and piece is a rook
                        #2. diagonally away from king and piece is a bishop
                        #3. 1 square away diagonally from king and piece is a pawn
                        #4. any direction and piece is a queen
                        #5. any direction 1 square away and piece is king (this is necessary to prevent a king move to a square controlled by another king)
                        if (0 <= j <= 3 and pieceType =="R") or \
                                (4 <= j <= 7 and pieceType == "B") or\
                                (i == 1 and pieceType == "p" and ((enemyColor == "w" and 6 <= j <= 7) or (enemyColor == "b" and 4 <= j <= 5))) or\
                                (pieceType == "Q") or (i == 1 and pieceType == "K"):
                            if possiblePin == (): #no piece blocking, so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: #piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else: #enemy piece not applying check
                            break
                else: # off board
                    break
        # check for knight  checks
        knightMoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,2), (2,-1), (2,1))
        for m in knightMoves:
            endRow = startRow + m[0] 
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == "N": #eneemy knight attacking knig
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return inCheck, pins, checks


    """
    Determine if the current player is in check
    """            
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1]) 

    """
    Determime if the enemy attack can attack the square r, c
    """
    def squareUnderAttack(self, r, c):
        self.whiteToMove =  not self.whiteToMove #switch to opponents move
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch turns back
        for move in oppMoves:
            if move.endRow ==  r and move.endCol == c: #square is under attack   
                # self.whiteToMove = not self.whiteToMove #switch turn back
                return True
        return False


    '''
    All moves considering checks
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]     
                    self.moveFunctions[piece](r, c, moves)             
        return moves
    
    '''
    All posible moves of Pawn.
    '''                
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break 
                
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == '--': # One square advance
                if not  piecePinned or pinDirection == (-1,0):    
                    moves.append(Move((r, c), (r-1,c), self.board))
                    if r == 6 and self.board[r-2][c] == '--':# Two square advance
                        moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: # capture left
                if self.board[r-1][c-1][0] == 'b': #enemy piece
                    if not  piecePinned or pinDirection == (1,-1):
                        moves.append(Move((r,c), (r-1,c-1), self.board))
            if c+1 <= 7: # capture right
                if self.board[r-1][c+1][0] == 'b': #enemy piece
                    if not  piecePinned or pinDirection == (-1,-1):
                        moves.append(Move((r,c), (r-1,c+1), self.board))

        else: # black pawn moves
            if self.board[r+1][c] == '--': #one square advance
                if not  piecePinned or pinDirection == (-1,0):
                    moves.append(Move((r,c), (r+1,c), self.board))
                    if r == 1 and self.board[r+2][c] == '--': #two square advance
                        moves.append(Move((r,c), (r+2,c), self.board))
            if c+1 <=7: # capture left
                if self.board[r+1][c+1][0] == 'w': #enemy capture
                    if not  piecePinned or pinDirection == (1,-1):
                        moves.append(Move((r,c), (r+1,c+1), self.board))
            if c-1 >=0: #capture right:
                if self.board[r+1][c-1][0] == 'w': #enemy capture
                    if not  piecePinned or pinDirection == (1,1):
                        moves.append(Move((r,c), (r+1,c-1), self.board))
    
    '''
    All posible moves of Rook.
    '''                
    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':# cant remove queen on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        #directions up down left right
        directions = ((-1, 0),
                      (1, 0),
                      (0, -1),
                      (0, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # end boundary of board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--': # move to an empty space
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                        elif endPiece[0] == enemyColor: # capture enemy piece
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                            break
                        else:
                            break # frendlly piece in the way so we cant check that direction
                else:
                    break # we cant go out of the board

    '''
    All posible moves of Bishop
    '''                              
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        #directions diaoganaly up-right, diaoganaly up-left, diaoganaly down-right, diaoganaly down-left 
        directions = ((-1,1),
                      (-1,-1),
                      (1,1),
                      (1,-1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # end boundary of board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--': # move to an empty space
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                        elif endPiece[0] == enemyColor: # capture enemy piece
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                            break
                        else:
                            break # friendlly piece in the way so we cant check that direction
                else:
                    break # we cant go out of the board
                
    '''
    All posibile moves of Knight
    '''       
    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        # directions of knight moves: up->right,left; right->up,down; down->right,left; left->up,down 
        knmoves = (
            (-2,-1),
            (-2,1),
            (-1,2),
            (1,2),
            (2,1),
            (2,-1),
            (-1,-2),
            (1,-2)
                )   
        allyColor = 'w' if self.whiteToMove else 'b'
        for k in knmoves:
            endRow = r + k[0]
            endCol = c + k[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] !=  allyColor:
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                
    '''
    All posible Kings moves
    '''                            
    def getKingMoves(self, r: int, c: int, moves: list) -> None:
        """Get all possible king moves for a given square."""
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            end_row = r + rowMoves[i]
            end_col = c + colMoves[i]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    # Set king location immediately
                    self.white_king_location = (end_row, end_col) if ally_color == 'w' else (r, c)
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    '''
    All posible Queen moves
    '''
    def getQueenMoves(self, r, c, moves):
        #queens moves are just the same moves as bishop and rook combined
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)       
        # directions =((-1,1),
        #              (-1,-1),
        #              (1,1),
        #              (1,-1),
        #              (-1, 0),
        #              (1, 0),
        #              (0, -1),
        #              (0, 1))
        # enemyColor = 'b' if self.whiteToMove else 'w'
        # for d in directions:
        #     for i in range(1,8):
        #         endRow = r + d[0] * i
        #         endCol = c + d[1] * i
        #         if 0 <= endRow < 8 and 0 <= endCol < 8: # end boundary of board
        #             endPiece = self.board[endRow][endCol]
        #             if endPiece == '--': # move to an empty space
        #                 moves.append(Move((r,c), (endRow,endCol), self.board))
        #             elif endPiece[0] == enemyColor: # capture enemy piece
        #                 moves.append(Move((r,c), (endRow,endCol), self.board))
        #                 break
        #             else:
        #                 break # frendlly piece in the way so we cant check that direction
        #         else:
        #             break # we cant go out of the board
        
                    
class Move():
    
    ranksToRows = {'1':7,
                   '2':6,
                   '3':5,
                   '4':4,
                   '5':3,
                   '6':2,
                   '7':1,
                   '8':0,}
    rowsToRanks = {v: k for k,v in ranksToRows.items()}
    
    filesToCols = {'a':0,
                   'b':1,
                   'c':2,
                   'd':3, 
                   'e':4,
                   'f':5,
                   'g':6,
                   'h':7}
    colsToFiles = {v: k for k,v in filesToCols.items()}
    # maps keys to values
    # key : values
    
    def __init__(self, startSq,endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7):
            self.isPawnPromotion = True
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        # print(self.moveID)
        
    # overriding the equal method
    def  __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
        
    def getChessNotation(self):
        #you can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c): 
        return self.colsToFiles[c] + self.rowsToRanks[r]