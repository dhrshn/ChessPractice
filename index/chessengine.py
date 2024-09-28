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
    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)# log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swamp player
        '''
        makeMove takes a move as a perameter and executes it (this will not work for castling, pawn promotion, and en-passant)
        '''
        
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #swaps players
            '''
            Undo the last move
            '''
            
    def getValidMoves(self):
        return self.getAllPossibleMoves()
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
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
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
                              
    def getBishopMoves(self, r, c, moves):
        pass                    
    def getKnightMoves(self, r, c, moves):
        pass                    
    def getKingMoves(self, r, c, moves):
        pass                    
    def getQueenMoves(self, r, c, moves):
        pass                    
                    
class Move():
    
    ranksToRows = {'1':7, '2':6, '3':5, '4':4,
                   '5':3, '6':2, '7':1, '8':0,}
    rowsToRanks = {v: k for k,v in ranksToRows.items()}
    
    filesToCols = {'a':0, 'b':1, 'c':2, 'd':3, 
                   'e':4, 'f':5, 'g':6, 'h':7}
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