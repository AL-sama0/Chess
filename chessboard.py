import os

# 初始化一个 15x15 的棋盘（终端下 15x15 视觉体验最好）
BOARD_SIZE = 15
EMPTY = "."
PLAYER = "X"  # 人类是 X
AI = "O"      # AI 是 O

def create_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# 打印棋盘（带坐标轴，方便你看坐标输入）
def print_board(board):
    os.system('cls' if os.name == 'nt' else 'clear') # 刷新屏幕，看起来更像游戏
    print("   " + " ".join([f"{i:2d}" for i in range(BOARD_SIZE)]))
    for r in range(BOARD_SIZE):
        print(f"{r:2d} ", end="")
        for c in range(BOARD_SIZE):
            print(f" {board[r][c]}", end="")
        print()
    print("-" * 50)

# 检查是否连成 5 个（判断输赢）
def check_win(board, r, c, piece):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        # 正向数
        nr, nc = r + dr, c + dc
        while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == piece:
            count += 1
            nr, nc = nr + dr, nc + dc
        # 反向数
        nr, nc = r - dr, c - dc
        while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == piece:
            count += 1
            nr, nc = nr - dr, nc - dc
        if count >= 5:
            return True
    return False

# AI 评估某个位置分数的“大脑” (沿用我们之前的启发式核心原理)
def evaluate_position(board, r, c):
    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    # 攻防权重表
    # (连子数, 是否两端空) -> 分数
    for dr, dc in directions:
        ai_count = 0
        player_count = 0
        
        # 探测 AI (O) 能连几个
        for i in range(1, 5):
            nr, nc = r + i*dr, c + i*dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == AI:
                ai_count += 1
            else: break
        for i in range(1, 5):
            nr, nc = r - i*dr, c - i*dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == AI:
                ai_count += 1
            else: break
            
        # 探测 人类 (X) 能连几个
        for i in range(1, 5):
            nr, nc = r + i*dr, c + i*dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == PLAYER:
                player_count += 1
            else: break
        for i in range(1, 5):
            nr, nc = r - i*dr, c - i*dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == PLAYER:
                player_count += 1
            else: break

        # 简单的打分逻辑：绝杀 > 强防 > 强攻
        if ai_count >= 4: score += 100000     # AI 马上赢
        elif player_count >= 4: score += 20000 # 人类马上赢，必须堵
        elif ai_count == 3: score += 5000      # AI 做活4
        elif player_count == 3: score += 2000  # 堵人类活3
        else: score += (ai_count * 10 + player_count * 5)
        
    # 越靠近中心，基础分稍高一点
    center = BOARD_SIZE / 2
    score += (10 - abs(r - center) - abs(c - center))
    return score

# AI 决定下在哪里
def get_ai_move(board):
    best_score = -1
    best_move = None
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == EMPTY:
                score = evaluate_position(board, r, c)
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
    return best_move

# 主游戏循环
def play_game():
    board = create_board()
    print_board(board)
    
    while True:
        # --- 人类回合 ---
        while True:
            try:
                # 提示输入类似 "7,8" 的坐标
                user_input = input("请输入你的坐标 (行,列)，例如 7,8: ")
                r, c = map(int, user_input.split(","))
                
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if board[r][c] == EMPTY:
                        board[r][c] = PLAYER
                        break
                    else:
                        print("这个位置已经有棋子了，换一个！")
                else:
                    print(f"坐标超出范围了，请输入 0 到 {BOARD_SIZE-1} 之间的数字。")
            except ValueError:
                print("输入格式错误！记得用英文逗号隔开，比如: 7,8")
        
        print_board(board)
        if check_win(board, r, c, PLAYER):
            print("🎉 卧槽你居然赢了！太强了吧！")
            break
            
        # --- AI 回合 ---
        print("AI 正在思考...")
        ai_r, ai_c = get_ai_move(board)
        board[ai_r][ai_c] = AI
        
        print_board(board)
        print(f"🤖 AI 下在了坐标: {ai_r},{ai_c}")
        
        if check_win(board, ai_r, ai_c, AI):
            print("💀 哎呀，你被 AI 乱杀了，胜败乃兵家常事，再来一把！")
            break

if __name__ == "__main__":
    play_game()
