import time


def run(draw, grid, start, end):
    start_time = time.time()
    algorithm_name = "Bellman-Ford"
    traverse_time = None
    traversed_nodes = None
    path_length = None
    
    distances = {}
    vertices = 0
    for row in grid:
        for spot in row:
            if not spot.is_barrier():
                vertices += 1
                distances[spot] = float('inf')

    pred = {}
    distances[start] = 0
    end_early = False
    for _ in range(len(distances) - 1):
        if end_early:
            break
        end_early = True
        for spot in distances.keys():
            if distances[spot] == float('inf'):
                continue
            edges = spot.neighbors
            for edge in edges:
                if distances[edge] > distances[spot] + 1:
                    end_early = False
                    distances[edge] = distances[spot] + 1
                    pred[edge] = spot
                    if edge == end:
                        continue
                    edge.make_open()

        draw()

    if distances[end] == float('inf'):
        traverse_time = time.time() - start_time
        traversed_nodes = len(grid) ** 2
        return algorithm_name, traverse_time, traversed_nodes, path_length
    
    path = pred[end]
    path_length = 1
    while path != start:
        path_length += 1
        path.make_path()
        path = pred[path]
        draw()
    end.make_end()
    start.make_start()
    draw()
    traverse_time = time.time() - start_time
    traversed_nodes = len(grid) ** 2
    return algorithm_name, traverse_time, traversed_nodes, path_length