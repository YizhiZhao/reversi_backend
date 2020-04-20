class Evaluator():

    __board_weight = [[100, -3, 11, 8, 8, 11, -3, 100],
                             [-3, -7, -4, 1, 1, -4, -7, -3],
                             [11, -4, 2, 2, 2, 2, -4, 11],
                             [8, 1, 2, -3, -3, 2, 1, 8],
                             [8, 1, 2, -3, -3, 2, 1, 8],
                             [11, -4, 2, 2, 2, 2, -4, 11],
                             [-3, -7, -4, 1, 1, -4, -7, -3],
                             [100, -3, 11, 8, 5, 11, -3, 100]]
                             
    @staticmethod
    def evaluate(board, color, step_count, is_terminal):
        if is_terminal:
            my_count = board.count(color)
            op_count = board.count(-1 * color)
            if my_count > op_count:
                return 100000 + my_count
            elif my_count < op_count:
                return -100000 - op_count
            else:
                return 0
        else:
            if step_count < 30:
                return 1 * Evaluator._weight(board, color) \
                       - 10 * Evaluator._unstability_difference(board, color) \
                       - 5 * Evaluator._op_move_count(board, color) \
                       + 50 * Evaluator._stability_difference(board, color) \
                       - 5 * Evaluator._pices_difference(board, color)
            else:
                return 2 * Evaluator._weight(board, color) \
                       - 10 * Evaluator._unstability_difference(board, color) \
                       + 50 * Evaluator._stability_difference(board, color)

    @staticmethod
    def _weight(board, color):
        pieces = board.get_squares(color)
        op_pieces = board.get_squares(-1 * color)
        score = sum([Evaluator.__board_weight[x][y] for x, y in pieces]) - \
                sum([Evaluator.__board_weight[x][y] for x, y in op_pieces])
        return score

    @staticmethod
    def _unstability_difference(board, color):
        op_color = -1 * color
        my_unstable = op_unstable = 0
        if board[0][0] == 0:
            my_unstable += (board[0][1] == color) + (board[1][1] == color) + (board[1][0] == color)
            op_unstable += (board[0][1] == op_color) + (board[1][1] == op_color) + (board[1][0] == op_color)
        if board[0][7] == 0:
            my_unstable += (board[0][6] == color) + (board[1][6] == color) + (board[1][7] == color)
            op_unstable += (board[0][6] == op_color) + (board[1][6] == op_color) + (board[1][7] == op_color)
        if board[7][0] == 0:
            my_unstable += (board[7][1] == color) + (board[6][1] == color) + (board[6][0] == color)
            op_unstable += (board[7][1] == op_color) + (board[6][1] == op_color) + (board[6][0] == op_color)
        if board[7][7] == 0:
            my_unstable += (board[6][7] == color) + (board[6][6] == color) + (board[7][6] == color)
            op_unstable += (board[6][7] == op_color) + (board[6][6] == op_color) + (board[7][6] == op_color)
        return my_unstable - op_unstable

    @staticmethod
    def _stability_difference(board, color):
        def snake_index(rows, cols):
            n = rows
            m = cols
            count = 0
            while n > 1 and m > 1:
                for i in range(cols - count * 2 - 1):
                    yield count, count + i
                for j in range(rows - count * 2 - 1):
                    yield count + j, cols - count - 1
                for i in range(cols - count * 2 - 1):
                    yield rows - count - 1, cols - count - i - 1
                for j in range(rows - count * 2 - 1):
                    yield rows - count - j - 1, count
                n -= 2
                m -= 2
                count += 1
            if n == 1:
                for i in range(cols - count * 2):
                    yield count, count + i
            elif m == 1:
                for j in range(rows - count * 2):
                    yield count + j, count

        def get_stability_count(board, color):
            background = [[False for i in range(10)] for j in range(10)]
            for i in range(10):
                background[0][i] = True
                background[i][0] = True
                background[9][i] = True
                background[i][9] = True
            clockwise = snake_index(8, 8)
            anticlockwise = snake_index(8, 8)
            for i in range(7, 0, -2):
                for j in range(i * 4):
                    x, y = next(clockwise)
                    if board[x][y] == color:
                        x_b, y_b = x + 1, y + 1
                        if (background[x_b - 1][y_b] and background[x_b][y_b - 1]) or \
                                (background[x_b + 1][y_b] and background[x_b][y_b - 1]) or \
                                (background[x_b + 1][y_b] and background[x_b][y_b + 1]) or \
                                (background[x_b - 1][y_b] and background[x_b][y_b + 1]):
                            background[x_b][y_b] = True
                    y, x = next(anticlockwise)
                    if board[x][y] == color:
                        x_b, y_b = x + 1, y + 1
                        if (background[x_b - 1][y_b] and background[x_b][y_b - 1]) or \
                                (background[x_b + 1][y_b] and background[x_b][y_b - 1]) or \
                                (background[x_b + 1][y_b] and background[x_b][y_b + 1]) or \
                                (background[x_b - 1][y_b] and background[x_b][y_b + 1]):
                            background[x_b][y_b] = True
            return sum([sum(line) for line in background]) - 36

        return get_stability_count(board, color) - get_stability_count(board, -1 * color)

    @staticmethod
    def _pices_difference(board, color):
        return len(board.get_squares(color)) - len(board.get_squares(-1 * color))

    @staticmethod
    def _op_move_count(board, color):
        return len(board.get_legal_moves(-1 * color))

    @staticmethod
    def is_terminal(board, color, my_moves=None, op_moves=None):
        if my_moves is None:
            my_moves = board.get_legal_moves(color)
        if op_moves is None:
            op_moves = board.get_legal_moves(-1 * color)
        return len(my_moves) == 0 and len(op_moves) == 0