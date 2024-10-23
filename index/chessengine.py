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
        self.moveFunctions = {
            'p':self.getPawnMoves,
            'N':self.getKnightMoves,
            'B':self.getBishopMoves,
            'R':self.getRookMoves,
            'Q':self.getQueenMoves,
            'K':self.getKingMoves
        } 
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False


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
        #1. Generate all possible moves
        moves = self.getAllPossibleMoves()
        #2. for each move , make the move
        for i in range(len(moves)-1, -1, -1):#when removing from a list go backwards through that list
            self.makeMove(moves[i])
            #3. generate all opponents move
            #4. for each of your opponents moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        #5. if they do attack your king, not a valid move
        return moves
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
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == '--': # One square advance
                moves.append(Move((r, c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == '--':# Two square advance
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: # capture left
                if self.board[r-1][c-1][0] == 'b': #enemy piece
                    moves.append(Move((r,c), (r-1,c-1), self.board))
            if c+1 <= 7: # capture right
                if self.board[r-1][c+1][0] == 'b': #enemy piece
                    moves.append(Move((r,c), (r-1,c+1), self.board))
        else: # black pawn moves
            if self.board[r+1][c] == '--': #one square advance
                moves.append(Move((r,c), (r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == '--': #two square advance
                    moves.append(Move((r,c), (r+2,c), self.board))
            if c+1 <=7: # capture left
                if self.board[r+1][c+1][0] == 'w': #enemy capture
                    moves.append(Move((r,c), (r+1,c+1), self.board))
            if c-1 >=0: #capture right:
                if self.board[r+1][c-1][0] == 'w': #enemy capture
                    moves.append(Move((r,c), (r+1,c-1), self.board))
    
    '''
    All posible moves of Rook.
    '''                
    def getRookMoves(self, r, c, moves):
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
    All posibile moves of Knight
    '''       
    def getKnightMoves(self, r, c, moves):
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
                endPiece = self.board[endRow][endCol]
                if endPiece[0] !=  allyColor:
                    moves.append(Move((r,c), (endRow,endCol), self.board))
                
    '''
    All posible Kings moves
    '''                            
    def getKingMoves(self, r, c, moves):
        # All moves of a king one step at all direction
        kingsmove = (
            (-1,0),
            (-1,1),
            (0,1),
            (1,1),
            (1,0),
            (1,-1),
            (0,-1),
            (-1,-1)
                    )
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + kingsmove[i][0]
            endCol = c + kingsmove[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol] 
                if endPiece[0] !=  allyColor:
                    moves.append(Move((r,c), (endRow,endCol), self.board)) 
                            
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