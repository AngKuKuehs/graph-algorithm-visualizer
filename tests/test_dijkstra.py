from algorithms.dijkstra import run
from components.grid import Grid
from components.spot import Spot
import math

def find_grid_path(start: Spot):
    res = []
    visited = set()
    brk = True
    curr = start
    while brk:
        brk = False
        visited.add(curr)
        res.append((curr.row, curr.col))
        for adj in curr.neighbors:
            if adj.is_path() and adj not in visited:
                brk = True
                curr = adj
                break
            if adj.is_end():
                res.append((adj.row, adj.col))
                return res
    return []

def test_straight_without_barriers():
    grid = Grid(None, 4, 1)

    start = grid.grid[0][0]
    end = grid.grid[3][0]
    start.make_start()
    end.make_end()
    
    exp_path = [(0, 0), (1, 0), (2, 0), (3, 0)]
    grid.update_neighbours()
    run(lambda: None, grid.grid, start, end)
    assert find_grid_path(start) == exp_path


def test_efficiency():
    # O(ELogV)
    grid = Grid(None, 4, 1) #16 nodes; 2 * 2 * 3 * 4 edges

    start = grid.grid[0][0]
    end = grid.grid[3][0]
    start.make_start()
    end.make_end()
    
    grid.update_neighbours()
    _, less_nodes_time, _, _ = run(lambda: None, grid.grid, start, end)

    grid = Grid(None, 13, 1) #169 nodes; 2 * 2 * 12 * 13 edges

    start = grid.grid[0][0]
    end = grid.grid[12][0]
    start.make_start()
    end.make_end()
    grid.update_neighbours()
    _, more_nodes_time, _, _ = run(lambda: None, grid.grid, start, end)
    time_complexity_mult = ((2*2*12*13) * math.log(169))/((2*2*3*4) * math.log(16))
    assert more_nodes_time < less_nodes_time * time_complexity_mult


def test_blocked_start():
    grid = Grid(None, 4, 1)

    start = grid.grid[0][0]
    end = grid.grid[3][0]
    start.make_start()
    end.make_end()
    
    grid.grid[0][1].make_barrier()
    grid.grid[1][0].make_barrier()
    
    exp_path = []
    grid.update_neighbours()
    run(lambda: None, grid.grid, start, end)
    assert find_grid_path(start) == exp_path

def test_blocked_end():
    grid = Grid(None, 4, 1)

    start = grid.grid[0][0]
    end = grid.grid[3][0]
    start.make_start()
    end.make_end()
    
    grid.grid[3][1].make_barrier()
    grid.grid[2][0].make_barrier()
    
    exp_path = []
    grid.update_neighbours()
    run(lambda: None, grid.grid, start, end)
    assert find_grid_path(start) == exp_path

def test_opposite_corners():
    grid = Grid(None, 4, 1)

    start = grid.grid[0][0]
    end = grid.grid[3][3]
    start.make_start()
    end.make_end()
    
    exp_path_1 = [(i, 0) for i in range(4)] + [(3, i) for i in range(1, 4)]
    exp_path_2 = [(0, i) for i in range(4)] + [(i, 3) for i in range(1, 4)]
    grid.update_neighbours()
    run(lambda: None, grid.grid, start, end)
    assert find_grid_path(start) == exp_path_1 or exp_path_2

def test_diagonal_barriers():
    grid = Grid(None, 4, 1)
    
    start = grid.grid[0][0]
    end = grid.grid[3][3]
    start.make_start()
    end.make_end()

    # Create diagonal barriers
    for i in range(1, 3):
        grid.grid[i][i].make_barrier()

    exp_path_1 = [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)]
    exp_path_2 = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3)]
    grid.update_neighbours()
    run(lambda: None, grid.grid, start, end)
    assert find_grid_path(start) == exp_path_1 or exp_path_2

def test_full_barrier_except_one_path():
    grid = Grid(None, 4, 1)
    
    start = grid.grid[0][0]
    end = grid.grid[3][3]
    start.make_start()
    end.make_end()

    # Create a full barrier besides one path
    for i in range(1, 4):
        for j in range(3):
            grid.grid[i][j].make_barrier()

    exp_path = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3)]
    grid.update_neighbours()
    run(lambda: None, grid.grid, start, end)
    assert find_grid_path(start) == exp_path
