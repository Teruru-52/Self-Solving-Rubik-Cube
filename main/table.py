import time 
import state

NUM_CORNERS = 8
NUM_EDGES = 12

NUM_CO = 2187  # 3 ** 7
NUM_EO = 2048  # 2 ** 11
NUM_E_COMBINATIONS = 495  # 12C4

NUM_CP = 40320  # 8!
# NUM_EP = 479001600  # 12! # これは使わない
NUM_UD_EP = 40320  # 8!
NUM_E_EP = 24  # 4!

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
    state_ = state.State(
        [0] * 8,
        index_to_co(i),
        [0] * 12,
        [0] * 12
    )
    for i_move, move_name in enumerate(move_names):
        new_state = state_.apply_move(moves[move_name])
        co_move_table[i][i_move] = co_to_index(new_state.co)
# f = open('co_move_table.txt', 'w')
# f.writelines(co_move_table)
# f.close()
print(f"Finished! ({time.time() - start:.5f} sec.)")
print("co_move_table = ", co_move_table)

# """EOの遷移表"""
# print("Computing eo_move_table")
# start = time.time()
# eo_move_table = [[0] * len(move_names) for _ in range(NUM_EO)]
# for i in range(NUM_EO):
#     state_ = state.State(
#         [0] * 8,
#         [0] * 8,
#         [0] * 12,
#         index_to_eo(i)
#     )
#     for i_move, move_name in enumerate(move_names):
#         new_state = state_.apply_move(moves[move_name])
#         eo_move_table[i][i_move] = eo_to_index(new_state.eo)
# print(f"Finished! ({time.time() - start:.5f} sec.)")

# """E列エッジの組合せの遷移表"""
# print("Computing e_combination_table")
# start = time.time()
# e_combination_table = [[0] * len(move_names) for _ in range(NUM_E_COMBINATIONS)]
# for i in range(NUM_E_COMBINATIONS):
#     state_ = state.State(
#         [0] * 8,
#         [0] * 8,
#         index_to_e_combination(i),
#         [0] * 12,
#     )
#     for i_move, move_name in enumerate(move_names):
#         new_state = state_.apply_move(moves[move_name])
#         e_combination_table[i][i_move] = e_combination_to_index(new_state.ep)
# print(f"Finished! ({time.time() - start:.5f} sec.)")

# """Phase2の遷移表"""
# move_names_ph2 = ["U", "U2", "U'", "D", "D2", "D'", "L2", "R2", "F2", "B2"]

# """CPの遷移表"""
# print("Computing cp_move_table")
# cp_move_table = [[0] * len(move_names_ph2) for _ in range(NUM_CP)]
# start = time.time()
# for i in range(NUM_CP):
#     state_ = state.State(
#         index_to_cp(i),
#         [0] * 8,
#         [0] * 12,
#         [0] * 12
#     )
#     for i_move, move_name in enumerate(move_names_ph2):
#         new_state = state_.apply_move(moves[move_name])
#         cp_move_table[i][i_move] = cp_to_index(new_state.cp)
# print(f"Finished! ({time.time() - start:.5f} sec.)")

# """UD面エッジのEPの遷移表"""
# print("Computing ud_ep_move_table")
# ud_ep_move_table = [[0] * len(move_names_ph2) for _ in range(NUM_UD_EP)]
# start = time.time()
# for i in range(NUM_UD_EP):
#     state_ = state.State(
#         [0] * 8,
#         [0] * 8,
#         [0] * 4 + index_to_ud_ep(i),
#         [0] * 12
#     )
#     for i_move, move_name in enumerate(move_names_ph2):
#         new_state = state_.apply_move(moves[move_name])
#         ud_ep_move_table[i][i_move] = ud_ep_to_index(new_state.ep[4:])
# print(f"Finished! ({time.time() - start:.5f} sec.)")

# """E列エッジのEPの遷移表"""
# print("Computing e_edge_permutation_move_table")
# e_ep_move_table = [[0] * len(move_names_ph2) for _ in range(NUM_E_EP)]
# start = time.time()
# for i in range(NUM_E_EP):
#     state_ = state.State(
#         [0] * 8,
#         [0] * 8,
#         index_to_e_ep(i) + [0] * 8,
#         [0] * 12,
#     )
#     for i_move, move_name in enumerate(move_names_ph2):
#         new_state = state_.apply_move(moves[move_name])
#         e_ep_move_table[i][i_move] = e_ep_to_index(new_state.ep[:4])
# print(f"Finished! ({time.time() - start:.5f} sec.)")

# """Phase1の枝刈り表"""
# """EOを無視して、COとE列だけ考えたときの最短手数表"""
# print("Computing co_eec_prune_table")
# start = time.time()
# co_eec_prune_table = [[-1] * NUM_E_COMBINATIONS for _ in range(NUM_CO)]
# co_eec_prune_table[0][0] = 0
# distance = 0
# num_filled = 1
# while num_filled != NUM_CO * NUM_E_COMBINATIONS:
#     print(f"distance = {distance}")
#     print(f"num_filled = {num_filled}")
#     for i_co in range(NUM_CO):
#         for i_eec in range(NUM_E_COMBINATIONS):
#             if co_eec_prune_table[i_co][i_eec] == distance:
#                 for i_move in range(len(move_names)):
#                     next_co = co_move_table[i_co][i_move]
#                     next_eec = e_combination_table[i_eec][i_move]
#                     if co_eec_prune_table[next_co][next_eec] == -1:
#                         co_eec_prune_table[next_co][next_eec] = distance + 1
#                         num_filled += 1
#     distance += 1
# print(f"Finished! ({time.time() - start:.5f} sec.)")

# """COを無視して、EOとE列だけ考えたときの最短手数表"""
# print("Computing eo_eec_prune_table")
# start = time.time()
# eo_eec_prune_table = [[-1] * NUM_E_COMBINATIONS for _ in range(NUM_EO)]
# eo_eec_prune_table[0][0] = 0
# distance = 0
# num_filled = 1
# while num_filled != NUM_EO * NUM_E_COMBINATIONS:
#     print(f"distance = {distance}")
#     print(f"num_filled = {num_filled}")
#     for i_eo in range(NUM_EO):
#         for i_eec in range(NUM_E_COMBINATIONS):
#             if eo_eec_prune_table[i_eo][i_eec] == distance:
#                 for i_move in range(len(move_names)):
#                     next_eo = eo_move_table[i_eo][i_move]
#                     next_eec = e_combination_table[i_eec][i_move]
#                     if eo_eec_prune_table[next_eo][next_eec] == -1:
#                         eo_eec_prune_table[next_eo][next_eec] = distance + 1
#                         num_filled += 1
#     distance += 1
# print(f"Finished! ({time.time() - start:.5f} sec.)") 

# """Phase2の枝刈り表"""
# """UD面のエッジを無視して、CPとE列エッジだけ揃えるときの最短手数表"""
# print("Computing cp_eep_prune_table")
# start = time.time()
# cp_eep_prune_table = [[-1] * NUM_E_EP for _ in range(NUM_CP)]
# cp_eep_prune_table[0][0] = 0
# distance = 0
# num_filled = 1
# while num_filled != NUM_CP * NUM_E_EP:
#     print(f"distance = {distance}")
#     print(f"num_filled = {num_filled}")
#     for i_cp in range(NUM_CP):
#         for i_eep in range(NUM_E_EP):
#             if cp_eep_prune_table[i_cp][i_eep] == distance:
#                 for i_move in range(len(move_names_ph2)):
#                     next_cp = cp_move_table[i_cp][i_move]
#                     next_eep = e_ep_move_table[i_eep][i_move]
#                     if cp_eep_prune_table[next_cp][next_eep] == -1:
#                         cp_eep_prune_table[next_cp][next_eep] = distance + 1
#                         num_filled += 1
#     distance += 1
# print(f"Finished! ({time.time() - start:.5f} sec.)")

# """CPを無視して、UD面のエッジとE列エッジだけ揃えるときの最短手数表"""
# print("Computing udep_eep_prune_table")
# start = time.time()
# udep_eep_prune_table = [[-1] * NUM_E_EP for _ in range(NUM_UD_EP)]
# udep_eep_prune_table[0][0] = 0
# distance = 0
# num_filled = 1
# while num_filled != NUM_UD_EP * NUM_E_EP:
#     print(f"distance = {distance}")
#     print(f"num_filled = {num_filled}")
#     for i_udep in range(NUM_UD_EP):
#         for i_eep in range(NUM_E_EP):
#             if udep_eep_prune_table[i_udep][i_eep] == distance:
#                 for i_move in range(len(move_names_ph2)):
#                     next_udep = ud_ep_move_table[i_udep][i_move]
#                     next_eep = e_ep_move_table[i_eep][i_move]
#                     if udep_eep_prune_table[next_udep][next_eep] == -1:
#                         udep_eep_prune_table[next_udep][next_eep] = distance + 1
#                         num_filled += 1
#     distance += 1
# print(f"Finished! ({time.time() - start:.5f} sec.)") 