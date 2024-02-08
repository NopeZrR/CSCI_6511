import heapq

class PuzzleNode:
    def __init__(self, state, g_cost, h_cost):
        self.state = state # Current state
        self.g_cost = g_cost # No. of moves between initial state and current state
        self.h_cost = h_cost # Heuristically estimated number of steps moved

    def __lt__(self, other):
        return (self.g_cost + self.h_cost) < (other.g_cost + other.h_cost)

def get_blank_position(state):
    """ Find the blank space"""
    for i, row in enumerate(state):
        for j, value in enumerate(row):
            if value == 0:
                return (i, j)

def get_manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def get_heuristic_cost(current_state, goal_state):
    """ calculate heuristically estimated number of steps moved (Manhattan distance)"""
    total_cost = 0
    n = len(current_state)
    for i in range(n):
        for j in range(n):
            if current_state[i][j] != 0:
                x, y = divmod(current_state[i][j] - 1, n)
                total_cost += get_manhattan_distance(i, j, x, y)
    return total_cost

def get_neighbors(state):
    """ Get all neighboring states of the current state"""
    neighbors = []
    blank_x, blank_y = get_blank_position(state)
    n = len(state)

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = blank_x + dx, blank_y + dy
        if 0 <= new_x < n and 0 <= new_y < n:
            new_state = [row[:] for row in state]
            new_state[blank_x][blank_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[blank_x][blank_y]
            neighbors.append(new_state)

    return neighbors

def is_valid_size(n):
    """ Determine whether the condition of n is satisfied"""
    return 3 <= n <= 25

def solve_puzzle(initial_state):
    """ Solving n-puzzle problems using the A* algorithm"""
    n = len(initial_state)
    goal_state = [list(range(i * n + 1, (i + 1) * n + 1)) for i in range(n)]
    goal_state[-1][-1] = 0

    initial_node = PuzzleNode(initial_state, 0, get_heuristic_cost(initial_state, goal_state))
    priority_queue = [initial_node]
    visited_states = set()

    while priority_queue:
        current_node = heapq.heappop(priority_queue)

        if current_node.state == goal_state:
            return current_node.state, current_node.g_cost

        visited_states.add(tuple(map(tuple, current_node.state)))

        for neighbor_state in get_neighbors(current_node.state):
            if tuple(map(tuple, neighbor_state)) not in visited_states:
                neighbor_node = PuzzleNode(neighbor_state, current_node.g_cost + 1, get_heuristic_cost(neighbor_state, goal_state))
                heapq.heappush(priority_queue, neighbor_node)

    return None, -1

def read_puzzle_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return [list(map(int, line.strip().split('\t'))) for line in lines]

if __name__ == "__main__":
    file_path = r"F:\CSCI 6511\P1_Option3_N_Puzzle\n-puzzle.txt" # n-puzzle file path
    initial_state = read_puzzle_file(file_path)

    n = len(initial_state)
    
    if not is_valid_size(n):
        print("Error: Invalid puzzle size. Size must be between 3 and 25.")
    else:
        print("Initial Puzzle:")
        for row in initial_state:
            print(row)

        final_state, move_count = solve_puzzle(initial_state)

        if final_state is not None:
            print("\nFinal Puzzle:")
            for row in final_state:
                print(row)
            print(f"\nMinimum moves required: {move_count}")
        else:
            print("The puzzle is unsolvable.")

