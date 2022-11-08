import copy

cur_map = []
stack = []
n = 9
 

class Cell:
    def __init__(self, x, y, number):
        self.x = x
        self.y = y

        self.isComplete = False
        if number != '*':
            self.isComplete = True
            number = int(number)
        self.number = number
        self.num_mrv = [x for x in range(1, n+1)]

    def __repr__(self):
        return "{}".format(self.number)


def get_input(inputMap):
    print("here")
    for i in range(n):
        cur_map.append([])
    for row in range(n):
        for col in range(n):
            cur_map[row].append(Cell(row, col, inputMap[row][col]))


def set_cell_num_domain(cell):
    x = cell.x
    y = cell.y
    if cell.number != '*':
        for i in range(n):
            if i == x:  # or  cur_map[i][y].isComplete == True :
                continue
            try:
                cur_map[i][y].num_mrv.remove(cell.number)
                if len(cur_map[i][y].num_mrv) == 0 and cur_map[i][y].isComplete != True:
                    return false
            except:
                pass
        for j in range(n):
            if j == y:  # or cur_map[x][j].isComplete == True:
                continue
            try:
                cur_map[x][j].num_mrv.remove(cell.number)
                if len(cur_map[x][j].num_mrv) == 0 and cur_map[x][j].isComplete != True:
                    return False
            except:
                pass
    return True


def set_map_domain():
    for i in range(n):
        for j in range(n):
            x = set_cell_num_domain(cur_map[i][j])
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
