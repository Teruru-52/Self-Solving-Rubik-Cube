import motors
import random
from shutil import move
import time 
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

class State:
    """
    ルービックキューブの状態を表すクラス
    """

    def __init__(self, cp, co, ep, eo):
        self.cp = cp
        self.co = co
        self.ep = ep
        self.eo = eo

    def apply_move(self, move):
        """
        操作を適用し、新しい状態を返す
        """
        new_cp = [self.cp[p] for p in move.cp]
        new_co = [(self.co[p] + move.co[i]) % 3 for i, p in enumerate(move.cp)]
        new_ep = [self.ep[p] for p in move.ep]
        new_eo = [(self.eo[p] + move.eo[i]) % 2 for i, p in enumerate(move.ep)]
        return State(new_cp, new_co, new_ep, new_eo)

# 完成状態を表すインスタンス
solved_state = State(
    [0, 1, 2, 3, 4, 5, 6, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
)

# 18種類の1手操作を全部定義する
moves = {
    'U': State([3, 0, 1, 2, 4, 5, 6, 7],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 2, 3, 7, 4, 5, 6, 8, 9, 10, 11],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    'D': State([0, 1, 2, 3, 5, 6, 7, 4],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    'L': State([4, 1, 2, 0, 7, 5, 6, 3],
               [2, 0, 0, 1, 1, 0, 0, 2],
               [11, 1, 2, 7, 4, 5, 6, 0, 8, 9, 10, 3],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    'R': State([0, 2, 6, 3, 4, 1, 5, 7],
               [0, 1, 2, 0, 0, 2, 1, 0],
               [0, 5, 9, 3, 4, 2, 6, 7, 8, 1, 10, 11],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    'F': State([0, 1, 3, 7, 4, 5, 2, 6],
               [0, 0, 1, 2, 0, 0, 2, 1],
               [0, 1, 6, 10, 4, 5, 3, 7, 8, 9, 2, 11],
               [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0]),
    'B': State([1, 5, 2, 3, 0, 4, 6, 7],
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


def scamble2state(scramble):
    """
    スクランブル文字列適用したstateを返す
    """
    scrambled_state = solved_state
    for move_name in scramble.split(" "):
        move_state = moves[move_name]
        scrambled_state = scrambled_state.apply_move(move_state)
    return scrambled_state

# 対面を引くdict
inv_face = {
    "U": "D",
    "D": "U",
    "L": "R",
    "R": "L",
    "F": "B",
    "B": "F"
}

@lru_cache(maxsize=400)
def is_move_available(prev_move, move):
    """
    前の1手を考慮して次の1手として使える操作であるかを判定する
    - 同じ面は連続して回さない (e.g. R' R2 は不可)
    - 対面を回すときは順序を固定する (e.g. D Uは良いが、U Dは不可)
    """
    if prev_move is None:
        return True  # 最初の1手はどの操作も可
    prev_face = prev_move[0]  # 1手前で回した面
    if prev_face == move[0]:
        return False # 同一面は不可
    if inv_face[prev_face] == move[0]:
        return prev_face < move[0] # 対面のときは、辞書順なら可
    return True

"""COのindex化"""
def co_to_index(co):
    index = 0
    for co_i in co[:-1]:
        index *= 3
        index += co_i
    return index

def index_to_co(index):
    co = [0] * 8
    sum_co = 0
    for i in range(6, -1, -1):
        co[i] = index % 3
        index //= 3
        sum_co += co[i]
    co[-1] = (3 - sum_co % 3) % 3
    return co

"""EOのindex化"""
def eo_to_index(eo):
    index = 0
    for eo_i in eo[:-1]:
        index *= 2
        index += eo_i
    return index


def index_to_eo(index):
    eo = [0] * 12
    sum_eo = 0
    for i in range(10, -1, -1):
        eo[i] = index % 2
        index //= 2
        sum_eo += eo[i]
    eo[-1] = (2 - sum_eo % 2) % 2
    return eo

def calc_combination(n, r):
    """nCrの計算"""
    ret = 1
    for i in range(r):
        ret *= n - i
    for i in range(r):
        ret //= r - i
    return ret

def e_combination_to_index(comb):
    index = 0
    r = 4
    for i in range(12 - 1, -1, -1):
        if comb[i]:
            index += calc_combination(i, r)
            r -= 1
    return index

def index_to_e_combination(index):
    combination = [0] * 12
    r = 4
    for i in range(12 - 1, -1, -1):
        if index >= calc_combination(i, r):
            combination[i] = 1
            index -= calc_combination(i, r)
            r -= 1
    return combination

"""CPのindex化"""
def cp_to_index(cp):
    index = 0
    for i, cp_i in enumerate(cp):
        index *= 8 - i
        for j in range(i + 1, 8):
            if cp[i] > cp[j]:
                index += 1
    return index

def index_to_cp(index):
    cp = [0] * 8
    for i in range(6, -1, -1):
        cp[i] = index % (8 - i)
        index //= 8 - i
        for j in range(i + 1, 8):
            if cp[j] >= cp[i]:
                cp[j] += 1
    return cp

"""UD面のEPのindex化"""
def ud_ep_to_index(ep):
    index = 0
    for i, ep_i in enumerate(ep):
        index *= 8 - i
        for j in range(i + 1, 8):
            if ep[i] > ep[j]:
                index += 1
    return index


def index_to_ud_ep(index):
    ep = [0] * 8
    for i in range(6, -1, -1):
        ep[i] = index % (8 - i)
        index //= 8 - i
        for j in range(i + 1, 8):
            if ep[j] >= ep[i]:
                ep[j] += 1
    return ep

"""E列のEPのindex化"""
def e_ep_to_index(eep):
    index = 0
    for i, eep_i in enumerate(eep):
        index *= 4 - i
        for j in range(i + 1, 4):
            if eep[i] > eep[j]:
                index += 1
    return index


def index_to_e_ep(index):
    eep = [0] * 4
    for i in range(4 - 2, -1, -1):
        eep[i] = index % (4 - i)
        index //= 4 - i
        for j in range(i + 1, 4):
            if eep[j] >= eep[i]:
                eep[j] += 1
    return eep

"""Phase1の遷移表"""
"""COの遷移表"""
print("Computing co_move_table")
start = time.time()
co_move_table = [[0] * len(move_names) for _ in range(NUM_CO)]
for i in range(NUM_CO):
    state = State(
        [0] * 8,
        index_to_co(i),
        [0] * 12,
        [0] * 12
    )
    for i_move, move_name in enumerate(move_names):
        new_state = state.apply_move(moves[move_name])
        co_move_table[i][i_move] = co_to_index(new_state.co)
print(f"Finished! ({time.time() - start:.5f} sec.)")

"""EOの遷移表"""
print("Computing eo_move_table")
start = time.time()
eo_move_table = [[0] * len(move_names) for _ in range(NUM_EO)]
for i in range(NUM_EO):
    state = State(
        [0] * 8,
        [0] * 8,
        [0] * 12,
        index_to_eo(i)
    )
    for i_move, move_name in enumerate(move_names):
        new_state = state.apply_move(moves[move_name])
        eo_move_table[i][i_move] = eo_to_index(new_state.eo)
print(f"Finished! ({time.time() - start:.5f} sec.)")

"""E列エッジの組合せの遷移表"""
print("Computing e_combination_table")
start = time.time()
e_combination_table = [[0] * len(move_names) for _ in range(NUM_E_COMBINATIONS)]
for i in range(NUM_E_COMBINATIONS):
    state = State(
        [0] * 8,
        [0] * 8,
        index_to_e_combination(i),
        [0] * 12,
    )
    for i_move, move_name in enumerate(move_names):
        new_state = state.apply_move(moves[move_name])
        e_combination_table[i][i_move] = e_combination_to_index(new_state.ep)
print(f"Finished! ({time.time() - start:.5f} sec.)")

"""Phase2の遷移表"""
move_names_ph2 = ["U", "U2", "U'", "D", "D2", "D'", "L2", "R2", "F2", "B2"]

"""CPの遷移表"""
print("Computing cp_move_table")
cp_move_table = [[0] * len(move_names_ph2) for _ in range(NUM_CP)]
start = time.time()
for i in range(NUM_CP):
    state = State(
        index_to_cp(i),
        [0] * 8,
        [0] * 12,
        [0] * 12
    )
    for i_move, move_name in enumerate(move_names_ph2):
        new_state = state.apply_move(moves[move_name])
        cp_move_table[i][i_move] = cp_to_index(new_state.cp)
print(f"Finished! ({time.time() - start:.5f} sec.)")

"""UD面エッジのEPの遷移表"""
print("Computing ud_ep_move_table")
ud_ep_move_table = [[0] * len(move_names_ph2) for _ in range(NUM_UD_EP)]
start = time.time()
for i in range(NUM_UD_EP):
    state = State(
        [0] * 8,
        [0] * 8,
        [0] * 4 + index_to_ud_ep(i),
        [0] * 12
    )
    for i_move, move_name in enumerate(move_names_ph2):
        new_state = state.apply_move(moves[move_name])
        ud_ep_move_table[i][i_move] = ud_ep_to_index(new_state.ep[4:])
print(f"Finished! ({time.time() - start:.5f} sec.)")

"""E列エッジのEPの遷移表"""
print("Computing e_edge_permutation_move_table")
e_ep_move_table = [[0] * len(move_names_ph2) for _ in range(NUM_E_EP)]
start = time.time()
for i in range(NUM_E_EP):
    state = State(
        [0] * 8,
        [0] * 8,
        index_to_e_ep(i) + [0] * 8,
        [0] * 12,
    )
    for i_move, move_name in enumerate(move_names_ph2):
        new_state = state.apply_move(moves[move_name])
        e_ep_move_table[i][i_move] = e_ep_to_index(new_state.ep[:4])
print(f"Finished! ({time.time() - start:.5f} sec.)")

"""Phase1の枝刈り表"""
"""EOを無視して、COとE列だけ考えたときの最短手数表"""
print("Computing co_eec_prune_table")
start = time.time()
co_eec_prune_table = [[-1] * NUM_E_COMBINATIONS for _ in range(NUM_CO)]
co_eec_prune_table[0][0] = 0
distance = 0
num_filled = 1
while num_filled != NUM_CO * NUM_E_COMBINATIONS:
    print(f"distance = {distance}")
    print(f"num_filled = {num_filled}")
    for i_co in range(NUM_CO):
        for i_eec in range(NUM_E_COMBINATIONS):
            if co_eec_prune_table[i_co][i_eec] == distance:
                for i_move in range(len(move_names)):
                    next_co = co_move_table[i_co][i_move]
                    next_eec = e_combination_table[i_eec][i_move]
                    if co_eec_prune_table[next_co][next_eec] == -1:
                        co_eec_prune_table[next_co][next_eec] = distance + 1
                        num_filled += 1
    distance += 1
print(f"Finished! ({time.time() - start:.5f} sec.)")

"""COを無視して、EOとE列だけ考えたときの最短手数表"""
print("Computing eo_eec_prune_table")
start = time.time()
eo_eec_prune_table = [[-1] * NUM_E_COMBINATIONS for _ in range(NUM_EO)]
eo_eec_prune_table[0][0] = 0
distance = 0
num_filled = 1
while num_filled != NUM_EO * NUM_E_COMBINATIONS:
    print(f"distance = {distance}")
    print(f"num_filled = {num_filled}")
    for i_eo in range(NUM_EO):
        for i_eec in range(NUM_E_COMBINATIONS):
            if eo_eec_prune_table[i_eo][i_eec] == distance:
                for i_move in range(len(move_names)):
                    next_eo = eo_move_table[i_eo][i_move]
                    next_eec = e_combination_table[i_eec][i_move]
                    if eo_eec_prune_table[next_eo][next_eec] == -1:
                        eo_eec_prune_table[next_eo][next_eec] = distance + 1
                        num_filled += 1
    distance += 1
print(f"Finished! ({time.time() - start:.5f} sec.)") 

"""Phase2の枝刈り表"""
"""UD面のエッジを無視して、CPとE列エッジだけ揃えるときの最短手数表"""
print("Computing cp_eep_prune_table")
start = time.time()
cp_eep_prune_table = [[-1] * NUM_E_EP for _ in range(NUM_CP)]
cp_eep_prune_table[0][0] = 0
distance = 0
num_filled = 1
while num_filled != NUM_CP * NUM_E_EP:
    print(f"distance = {distance}")
    print(f"num_filled = {num_filled}")
    for i_cp in range(NUM_CP):
        for i_eep in range(NUM_E_EP):
            if cp_eep_prune_table[i_cp][i_eep] == distance:
                for i_move in range(len(move_names_ph2)):
                    next_cp = cp_move_table[i_cp][i_move]
                    next_eep = e_ep_move_table[i_eep][i_move]
                    if cp_eep_prune_table[next_cp][next_eep] == -1:
                        cp_eep_prune_table[next_cp][next_eep] = distance + 1
                        num_filled += 1
    distance += 1
print(f"Finished! ({time.time() - start:.5f} sec.)")

"""CPを無視して、UD面のエッジとE列エッジだけ揃えるときの最短手数表"""
print("Computing udep_eep_prune_table")
start = time.time()
udep_eep_prune_table = [[-1] * NUM_E_EP for _ in range(NUM_UD_EP)]
udep_eep_prune_table[0][0] = 0
distance = 0
num_filled = 1
while num_filled != NUM_UD_EP * NUM_E_EP:
    print(f"distance = {distance}")
    print(f"num_filled = {num_filled}")
    for i_udep in range(NUM_UD_EP):
        for i_eep in range(NUM_E_EP):
            if udep_eep_prune_table[i_udep][i_eep] == distance:
                for i_move in range(len(move_names_ph2)):
                    next_udep = ud_ep_move_table[i_udep][i_move]
                    next_eep = e_ep_move_table[i_eep][i_move]
                    if udep_eep_prune_table[next_udep][next_eep] == -1:
                        udep_eep_prune_table[next_udep][next_eep] = distance + 1
                        num_filled += 1
    distance += 1
print(f"Finished! ({time.time() - start:.5f} sec.)") 

move_names_to_index = {move_name: i for i, move_name in enumerate(move_names)}

class Search:
    def __init__(self, state):
        self.initial_state = state
        self.current_solution_ph1 = []

    def depth_limited_search_ph1(self, co_index, eo_index, e_comb_index, depth):
        if depth == 0 and co_index == 0 and eo_index == 0 and e_comb_index == 0:
            return True
        if depth == 0:
            return False

        # 枝刈り
        if max(co_eec_prune_table[co_index][e_comb_index], eo_eec_prune_table[eo_index][e_comb_index]) > depth:
            return False

        prev_move = self.current_solution_ph1[-1] if self.current_solution_ph1 else None
        for move_name in move_names:
            if not is_move_available(prev_move, move_name):
                continue
            self.current_solution_ph1.append(move_name)
            move_index = move_names_to_index[move_name]
            next_co_index = co_move_table[co_index][move_index]
            next_eo_index = eo_move_table[eo_index][move_index]
            next_e_comb_index = e_combination_table[e_comb_index][move_index]
            if self.depth_limited_search_ph1(next_co_index, next_eo_index, next_e_comb_index, depth - 1):
                return True
            self.current_solution_ph1.pop()

    def start_search(self, max_length=20):
        co_index = co_to_index(self.initial_state.co)
        eo_index = eo_to_index(self.initial_state.eo)
        e_combination = [1 if e in (0, 1, 2, 3) else 0 for e in self.initial_state.ep]
        e_comb_index = e_combination_to_index(e_combination)
        depth = 0
        while depth <= max_length:
            print(f"# Start searching phase 1 length {depth}")
            if self.depth_limited_search_ph1(co_index, eo_index, e_comb_index, depth):
                return " ".join(self.current_solution_ph1)
            depth += 1
        return None

def Create_scramble(scramble_length):
    move_names = "U U' U2 D D' D2 L L' L2 R R' R2 F F' F2 B B' B2"
    random_scramble = " ".join(random.choices(move_names.split(), k=scramble_length))
    return random_scramble

print('start scramble')
sleep(5)

scramble_length = 20
random_scramble = Create_scramble(scramble_length)
print('random_scramble = ', random_scramble)
motor = motors.Motor()
motor.Solve(random_scramble)

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

move_names_to_index_ph2 = {move_name: i for i, move_name in enumerate(move_names_ph2)}

class Search:
    def __init__(self, state):
        self.initial_state = state
        self.current_solution_ph1 = []
        self.current_solution_ph2 = []
        self.max_solution_length = 9999
        self.start = 0

    def depth_limited_search_ph1(self, co_index, eo_index, e_comb_index, depth):
        if depth == 0 and co_index == 0 and eo_index == 0 and e_comb_index == 0:
            state = self.initial_state
            for move_name in self.current_solution_ph1:
                state = state.apply_move(moves[move_name])
            return self.start_phase2(state)

        if depth == 0:
            return False

        # 枝刈り
        if max(co_eec_prune_table[co_index][e_comb_index], eo_eec_prune_table[eo_index][e_comb_index]) > depth:
            return False

        prev_move = self.current_solution_ph1[-1] if self.current_solution_ph1 else None
        for move_name in move_names:
            if not is_move_available(prev_move, move_name):
                continue
            self.current_solution_ph1.append(move_name)
            move_index = move_names_to_index[move_name]
            next_co_index = co_move_table[co_index][move_index]
            next_eo_index = eo_move_table[eo_index][move_index]
            next_e_comb_index = e_combination_table[e_comb_index][move_index]
            if self.depth_limited_search_ph1(next_co_index, next_eo_index, next_e_comb_index, depth - 1):
                return True
            self.current_solution_ph1.pop()

    def depth_limited_search_ph2(self, cp_index, udep_index, eep_index, depth):
        if depth == 0 and cp_index == 0 and udep_index == 0 and eep_index == 0:
            return True
        if depth == 0:
            return False

        # 枝刈り
        if max(cp_eep_prune_table[cp_index][eep_index], udep_eep_prune_table[udep_index][eep_index]) > depth:
            return False

        if self.current_solution_ph2:
            prev_move = self.current_solution_ph2[-1]
        elif self.current_solution_ph1:
            prev_move = self.current_solution_ph1[-1]
        else:
            prev_move = None

        for move_name in move_names_ph2:
            if not is_move_available(prev_move, move_name):
                continue
            self.current_solution_ph2.append(move_name)
            move_index = move_names_to_index_ph2[move_name]
            next_cp_index = cp_move_table[cp_index][move_index]
            next_udep_index = ud_ep_move_table[udep_index][move_index]
            next_eep_index = e_ep_move_table[eep_index][move_index]
            if self.depth_limited_search_ph2(next_cp_index, next_udep_index, next_eep_index, depth - 1):
                return True
            self.current_solution_ph2.pop()

    def start_search(self, max_length=30):
        self.start = time.time()
        self.max_solution_length = max_length
        co_index = co_to_index(self.initial_state.co)
        eo_index = eo_to_index(self.initial_state.eo)
        e_combination = [1 if e in (0, 1, 2, 3) else 0 for e in self.initial_state.ep]
        e_comb_index = e_combination_to_index(e_combination)

        depth = 0
        while depth <= self.max_solution_length:
            if self.depth_limited_search_ph1(co_index, eo_index, e_comb_index, depth):
                return " ".join(self.current_solution_ph1) + " " + " ".join(self.current_solution_ph2)
            depth += 1
        return None

    def start_phase2(self, state):
        cp_index = cp_to_index(state.cp)
        udep_index = ud_ep_to_index(state.ep[4:])
        eep_index = e_ep_to_index(state.ep[:4])
        depth = 0
        while depth <= self.max_solution_length - len(self.current_solution_ph1):
            if self.depth_limited_search_ph2(cp_index, udep_index, eep_index, depth):
                return True
            depth += 1

"""Phase2探索プログラムの動作確認"""
# scramble = "R' U' F R' B' F2 L2 D' U' L2 F2 D' L2 D' R B D2 L D2 F2 U2 L R' U' F"
scrambled_state = scamble2state(random_scramble)
search = Search(scrambled_state)
start = time.time()
solution = search.start_search()
print(f"Finished! ({time.time() - start:.4f} sec.)")
if solution:
  print(f'Solution: "{solution}"')
else:
  print("Solution not found.")
motor.Solve(solution)
motor.Cleanup()