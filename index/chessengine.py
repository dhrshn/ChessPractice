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
                    # if piece == 'p':
                    #     self.getPawnMoves(r, c, moves)
                    # elif piece == 'R':
                    #     self.getRookMoves(r, c, moves)
                    # elif piece == 'B':
                    #     self.getBishopMoves(r, c, moves)
                    # elif piece == 'N':
                    #     self.getKnightMoves(r, c, moves)
                    # elif piece == 'K':
                    #     self.getKingMoves(r, c, moves)
                    # elif piece == 'Q':
                    #     self.getQueenMoves(r, c, moves)
                    self.moveFunctions[piece](r, c, moves)
        return moves
                    
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == '--': # One square advance
                moves.append(Move((r, c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == '--':# Two square advance
                    moves.append(Move((r, c), (r-2, c), self.board))
    def getRookMoves():
        pass                    
    def getBishopMoves():
        pass                    
    def getKnightMoves():
        pass                    
    def getKingMoves():
        pass                    
    def getQueenMoves():
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
        print(self.moveID)
        
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