from collections import deque
import time


def run(draw, grid, start, end):
    start_time = time.time()
    algorithm_name = "Dijkstra"
    traverse_time = None
    traversed_nodes = None
    path_length = None

    visited = set()
    queue = deque()
    res = {spot: float('inf') for row in grid for spot in row}
    res[start] = 0
    pred = {}

    queue.append(start)
    while queue:
        curr = queue.popleft()
        visited.add(curr)
        if curr != start and curr != end:
            curr.make_closed()
        if curr == end:
            path = pred[end]
            path_length = 1
            while path != start:
                path_length += 1
                path.make_path()
                draw()
                path = pred[path]
            end.make_end()
            start.make_start()
            draw()
            traverse_time = time.time() - start_time
            traversed_nodes = len(visited) + len(queue)
            return algorithm_name, traverse_time, traversed_nodes, path_length
        
        neighbors = curr.neighbors
        for adj in neighbors:
            if adj in visited:
                continue
            if res[curr] + 1 < res[adj]:
                res[adj] = res[curr] + 1
                pred[adj] = curr
                if adj != end:
                    adj.make_open()
                queue.append(adj)
        draw()
        traverse_time = time.time() - start_time
        traversed_nodes = len(visited) + len(queue)
    return algorithm_name, traverse_time, traversed_nodes, path_length