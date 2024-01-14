from queue import PriorityQueue
import time

def h(p1, p2): # Heuristic function
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1) # Manhattan distance

def reconstruct_path(came_from, curr, draw): # Make path
    path_length = 0
    while curr in came_from:
        path_length += 1
        curr = came_from[curr]
        curr.make_path()
        draw()
    return path_length

def run(draw, grid, start, end):
    start_time = time.time()
    algorithm_name = "A Star"
    traverse_time = None
    traversed_nodes = 0
    path_length = None

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # f_score, count, spot

    came_from = {}
    
    g_score = {spot: float("inf") for row in grid for spot in row} # Distance from start to spot
    g_score[start] = 0
    
    f_score = {spot: float("inf") for row in grid for spot in row} # Distance from start to end through spot
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    open_set_hash = {start} # Keeps track of items in the priority queue
    
    while not open_set.empty():
        curr = open_set.get()[2] # Get spot from priority queue
        open_set_hash.remove(curr)
        
        if curr == end: # Make path
            path_length = reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            traverse_time = time.time() - start_time
            return algorithm_name, traverse_time, traversed_nodes, path_length
        
        for neighbor in curr.neighbors:
            temp_g_score = g_score[curr] + 1 # Distance from start to neighbor
            
            if temp_g_score < g_score[neighbor]: # If new path is better than old path
                came_from[neighbor] = curr
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    traversed_nodes += 1
        draw()  

        if curr != start:
            curr.make_closed()

    return algorithm_name, traverse_time, traversed_nodes, path_length
  
