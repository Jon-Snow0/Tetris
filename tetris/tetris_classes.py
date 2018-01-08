#########################################
# Programmer: Mrs.G
# Date: 04/12/2016
# File Name: tetris_classes3.py
# Description: These classes form the third and final class template for our Tetris game.
#########################################
import pygame
#colors
BLACK     = (  0,  0,  0)                       
RED       = (255,  0,  0)                     
GREEN     = (  0,255,  0)                     
BLUE      = (  0,  0,255)                     
ORANGE    = (255,127,  0)               
CYAN      = (  0,183,235)                   
MAGENTA   = (255,  0,255)                   
YELLOW    = (255,255,  0)
WHITE     = (255,255,255)
#list of colors and list of their names
COLOURS   = [ BLACK,  RED,  GREEN,  BLUE,  ORANGE,  CYAN,  MAGENTA,  YELLOW,  WHITE ]
CLR_names = ['black','red','green','blue','orange','cyan','magenta','yellow','white']
#list of letters representing the different tetriminos
FIGURES   = [  None , 'Z' ,  'S'  ,  'J' ,  'L'   ,  'I' ,   'T'   ,   'O'  , None  ]
#loading the images for the shapes
tetriminos=[]
for i in range(7):
    tetriminos.append(pygame.image.load('tetriminos'+str(i+1)+'.png'))
class Block(object):                    
    """ A square - basic building block
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        #sets each object's x, y, and color according to the parameters taken
        self.col = col                  
        self.row = row                  
        self.clr = clr

    def __str__(self):
        #returns a string of the shape's x and y position as well as its color
        return '('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def __eq__(self, other):
        #special method checking if one object's position is the same as another's
        return self.col==other.col and self.row==other.row
    
    def draw(self, surface, gridsize=20):
        #draws the blocks of the walls and the shapes on the surface
        x = self.col * gridsize        
        y = self.row * gridsize
        CLR = COLOURS[self.clr]
        if self.clr==0 or self.clr ==8:
            pygame.draw.rect(surface,CLR,(x,y,gridsize,gridsize), 0)
            pygame.draw.rect(surface, WHITE,(x,y,gridsize+1,gridsize+1), 1)
        else:
            tetriminos[self.clr-1] = tetriminos[self.clr-1].convert_alpha()
            tetriminos[self.clr-1] = pygame.transform.scale(tetriminos[self.clr-1], (gridsize,gridsize))
            surface.blit(tetriminos[self.clr-1], (x,y))
            pygame.draw.rect(surface, WHITE,(x,y,gridsize+1,gridsize+1), 1)
        
        

    def sdraw(self, surface, gridsize=20):
        #draws the shadow's outline on the surface
        x = self.col * gridsize        
        y = self.row * gridsize
        CLR = COLOURS[self.clr]
        pygame.draw.rect(surface, CLR,(x,y,gridsize,gridsize), 1)

    def move_down(self):
        #moves the shape down
        self.row = self.row + 1   
               

#---------------------------------------#
class Cluster(object):
    """ Collection of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        #sets each object's column, row, and # of blocks according to the parameters taken
        self.col = col                    
        self.row = row                   
        self.clr = 0                          
        self.blocks = [Block()]*blocksNo      
        self._colOffsets = [0]*blocksNo  
        self._rowOffsets = [0]*blocksNo
        
    def _update(self):
        #sets each block in the cluster to the corresponding position in relation to the anchor block
        for i in range(len(self.blocks)):
            blockCOL = self.col+self._colOffsets[i] 
            blockROW = self.row+self._rowOffsets[i] 
            blockCLR = self.clr
            self.blocks[i]= Block(blockCOL, blockROW, blockCLR)

    def draw(self, surface, gridsize):
        #draws each block of the shape individually using the block cluster's draw method
        for block in self.blocks:
            block.draw(surface, gridsize)
    def sdraw(self, surface, gridsize):
        #draws each block of the shadow individually using the block cluster's draw method
        for block in self.blocks:
            block.sdraw(surface, gridsize)

    def collides(self, other):
        #checks if any block in the shape collides with another block using the eq method
        """ Compare each block from a cluster to all blocks from another cluster.
            Return True only if there is a location conflict.
        """
        for block in self.blocks:
            for obstacle in other.blocks:
                if block==obstacle:
                    return True
        return False
    
    def append(self, other):
        #appends one cluster object with its attributes to another 
        """ Append all blocks from another cluster to this one.
        """
        self.blocks.extend(other.blocks)
        self._colOffsets.extend(other._colOffsets)  
        self._rowOffsets.extend(other._rowOffsets)  
        

#---------------------------------------#
class Obstacles(Cluster):
    """ Collection of tetrominoe blocks on the playing field, left from previous shapes.
        
    """        
    def __init__(self, col = 0, row = 0, blocksNo = 0):
        Cluster.__init__(self, col, row, blocksNo)      # initially the playing field is empty(no shapes are left inside the field)'

    def findFullRows(self, top, bottom, columns):
        fullRows = []
        rows = []
        for block in self.blocks:                       
            rows.append(block.row)                      # make a list with only the row numbers of all blocks
            
        for row in range(top, bottom):                  # starting from the top (row 0), and down to the bottom
            if rows.count(row) == columns:              # if the number of blocks with certain row number
                fullRows.append(row)                    # equals to the number of columns -> the row is full
        return fullRows                                 # return a list with the full rows' numbers


    def removeFullRows(self, fullRows):
        for row in fullRows:                            # for each full row, STARTING FROM THE TOP (fullRows are in order)
            for i in reversed(range(len(self.blocks))): # check all obstacle blocks in REVERSE ORDER,
                                                        # so when popping them the index doesn't go out of range !!!
                if self.blocks[i].row == row:
                    self.blocks.pop(i)                  # remove each block that is on this row
                elif self.blocks[i].row < row:
                    self.blocks[i].move_down()          # move down each block that is above this row
   
#---------------------------------------#
class Shape(Cluster):                     
    """ A tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation             
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        #sets each object's column, row, and color according to the parameters taken
        Cluster.__init__(self, col, row, 4)
        self.clr = clr
        self._rot = 1
        self._colOffsets = [-1, 0, 0, 1] 
        self._rowOffsets = [-1,-1, 0, 0] 
        self._rotate() # private
        
    def __str__(self):
        #returns a string of the objects shape #, column, row, and color
        return FIGURES[self.clr]+' ('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def _rotate(self):
        """ offsets are assigned starting from the farthest (most distant) block in reference to the anchor block """
        if self.clr == 1:    #           (default rotation)    
                             #   o             o o                o              
                             # o x               x o            x o          o x
                             # o                                o              o o
            _colOffsets = [[-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0]] #       
        elif self.clr == 2:  #
                             # o                 o o           o              
                             # o x             o x             x o             x o
                             #   o                               o           o o
            _colOffsets = [[-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0], [-1, 0, 0, 1]] #
            _rowOffsets = [[-1, 0, 0, 1], [-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0]] #
        elif self.clr == 3:  # 
                             #   o             o                o o              
                             #   x             o x o            x           o x o
                             # o o                              o               o
            _colOffsets = [[-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0], [ 1, 1, 0,-1]] #
            _rowOffsets = [[ 1, 1, 0,-1], [-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0]] #            
        elif self.clr == 4:  #  
                             # o o                o             o              
                             #   x            o x o             x           o x o
                             #   o                              o o         o
            _colOffsets = [[-1, 0, 0, 0], [1, -1, 0, 1], [0, 0, 0, 1], [-1, 0, 1,-1]]#
            _rowOffsets = [[-1,-1, 0, 1], [-1,0, 0, 0], [-1, 0, 1, 1], [0, 0, 0, 1]]#
        elif self.clr == 5:  #   o                              o
                             #   o                              x              
                             #   x            o x o o           o          o o x o
                             #   o                              o              
            _colOffsets = [[ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0], [-2,-1, 0, 1]] #
            _rowOffsets = [[-2,-1, 0, 1], [ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0]] #           
        elif self.clr == 6:  #
                             #   o              o                o              
                             # o x            o x o              x o         o x o
                             #   o                               o             o 
            _colOffsets = [[ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0]] #
        elif self.clr == 7:  # 
                             # o o            o o               o o          o o
                             # o x            o x               o x          o x
                             # 
            _colOffsets = [[-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0]] #@@
            _rowOffsets = [[ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1]] #@@
        self._colOffsets = _colOffsets[self._rot] 
        self._rowOffsets = _rowOffsets[self._rot] 
        self._update() # private

    def move_left(self):
        #moves the object left
        self.col = self.col - 1                   
        self._update() # private
        
    def move_right(self):
        #moves the object right
        self.col = self.col + 1                   
        self._update() # private
        
    def move_down(self):
        #moves the object down
        self.row = self.row + 1                   
        self._update() # private
        
    def move_up(self):
        #moves the object up
        self.row = self.row - 1                   
        self._update() # private

    def rotateClkwise(self):
        #rotates the object clockwise
        self._rot = (self._rot+1)%4
        self._rotate()

    def rotateCntclkwise(self):
        #rotates the object counterclockwise
        if self._rot!=0:
            self._rot = self._rot-1
        else:
            self._rot=3
        self._rotate()

#---------------------------------------#
class Floor(Cluster):
    """ Horizontal line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        #sets an object column #, row #, and number of blocks 
        Cluster.__init__(self, col, row, blocksNo)
        #uses the objects attributes to create a cluster object
        for i in range(blocksNo):
            self._colOffsets[i] = i 
        self._update() # private       
            
#---------------------------------------#
class Wall(Cluster):
    """ Vertical line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        #sets an object column #, row #, and number of blocks 
        Cluster.__init__(self, col, row, blocksNo)
        #uses the objects attributes to create a cluster object
        for i in range(blocksNo):
            self._rowOffsets[i] = i 
        self._update() # private Make sure all the methods marked as private have an underscore before its name
