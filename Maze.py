# install pygame > pip install pygame

# [Right click] remove spot 
# [Left click] set a spot
# [SPACE] start A* 
# [C] clear

import pygame
import math
from queue import PriorityQueue

from GUI import Button
# width of the screen x*x
WIDTH = 800
# create the window 
WIN = pygame.display.set_mode((WIDTH,WIDTH+60))
pygame.display.set_caption("Path Finding Algorithm")

# Colors
L_GREEN = (115, 198, 0 )
GREEN = (69, 179, 157 )
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (46, 64, 83 )
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (169, 50, 38 )
RED = (203, 67, 53)


pygame.init()

A_star_btn = Button((WIDTH)-150,WIDTH+5,100,50,WHITE,"A *")
# DFS_btn = Button((WIDTH)-300,WIDTH+5,100,50,WHITE,"DFS")
CLEAR_btn = Button((WIDTH)-300,WIDTH+5,100,50,RED,"CLEAR")
A_star_btn.draw(WIN)
# DFS_btn.draw(WIN)
CLEAR_btn.draw(WIN)


# Node class or Spots 

class Spot:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

        # return position of the node (x,y)
    def get_pos(self):
        return self.row,self.col
    # this set the node checked        
    def is_closed(self):
        return self.color == L_GREEN
    def is_open(self):
        return self.color == GREEN
    def is_barrier(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == ORANGE
    def is_end(self):
        return self.color == PURPLE
    def reset(self):
        self.color = WHITE
    def make_start(self):
        self.color = ORANGE
    def make_closed(self):
        self.color = L_GREEN # the one inside
    def make_open(self):
        self.color = GREEN
    def make_barrier(self):
        self.color = BLACK
    def make_end(self):
        self.color = RED
    def make_path(self):
        self.color = PURPLE

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    
    def update_neighbors(self,grid):
        self.neighbors = []
        # Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row +1][self.col])
        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])
        # Left
        if self.col > 0  and not grid[self.row][self.col -1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])
        

    def __lt__(self,other):
        return False
        


def reconstruct_path(came_from,current,draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        
        draw()

def A_STAR(draw,grid,start,end):
    # herstic function take 2 points and return the distance  
    def h(p1,p2):
        x1,y1 = p1
        x2,y2 = p2
        return abs(x1-x2) + abs(y1-y2)
    
    # initialize the variables 
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start))   
    came_form = {}
    # a dictionary to store a g_score for all spots
    g_score = {spot:float('inf') for row in grid for spot in row}
    g_score[start]  = 0
    f_score = {spot:float('inf') for row in grid for spot in row}
    f_score[start] = h(start.get_pos(),end.get_pos())

    open_set_hash = {start}

    # while there is spots to check keep searching for end
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if CLEAR_btn.handle_event(event):
                return False
        # open set index 2 where the spot stored
        current = open_set.get()[2]
        # we remove the spot
        open_set_hash.remove(current)

        # if we reach the end display the path 
        if current == end:
            reconstruct_path(came_form,end,draw)
            end.make_end()
            start.make_start()
            return True

        # check neighbors
        for neighbor in current.neighbors:
            # get the current node g-score
            temp_g_score = g_score[current] + 1
            # we look for a neighbor closer then the current node 
            if temp_g_score < g_score[neighbor]:
                # add it to path
                came_form[neighbor] = current
                # update the g_score 
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(),end.get_pos())
                # if spot not added to the open set hash add it
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor],count,neighbor)) 
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                
        draw()
        # color it to green | closed that the node is considered
        if current != start:
            current.make_closed()
    # false we couldn't find the end
    return False


def make_grid(rows,width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)
    return grid

        
def draw_grid(win,rows,width):
    gap = width // rows
    for i in range(rows+1):
        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))
        for j in range(rows):
            pygame.draw.line(win,GREY,(j*gap,0),(j*gap,width))


def draw(win,grid,rows,width):
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win,rows,width)
    pygame.display.update()


def get_clicked_pos(pos,rows,width):
    gap = width//rows
    y,x = pos
    row = y // gap
    col = x // gap
    return row ,col




def main(win,width):
    ROWS = 50
    grid = make_grid(ROWS,width)
    start = None
    end = None
    run = True
    started = False
    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue    

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                try:
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()
                    elif not end and spot != start:
                        end = spot
                        end.make_end()
                    elif spot != end and spot != start:
                        spot.make_barrier()
                except:
                    pass

            elif pygame.mouse.get_pressed()[2]:#RIGHT
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                try:
                    spot = grid[row][col]
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None 
                    spot.reset()
                except:
                    pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS,width)
                
            if start and end:
                if A_star_btn.handle_event(event):
                    # update all the neighbors of all spots in the grid
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    A_STAR(lambda: draw(win,grid,ROWS,width),grid,start,end)
                elif CLEAR_btn.handle_event(event):
                    start = None
                    end = None
                    grid = make_grid(ROWS,width)


    pygame.quit()


main(WIN,WIDTH)