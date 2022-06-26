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

"""メイン関数"""
if __name__ == '__main__':
    solved_state = State(
    [0, 1, 2, 3, 4, 5, 6, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )

    r_state = State(
    [0, 2, 6, 3, 4, 1, 5, 7],
    [0, 1, 2, 0, 0, 2, 1, 0],
    [0, 5, 9, 3, 4, 2, 6, 7, 8, 1, 10, 11],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )

    r2_state = r_state.apply_move(r_state)
    print(f"r2_state.cp = {r2_state.cp}")
    print(f"r2_state.co = {r2_state.co}")
    print(f"r2_state.ep = {r2_state.ep}")
    print(f"r2_state.eo = {r2_state.eo}")

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

    # スクランブル
    scramble = "L D2 R U2 L F2 U2 L F2 R2 B2 R U' R' U2 F2 R' D B' F2"
    
    # スクランブルを構成する操作を1手ずつ順に適用する
    scrambled_state = solved_state
    for move_name in scramble.split(" "):
      move_state = moves[move_name]
      scrambled_state = scrambled_state.apply_move(move_state)

    # あっているかチェック
    print(f"scrambled_state.cp = {scrambled_state.cp}")
    print(f"scrambled_state.co = {scrambled_state.co}")
    print(f"scrambled_state.ep = {scrambled_state.ep}")
    print(f"scrambled_state.eo = {scrambled_state.eo}")

