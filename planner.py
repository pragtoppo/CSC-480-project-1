import sys
import heapq

ACTIONS = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1),
}

def parse_file(filename):
    with open(filename, encoding='utf-8') as f:
        cols = int(f.readline().lstrip('\ufeff')) 
        rows = int(f.readline())
        grid = [list(f.readline().strip()) for _ in range(rows)]

    dirty = set()
    start = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '*':
                dirty.add((r, c))
            elif grid[r][c] == '@':
                start = (r, c)
    return grid, start, dirty, rows, cols

def get_neighbors(state, grid, rows, cols):
    pos, dirty = state
    r, c = pos
    neighbors = []

    for action, (dr, dc) in ACTIONS.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
            neighbors.append((( (nr, nc), dirty ), action))

    if pos in dirty:
        new_dirty = set(dirty)
        new_dirty.remove(pos)
        neighbors.append((( pos, frozenset(new_dirty) ), 'V'))

    return neighbors

def uniform_cost_search(grid, start, dirty, rows, cols):
    start_state = (start, frozenset(dirty))
    frontier = []
    heapq.heappush(frontier, (0, start_state, []))
    visited = set()
    nodes_generated = 1
    nodes_expanded = 0

    while frontier:
        cost, state, path = heapq.heappop(frontier)

        if state in visited:
            continue
        visited.add(state)
        nodes_expanded += 1

        if not state[1]:
            for action in path:
                print(action)
            print(f"{nodes_generated} nodes generated")
            print(f"{nodes_expanded} nodes expanded")
            return

        for neighbor, action in get_neighbors(state, grid, rows, cols):
            if neighbor not in visited:
                heapq.heappush(frontier, (len(path)+1, neighbor, path + [action]))
                nodes_generated += 1

def depth_first_search(grid, start, dirty, rows, cols):
    start_state = (start, frozenset(dirty))
    stack = [(start_state, [])]
    visited = set()
    nodes_generated = 1
    nodes_expanded = 0

    while stack:
        state, path = stack.pop()

        if state in visited:
            continue
        visited.add(state)
        nodes_expanded += 1

        if not state[1]:
            for action in path:
                print(action)
            print(f"{nodes_generated} nodes generated")
            print(f"{nodes_expanded} nodes expanded")
            return

        for successor, action in reversed(get_neighbors(state, grid, rows, cols)):
            if successor not in visited:
                stack.append((successor, path + [action]))
                nodes_generated += 1

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py [uniform-cost|depth-first] [world-file]")
        return

    algo = sys.argv[1]
    filename = sys.argv[2]

    grid, start, dirty, rows, cols = parse_file(filename)

    if algo == "uniform-cost":
        uniform_cost_search(grid, start, dirty, rows, cols)
    elif algo == "depth-first":
        depth_first_search(grid, start, dirty, rows, cols)
    else:
        print("Unknown algorithm:", algo)

if __name__ == "__main__":
    main()
