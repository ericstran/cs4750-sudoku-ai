import copy, time

cur_map = []
stack = []
# n(umber) of rows/columns
n = 9
assignments = 0


class Cell:
    def __init__(self, x, y, number):
        # coordinate
        self.x = x
        self.y = y

        # check if filled
        self.isComplete = False
        if number != '*':
            self.isComplete = True
            number = int(number)
        # set cell value
        self.number = number
        # Sudoku numbers for minimum remaining possible values
        self.num_mrv = [x for x in range(1, n+1)]

    def __repr__(self): return "{}".format(self.number)


# initialize cur_map cells
def get_input(inputMap):
    print("here")
    # make rows
    for _ in range(n): cur_map.append([])
    # make cols/initialize cells
    for row in range(n):
        for col in range(n):
            cur_map[row].append(Cell(row, col, inputMap[row][col]))


# set other cell domains for a given cell
# returns True if no conflict, False if conflict
def set_cell_num_domain(cell):
    # get coordinate
    x = cell.x # row
    y = cell.y # col
    # proceed if cell is filled
    if cell.number != '*':
        # check rows and cols
        for i in range(n):
            if i == x:  # or  cur_map[i][y].isComplete == True :
                continue 
            try: 
                # for all in same col, different row, remove cell's number (forward checking)
                cur_map[i][y].num_mrv.remove(cell.number)
                # if no possible values remaining and not filled return False
                if len(cur_map[i][y].num_mrv) == 0 and cur_map[i][y].isComplete != True: return False
            except: pass
        for j in range(n):
            if j == y:  # or cur_map[x][j].isComplete == True:
                continue 
            try:
                # for all in same row, different col, remove cell's number (forward checking)
                cur_map[x][j].num_mrv.remove(cell.number)
                # if no possible values remaining and not filled return False
                if len(cur_map[x][j].num_mrv) == 0 and cur_map[x][j].isComplete != True: return False
            except: pass
        # check 3x3
        # get which square in map
        squareX = -1
        squareY = -1
        if((x == 0) or (x == 1) or (x == 2)): squareX = 0
        elif((x == 3) or (x == 4) or (x == 5)): squareX = 1
        elif((x == 6) or (x == 7) or (x == 8)): squareX = 2
        if((y == 0) or (y == 1) or (y == 2)): squareY = 0
        elif((y == 3) or (y == 4) or (y == 5)): squareY = 1
        elif((y == 6) or (y == 7) or (y == 8)): squareY = 2
        posInSquareX = x % 3
        posInSquareY = y % 3
        # loop through 3x3 where cell is located
        for currX in range(3):
            for currY in range(3):
                if((currX == posInSquareX) and (currY == posInSquareY)): continue
                try:
                    # for all in same 3x3, remove cell's number (forward checking)
                    cur_map[currX + (squareX * 3)][currY + (squareY * 3)].num_mrv.remove(cell.number)
                    # if no possible values remaining and not filled return False
                    if len(cur_map[currX + (squareX * 3)][currY + (squareY * 3)].num_mrv) == 0 and cur_map[currX + (squareX * 3)][currY + (squareY * 3)].isComplete != True:
                        return False
                except: pass
    return True


# wrapper function for set_cell_num_domain() - all cells
def set_map_domain():
    # for each cell, call set_cell_num_domain() 
    for row in range(n):
        for col in range(n):
            x = set_cell_num_domain(cur_map[row][col])
    return x


# print mrv for each cell
def print_mrv():
    for i in range(n):
        for j in range(n):
            print(cur_map[i][j].num_mrv, end=",,,")
        print()


def print_map(map, x, y):
    for i in range(n):
        for j in range(n):
            if (x == None and y == None) or (i != x or j != y): print(map[i][j], end=", ")
            else: print('(' + str(map[i][j]) + ')', end=", ")
        print()
    print("*********")


# choose cell with mrv
def choose_cell():
    # create fake cell for comparison
    min_mrv_cell = Cell(-1, -1, "*")
    min_mrv_cell.num_mrv = [x for x in range(n+1)]
    # loop through each cell
    for i in range(n):
        for j in range(n):
            # if cell not filled and num_mrv less than current min_mrv_cell num_mrv then set new min_mrv_cell
            if cur_map[i][j].isComplete == False and len(cur_map[i][j].num_mrv) <= len(min_mrv_cell.num_mrv):
                min_mrv_cell = cur_map[i][j]

    return min_mrv_cell

# wrapper function for set_cell_num_domain() - one cell
def forward_checking(cell):
    x = set_cell_num_domain(cell)
    if x == False:
        return "failure"

if __name__ == "__main__":
    start_time = time.time()
    # 2D array representation of Sudoku puzzle (map)
    # "*" represents open space
    map1 = [
        ["*", "*", 1, "*", "*", 2, "*", "*", "*"],
        ["*", "*", 5, "*", "*", 6, "*", 3, "*"],
        [4, 6, "*", "*", "*", 5, "*", "*", "*"],
        ["*", "*", "*", 1, "*", 4, "*", "*", "*"],
        [6, "*", "*", 8, "*", "*", 1, 4, 3],
        ["*", "*", "*", "*", 9, "*", 5, "*", 8],
        [8, "*", "*", "*", 4, 9, "*", 5, "*"],
        [1, "*", "*", 3, 2, "*", "*", "*", "*"],
        ["*", "*", 9, "*", "*", "*", 3, "*", "*"]
    ]

    map2 = [
        ["*", "*", 5, "*", 1, "*", "*", "*", "*"],
        ["*", "*", 2, "*", "*", 4, "*", 3, "*"],
        [1, "*", 9, "*", "*", "*", 2, "*", 6],
        [2, "*", "*", "*", 3, "*", "*", "*", "*"],
        ["*", 4, "*", "*", "*", "*", 7, "*", "*"],
        [5, "*", "*", "*", "*", 7, "*", "*", 1],
        ["*", "*", "*", 6, "*", 3, "*", "*", "*"],
        ["*", 6, "*", 1, "*", "*", "*", "*", "*"],
        ["*", "*", "*", "*", 7, "*", "*", 5, "*"]
    ]

    map3 = [
        [6, 7, "*", "*", "*", "*", "*", "*", "*"],
        ["*", 2, 5, "*", "*", "*", "*", "*", "*"],
        ["*", 9, "*", 5, 6, "*", 2, "*", "*"],
        [3, "*", "*", "*", 8, "*", 9, "*", "*"],
        ["*", "*", "*", "*", "*", "*", 8, "*", 1],
        ["*", "*", "*", 4, 7, "*", "*", "*", "*"],
        ["*", "*", 8, 6, "*", "*", "*", 9, "*"],
        ["*", "*", "*", "*", "*", "*", "*", 1, "*"],
        [1, "*", 6, "*", 5, "*", "*", 7, "*"]
    ]

    # put map1 in cur_map
    get_input(map1)

    # set starting cell domain values
    set_map_domain()

    print("map for first time: \n")
    print_map(cur_map, None, None)

    stack.append(cur_map)
    while len(stack) > 0:
        # get cell with mrv
        chosen_cell = choose_cell()
        # print("chosen is",chosen_cell.x,chosen_cell.y)
        # if cell couldn't be chosen, end
        if (chosen_cell.x == -1 or chosen_cell.y == -1):
            print("result: ")
            print_map(cur_map, None, None)
            print("--- %s seconds ---" % (time.time() - start_time))
            exit()

        # if chosen cell has no possible values, failure
        if len(chosen_cell.num_mrv) == 0:
            t = "failure"

        else:
            # pop chosen cell possible value
            x = chosen_cell.num_mrv.pop(0)
            # copy cur_map
            bp_map = copy.deepcopy(cur_map)
            # push new map onto stack
            stack.append(bp_map)
            # fill chosen cell
            chosen_cell.number = x
            chosen_cell.isComplete = True
            # print first 4 assignments
            if assignments < 4:
                assignments += 1
                print(("assignment " + str(assignments)).center(40, "*")) 
                print_map(cur_map, chosen_cell.x, chosen_cell.y)

            # forward check on chosen cell
            t = forward_checking(chosen_cell)

        if t != "failure": # keep going
            pass

        else:
            print("back Track".center(40, "*")) 
            # revert to previous map
            cur_map = stack.pop()

    print("no solution")

    # implement tiebreaking based on left to right and top to bottom and increasing order of values
