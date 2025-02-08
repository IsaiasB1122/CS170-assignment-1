import heapq
def algorithm_prompt():
    print(f"OK, now please choose which algorithm you would like to use:\n")
    print(f"[1] Uniform Cost Search")
    print(f"[2] A* with Misplaced Tile Heuristic")
    print(f"[3] A* with Manhattan Distance Heuristic")
    print()
class TreeNode:
    def __init__(self, puzzle_state, parent = None, move = None, cost = 0, depth = 0):
        #once state is created, convert to tuple so it cannot be changed
        self.puzzle_state = tuple(tuple(row) for row in puzzle_state)
        self.parent = parent
        self.move = move
        self.cost = cost
        self.depth = depth
    
    def __lt__(self, other):
        return self.cost < other.cost
    
    def swap(self, x1,y1,x2,y2):
        #convert tuple rows into lists to allow for modification
        new_state = [list(row) for row in self.puzzle_state]
        #swap is now valid
        new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
        
        #now, convert back to tuple and return
        return tuple(tuple(row) for row in new_state)

    def get_children(self):
        children = []
        empty_pos = self.find_empty_block()
        x, y = empty_pos #empty block position (x, y)

        moves = [(1,0,"Up"),(-1,0,"Down"),(0,-1,"Left"), (0,1, "Right")]
        #generates a new legal state from the empty block
        for dx, dy, move in moves: 
            new_x, new_y = x + dx, y + dy

            #if the new position is in logical range of an 8-puzzle, expand nodes and access children
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_state = self.swap(x, y, new_x, new_y)
                #cost for eight puzzle will always be one, so keep adding one cost when new children are made
                children.append(TreeNode(new_state, self, move, self.cost + 1,self.depth + 1))
        return children
    def find_empty_block(self): #returns the coordinates (x,y) of the zero node.
        #iterate through the whole puzzle
        for i in range(3):
            for j in range(3):  
                if self.puzzle_state[i][j] == 0:
                    return i, j
        return None
    
#cost for the eight-puzzle will always be one, so this serves as a breadth first search
def uniform_cost_search(start, goal_state): 
    nodes_expanded = 0 
    max_queue_length = 0
    nodes = []
    #visted nodes are in an unchangable structure
    visited = set() 
    
    #push the current cost of the root node into the nodes queue
    heapq.heappush(nodes, (0, TreeNode(start)))  
    #add a the node's state into the visited set
    visited.add(TreeNode(start).puzzle_state)  

    state = 1
    while nodes:
        #keep updating max_queue_length under each iteration of the loop
        max_queue_length = max(max_queue_length, len(nodes))
        #take the value of the current cost, along with the node
        current_cost, node = heapq.heappop(nodes)
        print(f"visited state: {state}")
        state += 1
        #prints all of the states pushed onto the queue
        for row in node.puzzle_state:
            print(row)
        #When UCS eventually finds goal, return the goal terminal node
        if node.puzzle_state == goal_state: 
            print("Goal Reached!")
            print(f"Nodes Expanded: {nodes_expanded}")
            print(f"Max Queue Length: {max_queue_length}")
            print(f"Depth: {node.depth}")
            return node
        #If the terminal node is not the goal, then expand
        nodes_expanded += 1 

        for child in node.get_children():
            if child.puzzle_state not in visited:
                #push the child into the queue, along with its cost
                heapq.heappush(nodes, (child.cost, child))
                visited.add(child.puzzle_state)  
    print("Failure. UCS was not able to find a solution")
    return None
def a_star_algorithm(start, heuristic,goal_state):
    nodes_expanded = 0
    max_queue_length = 0
    nodes = []
    visited = set()
    
    heapq.heappush(nodes,(0,TreeNode(start)))
    visited.add(TreeNode(start).puzzle_state)

    while nodes:
        max_queue_length = max(max_queue_length, len(nodes))
        current_cost, node = heapq.heappop(nodes)
        print(f"Best state with cheapest estimated cost: {current_cost}")
        for row in node.puzzle_state:
            print(row)
 
        if node.puzzle_state == goal_state:
            print("Goal Reached!")
            print(f"Nodes Expanded: {nodes_expanded}")
            print(f"Max Queue Length: {max_queue_length}")
            print(f"Depth: {node.depth}")
            return node
        
        nodes_expanded += 1
        for child in node.get_children():
            if child.puzzle_state not in visited:
                h_cost = heuristic(child.puzzle_state, goal_state)
                f_cost = child.cost + h_cost
                heapq.heappush(nodes, (f_cost , child))
                visited.add(child.puzzle_state)
    print("Failure. A* was not able to find a solution with given heuristic")

def manhattan_distance_heuristic(current_board,goal_state):
    distance = 0
    goal_positions={1:(0,0),2:(0,1),3:(0,2),
                    4:(1,0),5:(1,1),6:(1,2),
                    7:(2,0),8:(2,1),0:(2,2)}
    
    for i in range(3):
        for j in range(3):
            number = current_board[i][j]
            if number != 0:
                goal_i, goal_j = goal_positions[number]
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance


def misplaced_tile_hueristic(current_board,goal_state):
    misplaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if current_board[i][j] != 0 and current_board[i][j] != goal_state[i][j]:
                misplaced_tiles += 1
    return misplaced_tiles

trivial_test = [[1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]]
very_easy = [[1, 2, 3],
             [4, 5, 6],
             [0, 7, 8]]
easy = [[1, 2, 0],
        [4, 5, 3],
        [7, 8, 6]]
medium = [[0, 1, 2],
          [4, 5, 3],
          [7, 8, 6]]
difficult = [[8, 7, 1],
             [6, 0, 2],
             [5, 4, 3]]
#store as a tuple of a tuple to follow TreeNode puzzle_state
goal_state = tuple(tuple(row) for row in trivial_test)

print(f"Hello! Please choose what you would like to: do:\n")
print(f"[1] Select a default puzzle")
print(f"[2] Create your own puzzle")

board = []
default_or_custom = int(input())
if default_or_custom == 1:
    print("Please choose which puzzle you would like to use\n")
    print("[1] trivial puzzle")
    print("[2] very easy puzzle")
    print("[3] easy puzzle")
    print("[4] medium difficulty puzzle")
    print("[5] pretty difficult puzzle")
    difficulty_choice = int(input())
    if difficulty_choice == 1:
        board = trivial_test
    if difficulty_choice == 2:
        board = very_easy
    if difficulty_choice == 3:
        board = easy
    if difficulty_choice == 4:
        board = medium
    if difficulty_choice == 5:
        board = difficult
if default_or_custom == 2:
    print("\nEnter your puzzle row by row. Use spaces to separate the values and press enter when finished with the row:")
    for i in range(3):
        row = input(f"Row {i + 1}: ").split()
        board.append([int(value) for value in row])

algorithm_prompt()
algo_choice = int(input())
if algo_choice == 1:
    print("Now working on the puzzle with uniform cost search...")
    uniform_cost_search(board, goal_state)
if algo_choice == 2:
    print("Now working the puzzle with A* and a misplaced tile heuristic...")
    heuristic = misplaced_tile_hueristic
    a_star_algorithm(board, heuristic, goal_state)
if algo_choice == 3:
    print ("Now working the puzzle with A* and manhattan distance heuristic...")
    heuristic = manhattan_distance_heuristic
    a_star_algorithm(board, heuristic, goal_state)