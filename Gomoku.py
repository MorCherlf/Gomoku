import math

class GomokuAI:
    def __init__(self, size=15):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.human = 'O'
        self.ai = 'X'

    def is_win(self, player):
        # 检查行、列、对角线是否形成五连
        for i in range(self.size):
            for j in range(self.size - 4):
                if all(self.board[i][j + k] == player for k in range(5)) or \
                   all(self.board[j + k][i] == player for k in range(5)):
                    return True
        for i in range(self.size - 4):
            for j in range(self.size - 4):
                if all(self.board[i + k][j + k] == player for k in range(5)) or \
                   all(self.board[i + k][j + 4 - k] == player for k in range(5)):
                    return True
        return False

    def evaluate(self):
        def score_line(line):
            scores = {
                'XXXXX': 100000,
                'XXXX.': 1000, '.XXXX': 1000,
                'XXX..': 100, '..XXX': 100,
                'OOOOO': -100000,
                'OOOO.': -1000, '.OOOO': -1000,
                'OOO..': -100, '..OOO': -100,
            }
            score = 0
            for pattern, value in scores.items():
                score += line.count(pattern) * value
            return score

        total_score = 0
        for i in range(self.size):
            row = ''.join(self.board[i])
            col = ''.join([self.board[j][i] for j in range(self.size)])
            total_score += score_line(row)
            total_score += score_line(col)

        for d in range(-self.size + 1, self.size):
            main_diag = ''.join(
                self.board[i][i - d] 
                for i in range(max(0, d), min(self.size, self.size + d)) 
                if 0 <= i - d < self.size
            )
            anti_diag = ''.join(
                self.board[i][self.size - 1 - i + d]
                for i in range(max(0, -d), min(self.size, self.size - d)) 
                if 0 <= self.size - 1 - i + d < self.size
            )
            total_score += score_line(main_diag)
            total_score += score_line(anti_diag)

        return total_score

    def generate_candidates(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        candidates = set()

        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != '.':
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == '.':
                            candidates.add((nx, ny))

        return list(candidates)

    def alphabeta(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_win(self.ai) or self.is_win(self.human):
            return self.evaluate(), None

        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            for x, y in self.generate_candidates():
                self.board[x][y] = self.ai
                eval, _ = self.alphabeta(depth - 1, alpha, beta, False)
                self.board[x][y] = '.'
                if eval > max_eval:
                    max_eval = eval
                    best_move = (x, y)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            best_move = None
            for x, y in self.generate_candidates():
                self.board[x][y] = self.human
                eval, _ = self.alphabeta(depth - 1, alpha, beta, True)
                self.board[x][y] = '.'
                if eval < min_eval:
                    min_eval = eval
                    best_move = (x, y)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def play(self):
        print("Game Start! You're 'O', and the AI is 'X'。")
        self.print_board()

        while True:
            move = input("Input your step location like 'x y': ")
            x, y = map(int, move.split())
            if self.board[x][y] == '.':
                self.board[x][y] = self.human
            else:
                print("Invaild location, try again!")
                continue

            if self.is_win(self.human):
                self.print_board()
                print("You're Winner!")
                break

            print("AI is thinking......")
            _, move = self.alphabeta(3, -math.inf, math.inf, True)
            if move:
                self.board[move[0]][move[1]] = self.ai
            self.print_board()

            if self.is_win(self.ai):
                print("You lost.")
                break

    def print_board(self):
        print("  " + " ".join(map(str, range(self.size))))
        for i in range(self.size):
            print(f"{i} " + " ".join(self.board[i]))

if __name__ == "__main__":
    game = GomokuAI()
    game.play()
