import pygame
import math
import random
from queue import PriorityQueue

WIDTH = 800
#SETTING DIMENSIONS OF THE WINDOW
WIN = pygame.display.set_mode((WIDTH,WIDTH)) 
pygame.display.set_caption("A* Path Finding Algorithm")
#SOME COLORS
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)

class Spot:
    def __init__(self, row, col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows
        
    def get_pos(self):
        return self.row, self.col    
        
    def is_closed(self):
        return self.color == RED
    def is_open(self):
        return self.color ==  GREEN
    def is_barrier(self):
        return self.color == BLACK   
    def is_start(self):
        return self.color ==  ORANGE  
    def is_end(self):
        return self.color == TURQUOISE
    
    
    def reset(self):
        self.color = WHITE
        
    def make_closed(self):
        self.color = RED
        
    def make_start(self):
        self.color = ORANGE
        
    def make_open(self):
        self.color =  GREEN
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_end(self):
        self.color = TURQUOISE
        
    def make_path(self):
        self.color = PURPLE
        
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x , self.y,self.width,self.width))
        
    def update_neighbour(self,grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier():# DOWN
            self.neighbours.append(grid[self.row + 1][self.col])
            
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():#UP
            self.neighbours.append(grid[self.row - 1][self.col])
            
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier(): #RIGHT
            self.neighbours.append(grid[self.row ][self.col+ 1])
            
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): #LEFT
            self.neighbours.append(grid[self.row ][self.col-1])
    def __lt__(self, other):
        return False
    
    
def h(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current , draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count, start))
    came_from = {}
    g_score = {spot : float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot : float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    open_set_hash = {start}
    
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
                
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True
        
        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
                
        draw()
        if current != start:
            current.make_closed()
            
    return False 
                
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i , j , gap , rows)
            grid[i].append(spot)
    
    return grid 


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0,i*gap),(width, i*gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j*gap, 0),(j*gap, width))


def draw(win , grid, rows, width):
    win.fill(WHITE)
    
    for row in grid:
        for spot in row:
            spot.draw(win)
            
            
    draw_grid(win, rows, width)
    pygame.display.update()
    
    

    
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row , col


### ADDED PORTION ###
### Making Custom Maze by passing list 
def draw_maze(grid, POS_OF_WALLS):
    for row,col in POS_OF_WALLS:
        spot = grid[row][col]
        spot.make_barrier()
        
    return 0;


### used AI for maze generation implementation
def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0  
    
    walls = [(start_x + dx, start_y + dy) for dx, dy in [(2, 0), (0, 2)] if 0 <= start_x + dx < width and 0 <= start_y + dy < height]
    random.shuffle(walls)
    
    while walls:
        x, y = walls.pop()
        if maze[y][x] == 1:
            neighbors = []
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 0:
                    neighbors.append((nx, ny))
            
            if neighbors:
                nx, ny = random.choice(neighbors)
                maze[(y + ny) // 2][(x + nx) // 2] = 0
                maze[y][x] = 0
                for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                    wx, wy = x + dx, y + dy
                    if 0 <= wx < width and 0 <= wy < height and maze[wy][wx] == 1:
                        walls.append((wx, wy))
                random.shuffle(walls)
    
    wall_list = []
    for row in range(height):
        for col in range(width):
            if maze[row][col] == 1:
                wall_list.append([col + 1, row + 1])  

    return wall_list




def main(win, width):
    ROWS = 50 
    grid = make_grid(ROWS, width)
    
    start = None
    end = None
    
    run = True
    # WALLS = [[1,2],[3,4]] for custom mazes add points representing walls as shown
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run == False    
                pygame.quit()
                return

            ####ADDED PORTION####
            spot = grid[3][3]##will make changes later
            start = spot
            start.make_start()
            spot = grid[ROWS-2][ROWS-2]##will make changes later
            end = spot
            end.make_end()

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                
                elif spot != end and spot != start:
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE and start and end):
                    for row in grid:
                        for spot in row:
                            spot.update_neighbour(grid)
                            
                    algorithm(lambda: draw(win, grid,ROWS ,width), grid, start, end)
                    
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS,width)     
                if event.key == pygame.K_d:
                    WALLS = generate_maze(49, 49)
                    draw_maze(grid, WALLS)
                if event.key == pygame.K_q:
                    run == False    
                    pygame.quit()
                    return
 
    pygame.display.quit()                                            
    pygame.quit()
    
    
main(WIN, WIDTH)