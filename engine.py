import subprocess
import time
import re


# p = subprocess.Popen(r'stockfish_15_win_x64_avx2\stockfish.exe',stdout=subprocess.PIPE,stdin=subprocess.PIPE)
# p.stdin.write(b'uci\n')
# p.stdin.flush()
# print(p.stdout.readline())

# print(p.communicate()[0].decode('utf-8'))


class Engine:
    def __init__(self):
        self.process = subprocess.Popen(r'stockfish_15_win_x64_avx2\stockfish.exe', stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE)

    def command(self, cmd, stop_word, time_out=0.0):
        self.process.stdin.write(cmd.encode('utf-8'))
        self.process.stdin.flush()
        lines = []
        time.sleep(time_out)
        while True:
            text = self.process.stdout.readline().decode('utf-8').strip()
            lines.append(text)
            if stop_word in text:
                break
        return lines

    def uci(self):
        self.command('uci\n', 'uciok')

    def eval(self, moves_made_in_uci):
        # set stating position
        self.process.stdin.write(b'position startpos\n')
        # make moves in stockfish in uci
        uci_moves = ' '.join(moves_made_in_uci)
        self.process.stdin.write(f'position startpos move {uci_moves}\n'.encode('utf-8'))
        # get final eval
        lines = self.command('eval\n', 'Final evaluation', 0.5)
        return float(re.search('(?<=Final evaluation)\s*[A-Z0-9.+-]+', lines[-1]).group().strip())

    def find_moves_info_in_uci(self, moves_made_in_uci, move_time=1000, depth=20):
        # set stating position
        self.process.stdin.write(b'position startpos\n')
        # make moves in stockfish in uci
        uci_moves = ' '.join(moves_made_in_uci)
        self.process.stdin.write(f'position startpos move {uci_moves}\n'.encode('utf-8'))
        # get the best move
        lines = self.command(f'go movetime {move_time} depth {depth}\n', 'bestmove', (move_time / 1000) + 0.25)
        # get info of the moves
        is_mate = False
        try:
            score = re.search('(?<=cp )[-\d]+', lines[-2]).group()
        except AttributeError:
            is_mate = True
            score = re.search('(?<=mate )[-\d]+', lines[-2]).group()
        try:
            best_move = re.search('(?<=bestmove )[\da-z]+', lines[-1]).group()
        except AttributeError:
            best_move = None
        return is_mate, float(score), best_move

    @staticmethod
    # method to get the ovr accuracy of white or black base on the number of moves of each type
    def get_accuracy_score(best, excellent, good, inaccuracy, mistake, blunder):
        number_of_moves = best + excellent + good + inaccuracy + mistake + blunder
        # coefficient:
        #   best: 1.0
        #   excellent: 0.925
        #   good: 0.75
        #   inaccuracy : 0.5
        #   mistake: 0.25
        #   blunder: 0.0

        return (best + excellent * 0.9 + good * 0.725 + inaccuracy * 0.45 + mistake * 0.25) / number_of_moves * 100

        pass

    @staticmethod
    # method to classify the type of move like best,good,mistake etc depends on the eval before and after the move
    def classifying_move(best_move_eval, your_move_eval, is_mate=False, is_mate_2=False):
        if is_mate:
            if best_move_eval > 0:
                if is_mate_2 and your_move_eval == best_move_eval - 1:
                    return 0
                if is_mate_2 and your_move_eval > 0:
                    return 1
                if is_mate_2 and your_move_eval < 0:
                    return 5
                if your_move_eval / 100 >= 10:
                    return 2
                if your_move_eval / 100 >= 6:
                    return 3
                if your_move_eval / 100 >= 4:
                    return 4
                else:
                    return 5
            else:
                if is_mate_2 and your_move_eval == best_move_eval + 1:
                    return 0
                else:
                    return 1

        if is_mate_2:
            best_move_eval /= 100
        if best_move_eval >= 10:
            if is_mate_2:
                if your_move_eval >= 0:
                    return 0
                return 5
            if your_move_eval >= 10:
                return 1
            elif your_move_eval <= 0:
                return 5
            ratio = your_move_eval / best_move_eval
            if ratio >= 0.8:
                return 1
            if ratio >= 0.7:
                return 2
            if ratio >= 0.55:
                return 3
            if ratio >= 0.35:
                return 4
            else:
                return 5
        elif 0 <= best_move_eval < 10 or -10 < best_move_eval < 0:
            if is_mate_2:
                if (best_move_eval >= 0 and your_move_eval >= 0):
                    return 0
                if best_move_eval >= 0 and your_move_eval < 0:
                    return 5
                if best_move_eval < 0 and your_move_eval < 0:
                    return 5
            diff = best_move_eval - your_move_eval
            if diff <= 0.3:
                return 0
            if diff <= 1:
                return 1
            if diff <= 1.5:
                return 2
            if diff <= 2.5:
                return 3
            if diff <= 4:
                return 4
            else:
                return 5

        elif best_move_eval <= -10:
            if is_mate_2:
                return 4
            if your_move_eval <= -10:
                return 1
            ratio = best_move_eval / your_move_eval
            if ratio >= 0.8:
                return 1
            if ratio >= 0.7:
                return 2
            if ratio >= 0.35:
                return 3
            else:
                return 4

        pass

# engine=Engine()
# engine.uci()
# test='''d2d4 g8f6 c2c4 c7c5 d4d5 e7e6 b1c3 e6d5 c4d5 d7d6 g1f3 g7g6 c1g5 f8g7 f3d2 h7h6 g5h4 g6g5 h4g3 f6h5 d2c4 h5g3 h2g3 e8g8 e2e3 d8e7 f1e2 f8d8 e1g1 b8d7 a2a4 d7e5 c4e5 e7e5 a4a5 a8b8 a1a2 c8d7 c3b5 d7b5 e2b5 b7b6 a5a6 b8c8 d1d3 c8c7 b2b3 e5c3 d3c3 g7c3 a2c2 c3f6 g3g4 c7e7 c2c4 d8c8 g2g3 f6g7 f1d1 c8f8 d1d3 g8h7 g1g2 h7g6 d3d1 h6h5 g4h5 g6h5 g3g4 h5g6 c4c2 f8h8 b5d3 g6f6 g2g3 e7e8 d3b5 e8e4 c2c4 e4c4 b3c4 f6e7 b5a4 g7e5 g3f3 h8h4 d1g1 f7f5'''
# test=re.split('\s',test)
# print(engine.analysis(test))
