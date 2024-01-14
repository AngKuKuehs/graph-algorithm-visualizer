# Graph Algorithm Visualizer
Contributors: Bryan Ang Huai-En, Jingyi Hou

## Description

A visualization tool for graph traversal algorithms, focusing on Dijkstra, A*, and Bellman-Ford algorithms, utilizing Python and Pygame.

## Project Structure

- **algorithms**
  - `dijkstra.py`: Implementation of Dijkstra's algorithm for pathfinding.
  - `a_star.py`: Implementation of A* algorithm for pathfinding.
  - `bellman_ford.py`: Implemntation of Bellman-Ford algorithm for pathfinding.
- **components**
  - `spot.py`: Definition and management of a spot/node in the grid.
  - `grid.py`: Handling grid functionality, drawings, and updates.
- **tests**
  - `test_dijkstra.py`: Unit tests to validate the correctness and efficiency of the Dijkstra's algorithm implementation.
  - `test_a_star.py`: Unit tests to validate the correctness and efficiency of the A* algorithm implementation.
  - `test_bellman_ford.py`: Unit tests to validate the correctness and efficiency of the Bellman-Ford algorithm implementation.
  - `test_compare_dijkstra.py`: Test to validate that our implementation of Dijkstra is more efficient than Python's inbuilt implementation of Dijkstra.
- **assets**
  - `demo.mov`: A demonstration video providing an example of expected outcomes.
- **main.py**: Main script to execute the application.
- **pyproject.toml**: Configuration file for Poetry, outlining project dependencies.

# Encountered Challenges
## Project Structure
One challenge we faced was familliarising ourselves with how the file structure of the project works. This included learning about terms like package, sub-package, module, and sub-module.

One particular issue we faced was running sub-modules independently. For example, trying to run dijkstra.py to check for issues. dijkstra.py itself imports other sub-modules like grid.py so simply executing it with the play button on the top right of the screen in vscode returned an error as the sub-modules could not be located. Instead we learned to use `python -m algorithms.dijkstra`. The `-m` flag executes the module as a script in the root directory.

## Managing Different Environments
Another issue we encountered was the managing of the environment for the project. For example, it was not possible to simply execute `pytest` in the CLI as the environment of pytest on our computer did not contain certain libraries. This was true even though we were in a virtual environment which had another version of pytest. The CLI kept using the global pytest instead of the one in the virtual environment. The solution to this was to make use of poetry and execute `poetry run pytest` in the CLI instead. From this we gained an undrstanding of the importance of package/environment managing frameworks.

## Familliarising Ourselves with Pygame
At the start, the project was daunting given that we were completely unfamiliar with pygame. What helped us, apart from the recomended tutorial, was reading through pygame's documentation and posts on StackOverFlow to understand the functions and classes of pygame.

# Set-up
Assumming poetry has been setup on your computer with the [official installer](https://python-poetry.org/docs/#installing-with-the-official-installer):
1. Create/activate the virtual environement, `poetry shell`
2. Install dependencies with poetry, `poetry install`

# Instructions
Start the application by typing: 

```
poetry run python main.py
```
from the CLI in the root directory. Ensure that your virtual environment is activated.

1. Left click on a square to place the start node. The subsequent clicks will place the stop node and the barrier nodes.
2. Right click on a square to reset it.
3. Press 'S' to cycle through the different algorithms. The current algorithm's name will appear briefly on the top left.
4. Press spacebar to run the current algorithm.
5. Press 'C' to clear everything except for the barriers.
6. Press 'R' to reset the whole board.
7. Press 'I' to view statistics of last algorithm. Stats will display on the top left until another key is pressed.

# Algorithms
## Dijkstra's Algorithm
Given a directed graph with no negative weights and a starting node, Dijkstra's algorithm finds the shortest path to all other nodes. It utilizes a dictionary to keep track of distances from the start and a heap to keep track of the next node to visit.

The intuition behind the algorithm is to explore the graph based on the nearest node updating the distances of the nodes in a dictionary as we go along. We then go to the next node based on the smallest distance of known unvisited nodes.

In this implementation, since the graph is unweighted, we can use a queue instead of a min heap. This is all neighbouring nodes are the same distance from the source node so their order among each other does not matter. And since we are only interested in the path to a single node we can stop the algorithm once the end node has been found and visited. By using a queue instead of a heap, we change the time complexity to O(E + V) since every edge and node is visited at most once.

Time Complexity: O(E + V) but usually O(ELogV).
    where E is the total number of edges and V is the total number of nodes.

Space Complexity: O(V + E)
    where E is the total number of edges and V is the total number of nodes.

## A* (A-Star) Algorithm
A* Algorithm is used for efficiently finding the shortest path in a weighted graph by combining the best features of Dijkstra's Algorithm and Greedy Best-First-Search.

The algorithm's unique characteristic is its use of a heuristic to estimate the cost of the cheapest path from a node to the goal, unlike Dijkstra's which focuses solely on the actual cost from the start node. Our algorithm uses a heuristic function based on the Manhattan distance, which estimates the cost from any given node to the end node. This choice of heuristic is particularly effective for grid layouts where movement is constrained to horizontal and vertical directions.

A key feature of the A* algorithm is its use of a priority queue, managing nodes based on their 'f' score. This score is a sum of the actual distance from the start node ('g' score) and the heuristic distance to the end node ('h' score). The algorithm begins with the start node's 'g' score set to zero and its 'f' score set to the heuristic distance to the end node, while all other nodes have their scores set to infinity. The operational flow involves continuously processing nodes from the priority queue. For each node, its neighbors are examined, updating their scores and adding them to the queue if a shorter path is found. The algorithm continues until the end node is reached, upon which the shortest path is reconstructed and displayed.

Time Complexity: O(E + V log V)
    where E is the total number of edges, and V is the total number of nodes. The actual complexity can vary based on the heuristic's accuracy and the graph's structure.

Space Complexity: O(V)
    where V is the total number of nodes.

## Bellman-Ford Algorithm
Given a graph and starting node, the algorithm finds the shortest path to all other nodes. Similar to Dijkstra's algorithm, the Bellman-Ford algorithm uses a dictionary to account for the current known shortest distances to each node from the starting node.

Intuitively, the algorithm considers all the out edges for each node n-1 times updating the dictionary of shortest distances as it goes.

This algorithm is less efficient that Dijkstra's but it is able to handle negative weights and detect negative cycles. Since all nodes must be considered, we cannot make make the algorithm more efficient by ending when the end node has been reached.

We can however make the implementation more efficient by ending early if the distances table is not updated in an iteration. The end_early variable does this and it reduces the amount of time taken by the algorithm from 17 seconds to 0.38 seconds in one instance.

We also made the algorithm more efficient by skipping over nodes if their distance is equal to float('inf').

In our implementation we left out the negative cycle detection since there are no negative edges. 

Time Complexity: O(EV)
    where E is the total number of edges and V is the total number of nodes.

Space Complexity: O(V)
    where V is the total number of nodes.

# Bonus Question
We have implemented Dijkstra's algorithm more efficiently than the inbuilt Python Dijkstra's algorithm (at least in some situations).

The inbuilt Dijkstra's algorithm has a time complexity of O(ELogV). But we can make this more precise for our use case since we know that each node only has a maximum of 4 neighbours. The inbuilt Dijkstra algorithm iterates through all nodes in the worst case (O(V)) and in each iteration it makes an insertion into a min heap (O(LogV)) and it performs some constant time operations on each of the edges of the node (max 4 edges). Therefore, the time complexity of the inbuilt algorithm for our use case is O(4VLogV) which simplifies to O(VLogV).

The algorithm we implemented has a time complexity of O(V + E) for reasons discussed above.

Our algorithm also has the disadvantage of doing things unrelated to graph traversals (i.e. tasks for our visualization) so when the graph is small it is often beaten by the inbuilt algorithm.

Furthermore, when the graph is dense (i.e. no barriers) then E is roughly V^2 meaning the time complexity for our algorithm becomes O(V^2) which is worse than the time complexity of the inbuilt algorithm.

Therefore, to demonstrate that our algorithm is more efficient than the inbuilt algorithm we require: (1) A relatively large graph. (2) A graph where the relative number of edges is low compared to the nodes. 

With these principles in mind, we developed our unit test.

We initiate a 400*400 grid and set the start and end points to be the first and last node of the first row. We achieve a lower edge to node traversal ratio by setting the barriers in a particular way. Here, we find that 3 ways of setting the barrier, namely horizontal, vertical and diagonal barriers, yield similar results. Then, we run the test 100 times and compare the time taken by our algorithm and that of the inbuilt Dijkstra's algorithm and return the number of times that our algorithm can beat the inbuilt one. We find that under the circumstances that we defined, our algorithm can outperform in the inbuilt function for about 70% of the time. Hence, we have proven that for a relatively large graph in which the relative number of edges is low compared to the nodes (through setting the barriers), our implementation of the Dijkstra's algorithm has a higher chance of outperforming Python's inbuilt graph traversal in terms of time complexity.
