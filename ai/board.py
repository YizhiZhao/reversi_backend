from __future__ import print_function

class Board():
    # List of all 8 directions on the Reversi, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self, rawBoard):
        self.pieces = [None]*8
        for i in range(8):
            self.pieces[i] = [0]*8
        for j in range(64):
            if rawBoard[j] == 'ai':
                self.pieces[j//8][j%8] = 1
            elif rawBoard[j] == 'cat':
                self.pieces[j//8][j%8] = -1


    # Add [][] indexer syntax to the Reversi
    def __getitem__(self, index):
        return self.pieces[index]

    def count(self, color):
        count = 0
        for y in range(8):
            for x in range(8):
                if self[x][y]==color:
                    count += 1
        return count

    def get_squares(self, color):
        squares=[]
        for y in range(8):
            for x in range(8):
                if self[x][y]==color:
                    squares.append((x,y))
        return squares

    def get_legal_moves(self, color):
        if color!=1 and color!=-1:
            return []
        moves = set()
        for square in self.get_squares(color):
            # Find all moves using these pieces as base squares.
            newmoves = self._get_moves_for_square(square)
            moves.update(newmoves)
        return list(moves)

    def _get_moves_for_square(self, square):
        (x,y) = square
        color = self[x][y]

        # Skip empty source squares
        if color==0:
            return None

        # Search all possible directions
        moves = []
        for direction in self.__directions:
            move = self._discover_move(square, direction)
            if move:
                moves.append(move)
        return moves

    def execute_move(self, move, color):
        flips = (flip for direction in self.__directions
                      for flip in self._get_flips(move, direction, color))

        for x,y in flips:
            self[x][y] = color

    def _discover_move(self, origin, direction):
        x,y = origin
        color = self[x][y]
        flips = []

        for x,y in Board._increment_move(origin, direction):
            if self[x][y] == 0 and flips:
                return (x,y)
            elif (self[x][y] == color or (self[x][y] == 0 and not flips)):
                return None
            elif self[x][y] == -color:
                flips.append((x,y))

    def _get_flips(self, origin, direction, color):
        flips = [origin]

        for x, y in Board._increment_move(origin, direction):
            if self[x][y] == -color:
                flips.append((x, y))
            elif (self[x][y] == 0 or (self[x][y] == color and len(flips) == 1)):
                break
            elif self[x][y] == color and len(flips) > 1:
                return flips
        return []

    @staticmethod
    def _increment_move(move, direction):
        move = list(map(sum, zip(move, direction)))
        while all(list(map(lambda x: 0 <= x < 8, move))):
            yield move
            move = list(map(sum, zip(move, direction)))