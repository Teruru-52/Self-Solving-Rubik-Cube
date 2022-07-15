from functools import lru_cache
import time 
import state

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

# 対面を引くdict
inv_face = {
    "U": "D",
    "D": "U",
    "L": "R",
    "R": "L",
    "F": "B",
    "B": "F"
}

# ここにPhase1，2の遷移表と手数表を記述する

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

move_names_to_index = {move_name: i for i, move_name in enumerate(move_names)}

class Search1:
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

move_names_to_index_ph2 = {move_name: i for i, move_name in enumerate(move_names_ph2)}

class Search2:
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