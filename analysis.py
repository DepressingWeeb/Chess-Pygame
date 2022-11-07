import multiprocessing
import sys

from engine import Engine


def analysis(moves_made_in_uci, q, acc_white, acc_black, count_type_white, count_type_black, types,is_terminate):
    stockfish = Engine()
    for i in range(len(moves_made_in_uci)):
        if is_terminate.value == 1:
            sys.exit()
        is_mate, best_move_eval, best_move = stockfish.find_moves_info_in_uci(moves_made_in_uci[:i])
        is_mate_2, your_move_eval, next_best_move = stockfish.find_moves_info_in_uci(moves_made_in_uci[:i + 1])
        if best_move == moves_made_in_uci[i]:
            type = 0
            print(0, best_move_eval / 100, -your_move_eval / 100)
        elif is_mate or is_mate_2:
            type = stockfish.classifying_move(best_move_eval, -your_move_eval, is_mate, is_mate_2)
            print(type, f'Mate in {best_move_eval}', f'Mate in {your_move_eval}')
        else:
            type = stockfish.classifying_move(best_move_eval / 100, -your_move_eval / 100)
            print(type, best_move_eval / 100, -your_move_eval / 100)
        if i % 2 == 0:
            count_type_white[type] += 1
        else:
            count_type_black[type] += 1
        types[i] = type
        q.put(i)
    acc_white.value = stockfish.get_accuracy_score(count_type_white[0], count_type_white[1], count_type_white[2],
                                                   count_type_white[3], count_type_white[4], count_type_white[5])
    acc_black.value = stockfish.get_accuracy_score(count_type_black[0], count_type_black[1], count_type_black[2],
                                                   count_type_black[3], count_type_black[4], count_type_black[5])
