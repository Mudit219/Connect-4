Things to remember:

-> Command Line:
    - We are using numpy to make matrix(board)
    - For both players we will insert their piece in matrix        according to column(if column is not full)
    - If a player gets 4 consecutive same piece, he wins.
    - For winning condition reccursion is used at every turn of both players.
    - At every turn we are checking all neigbours of the last piece added(whether we get 4 consecutive) in each direction left_right,top_down,diagonal1,diagonal2.

-> Graphical Interface:
    - Firstly create a display screen correspondingly to row and column.
    - Use pygame.event.get() to get all the events(keypress,mouse movement,mouse click,etc.)
    - Now instead of type input(as we did in CLI) we will take input graphically(using MOUSEBUTTONDOWN), such that we can store the coordinates where we click the mouse.
    - Now once you get coordinates adjust it according to our col(used in CLI)
    - To color or game screen pygame.draw is used, for each row and col we draw square,circle,line....(with colors, postion and dimensions) whichever is required.
    - For rendering(writing on screen) we use pygame.font.SysFont(name,size)
    - Do not forget to call the function implemented
    - Just make sure whenever there is a feature is added display.update() should be there for it, otherwise our screen might not update it.

https://www.pygame.org/docs/ 