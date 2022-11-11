import copy, time

cur_map = []
stack = []
# n(umber) of rows/columns
n = 9


class Cell:
    def __init__(self, x, y, number):
        # coordinate
        self.x = x
        self.y = y

        # check if "filled"
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
    # make cols/initialize cell values
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
        # get which square in Sudoku puzzle
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


# wrapper function for set_cell_num_domain()
def set_map_domain():
    # for each cell, call set_cell_num_domain() 
    for row in range(n):
        for col in range(n):
            x = set_cell_num_domain(cur_map[row][col])
    return x


def print_mrv():
    for i in range(n):
        for j in range(n):
            print(cur_map[i][j].num_mrv, end=",,,")
        print()


def choose_cell():
    min_mrv_cell = Cell(-1, -1, "*")
    min_mrv_cell.num_mrv = [x for x in range(n+1)]
    for i in range(n):
        for j in range(n):
            if cur_map[i][j].isComplete == False and len(cur_map[i][j].num_mrv) <= len(min_mrv_cell.num_mrv):
                min_mrv_cell = cur_map[i][j]

    return min_mrv_cell


def forward_checking(cell):
    x = set_cell_num_domain(cell)
    if x == False:
        return "failuer"

if __name__ == "__main__":

  # 2D array representation of Sudoku puzzle
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

get_input(map1)

set_map_domain()

print("map for first time: \n")
for i in range(n):
    print(cur_map[i])
print("*********")

stack.append(cur_map)
while len(stack) > 0:
    chosen_cell = choose_cell()
    # print("chosen is",chosen_cell.x,chosen_cell.y)
    if (chosen_cell.x == -1 or chosen_cell.y == -1):
        print("result: ")
        for i in range(n):
            print(cur_map[i])
        exit()

    if len(chosen_cell.num_mrv) == 0:
        t = "failuer"

    else:
        x = chosen_cell.num_mrv.pop(0)
        bp_map = copy.deepcopy(cur_map)
        stack.append(bp_map)
        chosen_cell.number = x
        chosen_cell.isComplete = True
        t = forward_checking(chosen_cell)

    if t != "failuer":
        pass

    else:
        print("back Track".center(40, "*"))
        cur_map = stack.pop()

print("no solution")
