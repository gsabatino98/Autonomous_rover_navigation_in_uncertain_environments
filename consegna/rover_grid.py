import numpy as np

# IS A CLASS USED TO PRINT THE ELEMENT IN THE GRID
class colors:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   WHITE = '\033[0m'

# CLASS ISED TO DEFINE A SINGLE GRID SQUARE
class Square:

    __obstacle = False
    __roverPresence = False
    __targetRover = False
    __pmfTarget = [0.0, 0.0, 0.0, 0.0, 0.0]
    __id = None

    def __init__(self):
        pass
    
    # Set the return target of the square
    def set_return_target(self, pmfTarget):
        self.__pmfTarget = pmfTarget

    # Get the pmf's target of the square
    def get_pmf_target(self):
        return self.__pmfTarget

    # Set the square as an obstacle
    def set_to_obstacle(self):
        self.__obstacle = True
    
    # Sets the rover on the square  (used to indicate the presence, or not, of the rover in the grid)
    def in_square(self):
        self.__roverPresence = True

    # Sets the rover out of the square (used to indicate the presence, or not, of the rover in the grid)
    def out_square(self):
        self.__roverPresence = False

    # Set an id to the square (used to show rover's path)
    def set_id(self,id):
        self.__id = id

    # Get the id of the square  (used to show rover's path)
    def get_id(self):
        return self.__id

    # Set the square as the position to reach by the rover
    def set_to_target(self):
        self.__targetRover = True

    # Check if the square is a target (used for the routine's loop)
    def is_target(self):
        return self.__targetRover

    # Check if the square is an obstacle
    def is_obstacle(self):
        return self.__obstacle

    # Used to print the State (target, roverPresence or obstacle) of the square
    def print_type(self):

        if(self.__roverPresence):
            return colors.DARKCYAN+"X"+colors.WHITE
        if(self.__targetRover):
            return colors.GREEN+"T"+colors.WHITE
        if(self.__obstacle):
            return colors.RED+"O"+colors.WHITE
        else:
            return "-"

class Grid:

    __numRow = 0
    __numCol = 0
    __gridRover = [[]]
    __rover_positon_r = 0
    __rover_positon_c = 0
    __last_action = 0

    def __init__(self, numRow, numCol, posRoverR, posRoverC):
        self.__numRow = numRow
        self.__numCol = numCol
        self.__rover_positon_r = posRoverR
        self.__rover_positon_c = posRoverC
        self.__gridRover = [[Square() for i in range(numCol)]for j in range(numRow)] # allocates a Square object in all cells of the matrix
        self.__set_id_grid()
        self.__gridRover[posRoverR][posRoverC].in_square()
        self.__gridRover[0][numCol-1].set_to_target()
        self.__set_return_target()

    # Used to set id of the square
    def __set_id_grid(self):

        num_id = 0

        for row in reversed(range(self.__numRow)):
            for col in range(self.__numCol):
                self.__gridRover[row][col].set_id(num_id)
                num_id += 1

    # Set the pmf target in all the squares in the grid
    def __set_return_target(self):
        max_index = 1
        index = 0
        diag = []

        # sets the diagonal in the grid
        for row in range(1,self.__numRow):
            for col in reversed(range(self.__numCol)):
                    if index == max_index:
                        diag.append([row,col])
                        self.__gridRover[row][col].set_return_target([0.01,0.01,0.485,0.485,0.01])
                        max_index +=1
                        index = 0
                        break
                    index += 1        

        # sets the inner areas of the grid
        for crd in diag:
            for ind in range(1,self.__numCol-1):
                row = crd[0]
                col = crd[1]

                if ind > col:   # right part of the grid
                    self.__gridRover[row][ind].set_return_target([0.01,0.01,0.647,0.323,0.01])
                if ind < col:   # left part of the grid
                    self.__gridRover[row][ind].set_return_target([0.01,0.01,0.323,0.647,0.01])

        # sets the first column of the grid
        for row in range(self.__numRow-1):
            self.__gridRover[row][0].set_return_target([0.01,0.01,0.01,0.96,0.01])

        # first row of the grid
        for col in range(self.__numCol):
            if col == self.__numCol-1: # sets the pmf of the taget square to stay in place
                self.__gridRover[0][col].set_return_target([0.96,0.01,0.01,0.01,0.01])
            else:
                self.__gridRover[0][col].set_return_target([0.01,0.01,0.01,0.96,0.01])

        # last column of the grid
        for row in range(1,self.__numRow):
            self.__gridRover[row][self.__numCol-1].set_return_target([0.01,0.01,0.96,0.01,0.01])

        # last row of the grid
        for col in range(self.__numCol):
            if col == 0:
                self.__gridRover[self.__numRow-1][col].set_return_target([0.01,0.01,0.01,0.96,0.01])
            else:
                self.__gridRover[self.__numRow-1][col].set_return_target([0.01,0.01,0.96,0.01,0.01])

    # Used to insert in the grid an obstacle in a desired position
    def generate_obstacle(self, nRow, nCol):

        for row in range(self.__numRow):
            if(nRow == row):
                for col in range(self.__numCol):
                    if(nCol == col):
                        self.__gridRover[row][col].set_to_obstacle()

    # Used to move the rover on the grid
    def move_rover(self, action):
        # action indicates the movement that the rover must make [0=stay, 1=left, 2=up, 3=right, 4=down]
        
        # exit from the old square
        self.__gridRover[self.__rover_positon_r][self.__rover_positon_c].out_square()

        if(action == 1):# move rover left
            self.__last_action = 3  # last action is right
            self.__rover_positon_c -= 1

        if(action == 2):# move rover up
            self.__last_action = 4  # last action is down
            self.__rover_positon_r -= 1

        if(action == 3):# move rover right
            self.__last_action = 1  # last action is left
            self.__rover_positon_c += 1

        if(action == 4):# move rover down
            self.__last_action = 2 # last action is up
            self.__rover_positon_r += 1

        # enter in the new square
        self.__gridRover[self.__rover_positon_r][self.__rover_positon_c].in_square()        

    # Returns the id associated to the current rover position
    def get_current_square_id(self):
        return self.__gridRover[self.__rover_positon_r][self.__rover_positon_c].get_id()

    # Returns the Square object associated with the rover's current position
    def get_square(self):
        return self.__gridRover[self.__rover_positon_r][self.__rover_positon_c]

    # Return the coordinates of the rover in the grid
    def get_current_position(self):
        return [self.__rover_positon_r, self.__rover_positon_c]
   
    # Returns the last action made by the rover to reach the current square
    def get_last_action(self):
        return self.__last_action

# ----------------------- Functions used to solve the control problem (greedy and receding hoirzon) -----------------------

    # Returns the behavior of the sources for a desired square
    def return_sources(self, posRoverR, posRoverC):
        
        source_left = [0.01,0.96,0.01,0.01,0.01]
        source_top = [0.01,0.01,0.96,0.01,0.01]
        source_right = [0.01,0.01,0.01,0.96,0.01]
        source_bot = [0.01,0.01,0.01,0.01,0.96]
        source_stay = [0.96,0.01,0.01,0.01,0.01]

        if self.findWall(posRoverR,posRoverC)[0]: #If we are near a wall (or more), the corresponding movement is replaced by "stay in place"
            source_left = [0.96,0.01,0.01,0.01,0.01]
        if self.findWall(posRoverR,posRoverC)[1]:
            source_top = [0.96,0.01,0.01,0.01,0.01]
        if self.findWall(posRoverR,posRoverC)[2]:
            source_right = [0.96,0.01,0.01,0.01,0.01]
        if self.findWall(posRoverR,posRoverC)[3]:
            source_bot = [0.96,0.01,0.01,0.01,0.01]
            
        return(np.array([source_stay, source_left, source_top, source_right, source_bot]))

    # Returns the pmf target of a desired square
    def return_target(self, roverPositionR, roverPositionC):
        return self.__gridRover[roverPositionR][roverPositionC].get_pmf_target()

    # Returns the rover's reward in the desired position
    def return_reward(self, roverPositionR, roverPositionC):

        reward = [0,0,0,0,0]

        pos_r = roverPositionR
        pos_c = roverPositionC
        
        # Set a negative reward to the last action
        if reward[self.__last_action] == 0:
            reward[self.__last_action] = -10

        #find obstacle in the left side of the square
        if((pos_c - 1) != -1 and self.__gridRover[pos_r][pos_c - 1].is_obstacle()):
            reward[1] = -100

        #find obstacle in the top side of the square
        if((pos_r - 1) != -1 and self.__gridRover[pos_r - 1][pos_c].is_obstacle()):
            reward[2] = -100

        #find obstacle in the right side of the square
        if(self.__numCol != (pos_c + 1) and self.__gridRover[pos_r][pos_c + 1].is_obstacle()):
            reward[3] = -100

        #find obstacle in the down side of the square
        if(self.__numRow != (pos_r + 1) and self.__gridRover[pos_r + 1][pos_c].is_obstacle()):
            reward[4] = -100  

        return reward

    # Returns the rover's position according to a chosen action
    def actualState(self, action):

        pos_r = self.__rover_positon_r
        pos_c = self.__rover_positon_c

        if(action == 1):#moves rover left
            pos_c -= 1

        if(action == 2):#moves rover up
            pos_r -= 1

        if(action == 3):#moves rover right
            pos_c += 1

        if(action == 4):#moves rover down
            pos_r += 1

        return pos_r, pos_c

    # Returns an array to show the presence of the wall according to an action, on a desired square
    def findWall(self, roverPositionR, roverPositionC):
        
        wall = [0,0,0,0]

        pos_r = roverPositionR
        pos_c = roverPositionC
        
        # find wall on the left side of the square
        pos_c -= 1
        if(pos_c == -1):
            wall[0] = 1
        pos_c += 1

        # find wall on the top side of the square
        pos_r -= 1
        if(pos_r == -1):
            wall[1] = 1
        pos_r += 1

        # find wall on the right side of the square
        pos_c += 1
        if(self.__numCol == pos_c):
            wall[2] = 1
        pos_c -= 1

        # find wall on the down side of the square
        pos_r += 1
        if(self.__numRow == pos_r):
            wall[3] = 1
        pos_r -= 1        

        return wall

    # Returns the available states in the current position of the rover
    def available_States(self):

        available_action = []
        action = 0

        available_action.append(action)  # stay in place is an action that can always be done
        
        posRov = self.get_current_position()

        pos = self.findWall(posRov[0], posRov[1])

        for wall in pos:
            action += 1
            if(wall != 1):
                available_action.append(action)

        return available_action

# ---------------------------------------------- Print and routine functions ----------------------------------------------

    # Returns true or false if the rover is on the target (used for the routine's loop)
    def is_on_target(self):
        square = self.__gridRover[self.__rover_positon_r][self.__rover_positon_c]

        if square.is_target():
            return True
        else:
            return False        

    # Print the grid
    def print_grid(self):

        indexCol = 0

        print("+",end="")
        
        for i in range(self.__numCol):
            indexCol += 1
            if(indexCol == self.__numCol):
                print("-----",end="")
                indexCol = 0
            else:
                print("------",end="")

        print("+")

        for row in self.__gridRover:
            for col in row:
                indexCol += 1
                print("|  "+col.print_type(),end="  ")
                if(indexCol == self.__numCol):
                    print("|",end="")
                    indexCol = 0
            print("")
            print("+",end="")

            for i in range(self.__numCol): 
                indexCol += 1
                if(indexCol == self.__numCol):
                    print("-----",end="")
                    indexCol = 0
                else:
                    print("------",end="")

            print("+")
