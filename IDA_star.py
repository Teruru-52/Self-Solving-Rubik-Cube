import time

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

def is_solved(state):
    return (state.eo == [0] * 12  # EOが全部揃っている
        and state.co == [0] * 8  # COが全部揃っている
        and state.ep == list(range(12))  # EPが全部揃っている
        and state.cp == list(range(8))  # CPが全部揃っている
    )

# 対面を引くdict
inv_face = {
    "U": "D",
    "D": "U",
    "L": "R",
    "R": "L",
    "F": "B",
    "B": "F"
}

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

def count_solved_corners(state):
    """
    揃っているコーナーの個数をカウント
    """
    return sum([state.cp[i] == i and state.co[i] == 0 for i in range(8)])

def count_solved_edges(state):
    """
    揃っているエッジの個数をカウント
    """
    return sum([state.ep[i] == i and state.eo[i] == 0 for i in range(12)])
    
def prune(depth, state):
    """
    それ以上探索を進めても無意味ならTrueを返す
    """
    if depth == 1 and (count_solved_corners(state) < 4 or count_solved_edges(state) < 8):
        # 残り1手で揃っているコーナーが4個未満、もしくは、揃っているエッジが8個未満ならもう揃わない
        return True
    if depth == 2 and count_solved_edges(state) < 4:
        # 残り2手で揃っているエッジが4個未満ならもう揃わない
        return True
    if depth == 3 and count_solved_edges(state) < 2:
        # 残り3手で揃っているエッジが2個未満ならもう揃わない
        return True
    return False

class Search:
    def __init__(self):
        self.current_solution = []  # 今探索している手順を入れておくstack

    def depth_limited_search(self, state, depth):
        if depth == 0 and is_solved(state):
            # is_solvedがTrueなら完成しているので解が見つかったということでTrueを返す
            # depth==0はなくてもいいが、depth > 0には解がないことがすでにわかっているのでいちいち判定関数を呼ぶ必要はない
            return True
        if depth == 0:  # depth 0 までたどり着いたのに解が見つからなかったらFalseを返す
            return False
        # 枝刈り
        if prune(depth, state):
            return False

        # depth=0まで探索を続ける
        prev_move = self.current_solution[-1] if self.current_solution else None  # 1手前の操作
        for move_name in move_names:
            if not is_move_available(prev_move, move_name):
                continue
            self.current_solution.append(move_name)
            if self.depth_limited_search(state.apply_move(moves[move_name]), depth - 1):
                return True
            self.current_solution.pop()

    def start_search(self, state, max_length=20):
        for depth in range(0, max_length):  # 0から次第にに手数を増やしながら深さ制限探索を繰り返す
            print(f"# Start searching length {depth}")
            if self.depth_limited_search(state, depth):
                # 解が見つかったらその時点でそれを返却
                return " ".join(self.current_solution)
        return None

"""メイン関数"""
if __name__ == '__main__':
    scramble = "R U R' F2 D2 L"
    scrambled_state = scamble2state(scramble)
    search = Search()
    start = time.time()
    solution = search.start_search(scrambled_state)
    print(f"Finished! ({time.time() - start:.2f} sec.)")
    if solution:
      print(f"Solution: {solution}.")
    else:
      print("Solution not found.")