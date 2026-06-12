import os

BOARD_SIZE = 15
EMPTY = "."
P1 = "X"  # 玩家 1
P2 = "O"  # 玩家 2

def create_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# 核心修改：让所有字符严格占用相同的宽度（3个字符宽）
def print_board(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # 打印顶部列坐标，每个数字占3个位置并居中
    header = "   " + "".join([f"{i}".center(3) for i in range(BOARD_SIZE)])
    print(header)
    
    # 打印棋盘内容
    for r in range(BOARD_SIZE):
        # 行坐标占3个位置，靠左对齐
        row_str = f"{r}".ljust(3)
        for c in range(BOARD_SIZE):
            # 每一个棋子或空位都居中占用3个位置
            row_str += board[r][c].center(3)
        print(row_str)
        
    print("-" * (BOARD_SIZE * 3 + 4))

def check_win(board, r, c, piece):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        nr, nc = r + dr, c + dc
        while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == piece:
            count += 1
            nr, nc = nr + dr, nc + dc
        nr, nc = r - dr, c - dc
        while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == piece:
            count += 1
            nr, nc = nr - dr, nc - dc
        if count >= 5:
            return True
    return False

def play_game():
    board = create_board()
    current_player = P1
    player_name = "玩家 1 (X)"
    
    while True:
        print_board(board)
        while True:
            try:
                user_input = input(f"请【{player_name}】输入落子坐标 (行,列)，例如 7,8: ")
                r, c = map(int, user_input.split(","))
                
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if board[r][c] == EMPTY:
                        board[r][c] = current_player
                        break
                    else:
                        print("❌ 这个位置已经有棋子了，换一个！")
                else:
                    print(f"❌ 坐标超出范围了，请输入 0 到 {BOARD_SIZE-1} 之间的数字。")
            except ValueError:
                print("❌ 输入格式错误！记得用英文逗号隔开，比如: 7,8")
        
        if check_win(board, r, c, current_player):
            print_board(board)
            print(f"🎉 恭喜【{player_name}】赢了！绝杀比赛！")
            break
            
        if current_player == P1:
            current_player = P2
            player_name = "玩家 2 (O)"
        else:
            current_player = P1
            player_name = "玩家 1 (X)"

if __name__ == "__main__":
    play_game()
