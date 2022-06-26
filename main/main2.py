# import motors
import state
import random
from shutil import move
# import time 
from time import sleep
from functools import lru_cache

NUM_CORNERS = 8
NUM_EDGES = 12

NUM_CO = 2187  # 3 ** 7
NUM_EO = 2048  # 2 ** 11
NUM_E_COMBINATIONS = 495  # 12C4

NUM_CP = 40320  # 8!
# NUM_EP = 479001600  # 12! # これは使わない
NUM_UD_EP = 40320  # 8!
NUM_E_EP = 24  # 4!

def scamble2state(scramble):
    """
    スクランブル文字列適用したstateを返す
    """
    scrambled_state = solved_state
    for move_name in scramble.split(" "):
        move_state = moves[move_name]
        scrambled_state = scrambled_state.apply_move(move_state)
    return scrambled_state

def Create_scramble(scramble_length):
    move_names = "U U' U2 D D' D2 L L' L2 R R' R2 F F' F2 B B' B2"
    random_scramble = " ".join(random.choices(move_names.split(), k=scramble_length))
    return random_scramble

"""メイン関数"""
if __name__ == '__main__':
        # 完成状態を表すインスタンス
    solved_state = state.State(
        [0, 1, 2, 3, 4, 5, 6, 7],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )

    # 18種類の1手操作を全部定義する
    moves = {
        'U': state.State([3, 0, 1, 2, 4, 5, 6, 7],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 1, 2, 3, 7, 4, 5, 6, 8, 9, 10, 11],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        'D': state.State([0, 1, 2, 3, 5, 6, 7, 4],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        'L': state.State([4, 1, 2, 0, 7, 5, 6, 3],
                   [2, 0, 0, 1, 1, 0, 0, 2],
                   [11, 1, 2, 7, 4, 5, 6, 0, 8, 9, 10, 3],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        'R': state.State([0, 2, 6, 3, 4, 1, 5, 7],
                   [0, 1, 2, 0, 0, 2, 1, 0],
                   [0, 5, 9, 3, 4, 2, 6, 7, 8, 1, 10, 11],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        'F': state.State([0, 1, 3, 7, 4, 5, 2, 6],
                   [0, 0, 1, 2, 0, 0, 2, 1],
                   [0, 1, 6, 10, 4, 5, 3, 7, 8, 9, 2, 11],
                   [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0]),
        'B': state.State([1, 5, 2, 3, 0, 4, 6, 7],
                   [1, 2, 0, 0, 2, 1, 0, 0],
                   [4, 8, 2, 3, 1, 5, 6, 7, 0, 9, 10, 11],
                   [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
                   )}
    move_names = []
    faces = list(moves.keys())
    for face_name in faces:
        move_names += [face_name, face_name + '2', face_name + '\'']
        moves[face_name + '2'] = moves[face_name].apply_move(moves[face_name])
        moves[face_name + '\''] = moves[face_name].apply_move(moves[face_name]).apply_move(moves[face_name])
    print(move_names)

    scramble_length = 20
    random_scramble = Create_scramble(scramble_length)
    print('random_scramble = ', random_scramble)
    # motor = motors.Motor()
    # motor.Solve(random_scramble)

    sleep(2)
    print('start solving')

    """Phase1探索プログラムの動作確認"""
    # scramble = "R' U' F R' B' F2 L2 D' U' L2 F2 D' L2 D' R B D2 L D2 F2 U2 L R' U' F"
    scrambled_state = scamble2state(random_scramble)
    search = Search(scrambled_state)
    start = time.time()
    solution = search.start_search()
    print(f"Finished! ({time.time() - start:.2f} sec.)")
    if solution:
      print(f'Solution: "{solution}"')
    else:
      print("Solution not found.")