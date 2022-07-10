import numpy as np
ROW_COUNT = 6
COL_COUNT = 7
count1 = [0,0,0,0]
count2 = [0,0,0,0]

def create_board(): # Create a matrix of all zeroes
    board = np.zeros((ROW_COUNT,COL_COUNT))
    return board

def drop_piece(board,col,row,piece):
    board[row][col] = piece

def is_valid_location(board,col):
    return board[0][col] == 0   # All we need to check is the top row has zero or not

def row_available(board,col):
    for r in reversed(range(ROW_COUNT)):
        if(board[r][col] == 0):
            return r

def bound_check(board,row,col,piece):
    if(row >= 0 and col >= 0 and row < ROW_COUNT and col < COL_COUNT and board[row][col] == piece and visited[row][col] == 0):
        return True

def left_right(board,row,col,piece):
    if(not(bound_check(board,row,col,piece))):
        return
    global count1,count2
    if(piece == 1):
        count1[0] +=1
    if(piece == 2):
        count2[0] +=1
    global visited
    visited[row][col] = 1
    left_right(board,row,col-1,piece)
    left_right(board,row,col+1,piece)
    visited[row][col] = 0   # Very imp condition.Suppose we do not get winner in left_right then we want to check other cases also but everything should be reset to zero.

def top_down(board,row,col,piece):
    if(not(bound_check(board,row,col,piece))):
        return
    global count1,count2
    if(piece == 1):
        count1[1] +=1
    if(piece == 2):
        count2[1] +=1
    global visited
    visited[row][col] = 1
    top_down(board,row-1,col,piece)
    top_down(board,row+1,col,piece)
    visited[row][col] = 0

def diagonal1(board,row,col,piece):
    if(not(bound_check(board,row,col,piece))):
        return
    global count1,count2
    if(piece == 1):
        count1[2] +=1
    if(piece == 2):
        count2[2] +=1
    global visited
    visited[row][col] = 1
    diagonal1(board,row-1,col-1,piece)
    diagonal1(board,row+1,col+1,piece)
    visited[row][col] = 0

def diagonal2(board,row,col,piece):
    if(not(bound_check(board,row,col,piece))):
        return
    global count1,count2
    if(piece == 1):
        count1[3] +=1
    if(piece == 2):
        count2[3] +=1
    global visited
    visited[row][col] = 1
    diagonal2(board,row+1,col-1,piece)
    diagonal2(board,row-1,col+1,piece)
    visited[row][col] = 0

def check_winner(board,row,col,piece):
    global count1,count2,visited
    count1 = [0,0,0,0]  # At each turn we have to set count to zero
    count2 = [0,0,0,0]
    # Here we are checking all the nearby place where we can get 4 same piece consecutively at each turn(for both players).
    left_right(board,row,col,piece)
    top_down(board,row,col,piece)
    # print("visited:\n", visited)
    diagonal1(board,row,col,piece)
    diagonal2(board,row,col,piece)

game_over = False
turn = 0
board = create_board()
visited = create_board()
print(board)
while not game_over:

    #Ask for player 1 input
    if(turn == 0):
        col = int(input("Player 1 make your choice (0,6):"))
        # print(col)
        # print(type(col))
        if(is_valid_location(board,col)):
            row = row_available(board,col)
            drop_piece(board,col,row,1)
            check_winner(board,row,col,1)
            # print("count1:", count1[1])
            for i in count1:
                if(i >= 4):
                    print("Player 1 Wins")
                    game_over = True
    
    #Ask for player 2 input
    else:
        col = int(input("Player 2 make your choice (0,6):"))
        # print(col)
        if(is_valid_location(board,col)):
            row = row_available(board,col)
            drop_piece(board,col,row,2)
            check_winner(board,row,col,2)
            # print("count2:", count2[1])
            for i in count2:
                if(i >= 4):
                    print("Player 2 Wins")
                    game_over = True
    
    turn += 1
    turn = turn%2
    print(board)
