def create_board(size=10):
    """创建一个指定大小的空棋盘"""
    # 使用 '+' 表示棋盘上的交叉点空位
    return [['+' for _ in range(size)] for _ in range(size)]

def print_board(board):
    """在控制台打印棋盘"""
    size = len(board)
    
    # 打印列号 (0-9)
    print("  " + " ".join(str(i) for i in range(size)))
    
    # 打印行号和棋盘内容
    for i in range(size):
        print(f"{i} " + " ".join(board[i]))

# 主程序
if __name__ == "__main__":
    # 初始化 10x10 棋盘
    board_size = 10
    game_board = create_board(board_size)
    
    # 显示棋盘
    print_board(game_board)
