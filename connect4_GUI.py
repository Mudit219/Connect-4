import pygame
import numpy as np

from pygame import mixer

ROW_COUNT = 6
COL_COUNT = 7
count1 = [0,0,0,0]
count2 = [0,0,0,0]

RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
CYAN = (0,255,255)
GREY = (47,79,79)
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

#   It is a simple task to draw, just enter the screen,color,position & size. For rect we give top coordinate and the height and width of rect. For circle we give center and radius.
# Just remember top left corner represents the (0,0) pixel
def draw_board(board):
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen,CYAN,(c*SQUARESIZE,r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
            if(board[r][c] == 0):
                pygame.draw.circle(screen,BLACK,(c*SQUARESIZE+int(SQUARESIZE/2),r*SQUARESIZE+SQUARESIZE+int(SQUARESIZE/2)),RADIUS)
            elif(board[r][c] == 1):
                pygame.draw.circle(screen,RED,(c*SQUARESIZE+int(SQUARESIZE/2),r*SQUARESIZE+SQUARESIZE+int(SQUARESIZE/2)),RADIUS)
            elif(board[r][c] == 2):
                pygame.draw.circle(screen,YELLOW,(c*SQUARESIZE+int(SQUARESIZE/2),r*SQUARESIZE+SQUARESIZE+int(SQUARESIZE/2)),RADIUS)
    pygame.display.update() # DO NOT remove, otherwise last piece will not be seen.


game_over = False
turn = 0
board = create_board()
visited = create_board()
print(board)

pygame.init()
SQUARESIZE = 100  # This is not the area, it is the side
RADIUS = int(SQUARESIZE/2 - 5)

width = COL_COUNT*SQUARESIZE
height = (ROW_COUNT+1)*SQUARESIZE
size = (width,height)
screen = pygame.display.set_mode(size)  # Need to initalise the screen
draw_board(board)
myfont = pygame.font.SysFont("monospace",75)

while not game_over:

    pygame.display.update()    
    #Ask for player 1 input
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            quit()

        if(event.type == pygame.MOUSEMOTION):
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE)) # Basically color the prev location black as we move the mouse
            posx = event.pos[0]
            if(turn == 0):
                pygame.draw.circle(screen,RED,(posx,int(SQUARESIZE/2)),RADIUS)
            else:
                pygame.draw.circle(screen,YELLOW,(posx,int(SQUARESIZE/2)),RADIUS)
        
        if(event.type == pygame.MOUSEBUTTONDOWN):
            # print(event.pos)  # Run and click anywhere on screen u get coordinates.
            if(turn == 0):
                posx = event.pos[0]
                col = int(posx/SQUARESIZE)
                # print(col)
                # print(type(col))
                if(is_valid_location(board,col)):
                    row = row_available(board,col)
                    drop_piece(board,col,row,1)
                    pygame.draw.circle(screen,YELLOW,(posx,int(SQUARESIZE/2)),RADIUS)
                    check_winner(board,row,col,1)
                    # print("count1:", count1[1])
                    for i in count1:
                        if(i >= 4):
                            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE)) # When it renders the winner I dont want the colored ball to be visible
                            label = myfont.render("Player 1 WINS!!!",1,RED,BLACK)
                            screen.blit(label,(40,10)) # Update the specific part of screen
                            pygame.display.update()
                            game_over = True
            
        #Ask for player 2 input
            else:
                posx = event.pos[0]
                col = int(posx/SQUARESIZE)
                # print(col)
                if(is_valid_location(board,col)):
                    row = row_available(board,col)
                    drop_piece(board,col,row,2)
                    pygame.draw.circle(screen,RED,(posx,int(SQUARESIZE/2)),RADIUS)
                    check_winner(board,row,col,2)
                    # print("count2:", count2[1])
                    for i in count2:
                        if(i >= 4):
                            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
                            label = myfont.render("Player 2 WINS!!!",1,YELLOW,BLACK)
                            screen.blit(label,(40,10))
                            pygame.display.update()
                            game_over = True
            # After the mouse button is clicked we print the board and change the turn
            print(board)       
            draw_board(board)     
            turn += 1
            turn = turn%2
            
            if(game_over == True):
                pygame.time.wait(3000)
