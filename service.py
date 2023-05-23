import copy

from data import Algorithm, NodeState
from tsp_algo import Vertex, Edge, Branch_n_Bound, DummyGreedy
from visualize import print_banner, refresh

# Heuristic factor Constant
FACTOR = 1


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.state = NodeState.NEW
        self.parent = None
        self.given_cost = 1
        self.heuristic = 0
        self.total_cost = 0
        self.final_cost = 0
        self.neighbours = []

    def cal_total_cost(self, new_total_cost):
        """ The cal_total_cost function calculates the total cost of the current node.
        It does this by adding the new total cost and the given cost of the current node.

        :param new_total_cost: The new total cost of the current node
        :return: The total cost of the current node
        """

        return new_total_cost + self.given_cost

    def set_parent(self, parent):
        """ The set_parent function sets the parent of the current node.
        :param parent: The parent node
        """
        self.parent = parent

    def get_parent(self):
        """ The get_parent function returns the parent of the current node."""

        try:
            return self.parent
        except AttributeError:
            return None

    def cal_heuristic(self, target):
        """ The cal_heuristic function calculates the heuristic of the current node.
        It does this by using the Euclidean distance formula.

        :param target: The target node
        :return: The heuristic of the current node
        """
        self.heuristic = abs(self.x - target.x) + abs(self.y - target.y)
        # self.heuristic = math.sqrt((self.x - target.x) ** 2 + (self.y - target.y) ** 2)
        return self.heuristic

    def get_final_cost(self, target):
        """ The get_final_cost function calculates the final cost of the current node.
        It does this by adding the total cost and the heuristic of the current node.

        :param target: The target node
        :return: The final cost of the current node
        """
        # self.cal_heuristic(target)

        self.final_cost = self.total_cost + FACTOR * self.heuristic
        return self.final_cost

    def is_next_to(self, next_block):
        """
        The is_next_to function checks if the current node is next to the next_node.
        It does this by checking if any of the following conditions are true:

        :param self: Represent the instance of the class
        :param next_block: Check if the current node is next to the next_node
        :return: True if the next node is adjacent to the current node
        """

        if (self.x == next_block.x + 1 and self.y == next_block.y) or (
                self.x == next_block.x - 1 and self.y == next_block.y) or (
                self.x == next_block.x and self.y == next_block.y + 1) or (
                self.x == next_block.x and self.y == next_block.y - 1):
            return True
        else:
            return False

    def __str__(self):
        return str(self.pos)





class Map:
    """A class to represent the map of the warehouse."""

    def __init__(self, map_data):

        self.map_data = map_data
        # All the map data (Not for display) are down here, don't touch this
        self.worker = map_data.worker
        self.org_pos = map_data.worker_org
        self.shelves = map_data.shelves
        self.items = map_data.items
        self.targets = map_data.targets
        self.map_row = map_data.map_row
        self.map_col = map_data.map_col

        # All the map component are down here, use this to implement the algorithm
        self.grid = [[Block(i, j) for j in range(self.map_col)] for i in range(self.map_row)]

        self.target_shelves = []

        for shelf in self.shelves:
            if shelf.pos in list(map(lambda x: x.pos, self.targets)):
                self.target_shelves.append(shelf)

        # Initialize the map component, don't touch this
        self.total_path = []
        self.total_path_description = []
        self.target_blocks = []

        for i in range(self.map_row):
            for j in range(self.map_col):
                if self.grid[i][j].pos == self.worker.pos:
                    self.grid[i][j].state = NodeState.START
                    self.start_block = self.grid[i][j]  # ! start_block

                elif self.grid[i][j].pos in list(map(lambda x: x.pos, self.target_shelves)):
                    self.grid[i][j].state = NodeState.TARGET
                    self.target_blocks.append(self.grid[i][j])  # ! target_block
                #     self.target_block = self.grid[i][j]  # ! target_block

                elif self.grid[i][j].pos in list(map(lambda x: x.pos, self.shelves)):
                    self.grid[i][j].state = NodeState.BLOCK
                else:
                    self.grid[i][j].state = NodeState.NEW

        self.current_block = self.start_block
        self.org_grid = copy.deepcopy(self.grid)
        self.open_list = []
        self.closed_list = []
        self.path = []
        self.iteration = 0
        self.total_length = 0
        self.has_path = False
        self.all_target_nodes = []
        self.adjacency_map = None

    def init_for_tsp(self):
        self.all_target_nodes = self.set_target_entrances()
        # print("initial target nodes successfully")
        # for target in self.all_target_nodes:
        #     print(target)
        self.adjacency_map = self.set_adjacency_map(self.all_target_nodes)

        # print("initial adjacency map successfully")

    def test_basic_tsp(self):
        """
        Test the basic TSP algorithm.
        """
        print(self.target_blocks)
        for target in self.target_blocks:
            self.find_single_target(start=self.current_block, target=target)

        self.set_total_path_state()
        # self.print_map_tsp()

    def find_single_target(self, start=None, target=None, algorithm=Algorithm.A_STAR):
        """
        Find the shortest path to a single target.

        :return: A list of nodes representing the path from the worker to the target.
        """
        self.reset_map()

        # Reset the map
        if start is None:
            curr = self.start_block
        else:
            curr = start

        if target is None:
            target = self.target_blocks.pop()
        else:
            target = target
        # Add the target to the map
        # Find the path

        if algorithm == Algorithm.A_STAR:
            self.a_star(curr, target)
        elif algorithm == Algorithm.DIJKSTRA:
            self.dijkstra(curr, target)
        elif algorithm == Algorithm.BFS:
            self.bfs(curr, target)
        elif algorithm == Algorithm.DFS:
            self.dfs(curr, target)

        # Return the path
        return self.path

    def reset_map(self):
        """
        Reset the map for the next iteration.
        """
        self.path = []
        self.iteration = 0
        self.has_path = False
        self.grid = copy.deepcopy(self.org_grid)

    def set_target_entrances(self):
        """
        A function to set the state of the nodes in the target entrances to TARGET.
        """
        entrances = []
        index = 0
        start = Vertex(self.start_block, 0)
        entrances.append(start)

        for node in self.target_blocks:
            for block in self.get_neighbours(node):
                if block.state != NodeState.TARGET:
                    index += 1
                    entrance = Vertex(block, index, node)
                    entrances.append(entrance)

        return entrances

    def set_adjacency_map(self, all_path_nodes):
        """
        A function to set the adjacency map of the nodes in the total path.
        The function will check all the nodes in the total path and do the following:

        """
        n = len(all_path_nodes)
        adjacency_map = [[None] * n for _ in range(n)]
        for i in range(len(all_path_nodes)):
            for j in range(len(all_path_nodes)):
                if i != j and all_path_nodes[i].is_entrance_of != all_path_nodes[j].is_entrance_of:
                    path = self.find_single_target(all_path_nodes[i].block, all_path_nodes[j].block)
                    path_description = set_path_description(path)
                    edge = Edge(all_path_nodes[i], all_path_nodes[j], path, path_description)
                else:
                    edge = None

                adjacency_map[i][j] = edge
        self.reset_map()
        return adjacency_map

    def tsp(self, algorithm="branch_and_bound"):
        # self.init_for_tsp()
        if algorithm == "branch_and_bound":
            branch_and_bound = Branch_n_Bound(self.adjacency_map, self.all_target_nodes, len(self.target_blocks) + 1)
            branch_and_bound.set_matrix()
            self.total_path, self.total_path_description, self.total_length = branch_and_bound.solve()
        elif algorithm == "dummy_greedy":
            dummy_greedy = DummyGreedy(self.adjacency_map, self.all_target_nodes, len(self.target_blocks) + 1)
            self.total_path, self.total_path_description, self.total_length = dummy_greedy.solver()

        refresh()
        self.set_total_path_state()
        self.print_map()
        print_path_descriptions(self.total_path_description, self.total_length)
        print("If you want to dump the result to a .txt file, press 'd', press other keys and enter to continue.")
        if input() == "d":
            self.dump_instruction_into_file()
        else:
            pass
        return self.total_path, self.total_path_description

    def a_star(self, curr_start, curr_target):
        """
        A function to find a path from the worker to the target using the A* algorithm.
        The function will keep iterating until it finds a path from the worker to the target.
        In each iteration, it will pick the first node from the open list,
        which is the node with the lowest final cost, and call the function astar_iterate().

        :return: A list of nodes representing the path from the worker to the target.
        """

        # Initialize the open and closed list
        curr = curr_start
        self.open_list = [curr]
        self.closed_list = []

        while not self.has_path:  # Keep iterating until a path is found
            self.iteration += 1  # Record the number of iterations
            curr = self.open_list.pop(0)  # Pick the first node from the open list
            self.astar_iterate(curr, curr_target)

        return self.path

    def astar_iterate(self, curr, curr_target):
        """ A function to represent an iteration of A* algorithm.
        The function will check all the neighbours of the current node and do the following:
        1. If the neighbour is next to the target node, then the path is found.
        2. If the neighbour is a new node, then add it to the open list.
        3. If the neighbour is an open node, then check if the new final cost is lower than the current final cost.
        4. If the neighbour is a closed node, then check if the new final cost is lower than the current final cost.
        5. When all the neighbours are checked, add the current node to the closed list.
        6. Sort the open list by the final cost of the nodes.
        (final cost = total cost + heuristic cost, total cost = given cost + parent's total cost)

        :param curr: The current node
        :param curr_target: The current target
        """

        for neighbour in self.get_neighbours(curr):
            state = neighbour.state
            new_cost = curr.total_cost + neighbour.given_cost
            new_final_cost = new_cost + FACTOR * neighbour.cal_heuristic(curr_target)

            # if state == NodeState.GOAL:
            if neighbour.pos == curr_target.pos:
                # If the neighbour is next to the target node, then the path is found

                neighbour.parent = curr
                self.current_block = neighbour
                self.get_path(neighbour)
                return self.path

            elif state == NodeState.NEW:
                # If the neighbour is a new node, then add it to the open list
                neighbour.state = NodeState.OPEN
                neighbour.parent = curr
                neighbour.total_cost = new_cost
                neighbour.final_cost = new_final_cost
                self.open_list.append(neighbour)
                continue

            elif state == NodeState.OPEN:
                # If the neighbour is an open node, then check if the new cost is lower than the current cost
                # If the new cost is lower, then update the neighbour's cost and parent
                if new_final_cost < neighbour.final_cost:
                    neighbour.total_cost = new_cost
                    neighbour.final_cost = new_final_cost
                    neighbour.parent = curr
                    continue

            elif state == NodeState.CLOSE:
                # If the neighbour is a closed node, then check if the new cost is lower than the current cost
                # If the new cost is lower, then remove the neighbour from the closed list and add it to the open list
                if new_final_cost < neighbour.final_cost:
                    neighbour.total_cost = new_cost
                    neighbour.final_cost = new_final_cost
                    neighbour.parent = curr

                    # Also update the neighbour's state
                    neighbour.state = NodeState.OPEN
                    # Also update the neighbour's cost and parent
                    self.closed_list.remove(neighbour)
                    self.open_list.append(neighbour)
                    continue
        # Add the current node to the closed list and set its state to closed
        self.closed_list.append(curr)
        curr.state = NodeState.CLOSE
        # Sort the open list by the final cost
        self.open_list.sort(key=lambda x: x.final_cost)

    def bfs(self, curr_start, curr_target):
        """A function to find the shortest path from the worker to the target using the BFS algorithm.
        The function will keep iterating until it finds a path from the worker to the target.
        In each iteration, it will pick the first node from the open list,
        which is the earliest node to be added to the open list, and call the function bfs_iterate().

        :return: A list of nodes representing the shortest path from the worker to the target.
        """

        # Initialize the open and closed list
        curr = curr_start
        self.open_list = [curr]
        self.closed_list = []

        while not self.has_path:  # Keep iterating until a path is found
            self.iteration += 1  # Record the number of iterations
            curr = self.open_list.pop(0)  # Pick the first node from the open list
            self.bfs_iterate(curr, curr_target)

    def bfs_iterate(self, curr, curr_target):
        """ A function to represent an iteration of BFS algorithm.
        The function will check all the neighbours of the current node and do the following:
        1. If the neighbour is next to the target node, then the path is found.
        2. If the neighbour is a new node, then add it to the open list.
        3. When all the neighbours are checked, add the current node to the closed list.

        :param curr: The current node
        :param curr_target: The target node
        """

        for neighbour in self.get_neighbours(curr):
            state = neighbour.state

            if neighbour.pos == curr_target.pos:
                # If the neighbour is next to the target node, then the path is found

                neighbour.parent = curr
                self.current_block = neighbour
                self.get_path(neighbour)
                return self.path

            elif state == NodeState.NEW:
                neighbour.state = NodeState.OPEN
                neighbour.parent = curr
                self.open_list.append(neighbour)
                continue

            elif state == NodeState.OPEN:
                continue

            elif state == NodeState.CLOSE:
                continue

        self.closed_list.append(curr)
        curr.state = NodeState.CLOSE

    def dfs(self, curr_start, curr_target):
        """
        A function to find a path from the worker to the target using the DFS algorithm.
        The function will keep iterating until it finds a path from the worker to the target.
        In each iteration, it will pick the last node from the open list,
        which is the latest node to be added to the open list, and call the function dfs_iterate().

        :return: A list of nodes representing the path from the worker to the target.
        """

        # Initialize the open and closed list
        curr = curr_start
        self.open_list = [curr]
        self.closed_list = []

        while not self.has_path:  # Keep iterating until a path is found
            self.iteration += 1  # Record the number of iterations
            curr = self.open_list.pop()  # Pick the last node from the open list
            self.dfs_iterate(curr, curr_target)

        return self.path

    def dfs_iterate(self, curr, curr_target):
        """ A function to represent an iteration of DFS algorithm.
        The function will check all the neighbours of the current node and do the following:
        1. If the neighbour is next to the target node, then the path is found.
        2. If the neighbour is a new node, then add it to the open list.
        3. When all the neighbours are checked, add the current node to the closed list.

        :param curr: The current node
        :param curr_target: The target node
        """
        for neighbour in self.get_neighbours(curr):
            state = neighbour.state
            if neighbour.pos == curr_target.pos:
                neighbour.parent = curr
                self.get_path(neighbour)
                return self.path

            elif state == NodeState.NEW:
                neighbour.state = NodeState.OPEN
                neighbour.parent = curr
                self.open_list.append(neighbour)
                continue

            elif state == NodeState.OPEN:
                continue

            elif state == NodeState.CLOSE:
                continue

        self.closed_list.append(curr)
        curr.state = NodeState.CLOSE

    def dijkstra(self, curr_start, curr_target):
        """
        A function to find the shortest path from the worker to the target using the Dijkstra algorithm.
        The function will keep iterating until it finds a path from the worker to the target.
        In each iteration, it will pick the first node from the open list,
        which is the node with the lowest total cost, and call the function dijkstra_iterate().


        :return: A list of nodes representing the shortest path from the worker to the target.
        """

        # Initialize the open and closed list
        curr = curr_start
        self.open_list = [curr]
        self.closed_list = []

        while not self.has_path:  # Keep iterating until a path is found
            curr = self.open_list.pop(0)  # Pick the first node from the open list
            self.iteration += 1  # Record the number of iterations
            self.dijkstra_iterate(curr, curr_target)  # Call the function dijkstra_iterate()

        return self.path

    def dijkstra_iterate(self, curr, curr_target):
        """A function to iterate through the Dijkstra algorithm.
        The function will check all the neighbours of the current node and do the following:
        1. If the neighbour is next to the target node, then the path is found.
        2. If the neighbour is in the open list, then update its total cost if necessary.
        3. If the neighbour is a new node, then add it to the open list.
        4. When all the neighbours are checked, add the current node to the closed list.
        5. Sort the open list by the total cost of the nodes. (total cost = given cost + total cost of the parent node)

        :param curr: The current node
        :param curr_target: The target node
        """

        for neighbour in self.get_neighbours(curr):
            # Calculate the new total cost
            new_total_cost = curr.total_cost + neighbour.given_cost

            # Check if the neighbour is next to the target node
            if neighbour.pos == curr_target.pos:
                # If so, then the path is found
                # Update the total cost and parent of the neighbour
                neighbour.parent = curr
                self.get_path(neighbour)

                return self.path

            elif neighbour in self.open_list:
                # If the neighbour is in the open list, then update its total cost if necessary
                if new_total_cost < neighbour.total_cost:
                    neighbour.total_cost = new_total_cost
                    neighbour.parent = curr
                    continue

            elif neighbour.state == NodeState.NEW:
                # If the neighbour is a new node, then add it to the open list
                neighbour.state = NodeState.OPEN
                neighbour.parent = curr
                neighbour.total_cost = new_total_cost
                self.open_list.append(neighbour)
                continue

        # When all the neighbours are checked, add the current node to the closed list
        self.closed_list.append(curr)
        curr.state = NodeState.CLOSE
        # Sort the open list by the total cost of the nodes
        self.open_list.sort(key=lambda x: x.total_cost)

    def get_path(self, curr):
        """
        A function to get the path from the worker to the target.
        The function will start from the target and reach the start node recursively.
        It will update the state of the nodes to represent the path.

        :param curr: The current node
        """

        self.has_path = True
        if curr.state != NodeState.TARGET:
            curr.state = NodeState.PATH
        self.path = [curr]
        # Start from the target and reach the start node recursively
        while curr.parent is not None:
            curr = curr.parent
            curr.state = NodeState.PATH
            self.path.append(curr)

        curr.state = NodeState.START

        # Reverse the path to get the correct order
        self.path.reverse()
        # self.path.pop(0)
        self.total_path += self.path
        # self.print_path_description()

    def set_total_path_state(self):
        """
        A function to set the state of the nodes in the total path to PATH.
        """

        for node in self.total_path:
            if self.grid[node.x][node.y].state != NodeState.STOP and self.grid[node.x][node.y].state != NodeState.START:
                self.grid[node.x][node.y].state = node.state

    def get_neighbours(self, curr):
        """
        A function to get the neighbours of the current node.
        The function will check all the neighbours whether it is a block(Shelf), if it is not, add it to the list.

        :param curr: The current node
        :return: A list of nodes representing the neighbours of the current node.
        """

        # North, West, East, South
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbours = []

        # Check all the neighbours of the current node
        # If the neighbour is not a block(Shelf), then add it to the list
        for x_diff, y_diff in directions:
            x = curr.x + x_diff
            y = curr.y + y_diff
            if 0 <= x < self.map_row and 0 <= y < self.map_col:
                if self.grid[x][y].state != NodeState.BLOCK:
                    neighbours.append(self.grid[x][y])

        return neighbours

    def print_map(self):
        print_banner()

        for y in range(self.map_col - 1, -1, -1):
            # Print the y-axis index
            # if the y-axis index is less than 10, then print the index with 2 spaces
            if 0 <= y < 10:
                print(y, end="  ")
            # if the y-axis index is more than 10, then print the index with 1 space
            elif y >= 10:
                print(y, end=" ")
            # Print the map content
            for x in range(self.map_row):
                if self.grid[x][y].state == NodeState.TARGET:
                    print("\U0001F3AF", end=" ")
                elif self.grid[x][y].state == NodeState.STOP:
                    print("\U0001F535", end=" ")
                elif self.grid[x][y].state == NodeState.START:
                    print("\U0001F680", end=" ")
                elif self.grid[x][y].state == NodeState.BLOCK:
                    print("\U0001F6AA", end=" ")
                elif self.grid[x][y].state == NodeState.PATH:
                    print("\U0001F7E9", end=" ")
                    # print("\U0001F7E9", end=" ")

                else:
                    print("\U0001F518", end=" ")
                    # print("\U0001F535", end=" ")
            print()
        # Print the x-axis index
        for i in range(self.map_row + 1):
            # Empty space for the left bottom corner
            if i == 0:
                print(" ", end="  ")
            # Print the x-axis index
            elif 0 < i < 10:
                print(i - 1, end="  ")
            elif i >= 10:
                print(i - 1, end=" ")
        print()
        print()
        print("'\U0001F680': is the start point, '\U0001F3AF': is the target item, '\U0001F7E9' is the path, "
              "'\U0001F6AA' is the shelf location, '\U0001F518' is the empty space ")

    def print_map_single_search(self):
        """A function to visualize the map.
        First, the function will print the map in the terminal.
        The map will be printed in the format of a 2D grid, where origin point is in the bottom left corner of the map.
        To make the index of the map easier to read, the function does the following:
        The map is printed row by row, the first index of each row will be printed to represent the y-axis.
        If the x-axis index is less than 10, then the row number will be printed with 2 spaces.
        If the x-axis index is more than 10, then the row number will be printed with 1 space.
        The last row of will be printed as the x-axis.

        Then, the function will refresh the map with the given refresh rate if is_refresh signal is True.
        """
        print_banner()
        # Print the map
        for y in range(self.map_col - 1, -1, -1):
            # Print the y-axis index
            # if the y-axis index is less than 10, then print the index with 2 spaces
            if 0 <= y < 10:
                print(y, end="  ")
            # if the y-axis index is more than 10, then print the index with 1 space
            elif y >= 10:
                print(y, end=" ")
            # Print the map content
            for x in range(self.map_row):
                if self.grid[x][y].state == NodeState.TARGET:
                    print("\U0001F3AF", end=" ")
                elif self.grid[x][y].state == NodeState.START:
                    print("\U0001F680", end=" ")
                elif self.grid[x][y].state == NodeState.BLOCK:
                    print("\U0001F6AA", end=" ")
                elif self.grid[x][y].state == NodeState.PATH:
                    print("\U0001F7E9", end=" ")
                elif self.grid[x][y].state == NodeState.CLOSE:
                    print("\U0001F534", end=" ")
                elif self.grid[x][y].state == NodeState.OPEN:
                    print("\U0001F50E", end=" ")
                    # print("\U0001F7E9", end=" ")
                else:
                    print("\U0001F518", end=" ")
                    # print("\U0001F535", end=" ")
            print()
        # Print the x-axis index
        for i in range(self.map_row + 1):
            # Empty space for the left bottom corner
            if i == 0:
                print(" ", end="  ")
            # Print the x-axis index
            elif 0 < i < 10:
                print(i - 1, end="  ")
            elif i >= 10:
                print(i - 1, end=" ")
        print()
        print()
        print("'\U0001F680': is the start point, '\U0001F3AF': is where your target item located, "
              "'\U0001F6AA' is the block")
        print("'\U0001F7E9' is the path, '\U0001F50E': is in the node will be searched. "
              "'\U0001F534' is the node has been searched")

        # if is_refresh:
        #     sleep(refresh_rate)
        #     refresh()

    def dump_instruction_into_file(self):
        """A function to dump the instruction into a file.
        The file will be named as "instruction.txt".
        The file will be saved in the same directory as the main.py file.
        """
        with open("instruction.txt", "w", encoding='utf-8') as file:
            # Print the map
            file.write("\n")
            file.write(
                "--------------------------------------------------------------------------------------------------------")
            file.write("\n")
            file.write(
                "▄▀▀▀▀▄      ▄▀▀█▄   ▄▀▀▀▀▄   ▄▀▀▄ ▀▀▄      ▄▀▀▄▀▀▀▄  ▄▀▀█▀▄    ▄▀▄▄▄▄   ▄▀▀▄ █  ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄")
            file.write("\n")
            file.write(
                "█    █      ▐ ▄▀ ▀▄ █     ▄▀ █   ▀▄ ▄▀     █   █   █ █   █  █  █ █    ▌ █  █ ▄▀ ▐  ▄▀   ▐ █   █   █")
            file.write("\n")
            file.write(
                "▐    █        █▄▄▄█ ▐ ▄▄▀▀   ▐     █       ▐  █▀▀▀▀  ▐   █  ▐  ▐ █      ▐  █▀▄    █▄▄▄▄▄  ▐  █▀▀█▀ ")
            file.write("\n")
            file.write(
                "    █        ▄▀   █   █            █          █          █       █        █   █   █    ▌   ▄▀    █ ")
            file.write("\n")
            file.write(
                "  ▄▀▄▄▄▄▄▄▀ █   ▄▀     ▀▄▄▄▄▀    ▄▀         ▄▀        ▄▀▀▀▀▀▄   ▄▀▄▄▄▄▀ ▄▀   █   ▄▀▄▄▄▄   █     █ ")
            file.write("\n")
            file.write(
                "  █         ▐   ▐          ▐     █         █         █       █ █     ▐  █    ▐   █    ▐   ▐     ▐ ")
            file.write("\n")
            file.write("  ▐                              ▐         ▐         ▐       ▐ ▐        ▐        ▐            ")
            file.write("\n")
            file.write(
                "--------------------------------------------------------------------------------------------------------")
            file.write("\n")
            for y in range(self.map_col - 1, -1, -1):
                # Print the y-axis index
                # if the y-axis index is less than 10, then print the index with 2 spaces
                if 0 <= y < 10:
                    file.write(str(y) + "  ")
                # if the y-axis index is more than 10, then print the index with 1 space
                elif y >= 10:
                    file.write(str(y) + " ")
                # Print the map content
                for x in range(self.map_row):
                    if self.grid[x][y].state == NodeState.TARGET:
                        file.write("\U0001F3AF" + " ")
                    elif self.grid[x][y].state == NodeState.STOP:
                        file.write("\U0001F535" + " ")
                    elif self.grid[x][y].state == NodeState.START:
                        file.write("\U0001F680" + " ")
                    elif self.grid[x][y].state == NodeState.BLOCK:
                        file.write("\U0001F6AA" + " ")
                    elif self.grid[x][y].state == NodeState.PATH:
                        file.write("\U0001F7E9" + " ")
                        # print("\U0001F7E9", end=" ")

                    else:
                        file.write("\U0001F518" + " ")
                        # print("\U0001F535", end=" ")
                file.write("\n")
            # Print the x-axis index
            for i in range(self.map_row + 1):
                # Empty space for the left bottom corner
                if i == 0:
                    file.write("  ")
                # Print the x-axis index
                elif 0 < i < 10:
                    file.write(str(i - 1) + "  ")
                elif i >= 10:
                    file.write(str(i - 1) + " ")
            file.write("\n")
            file.write("\n")
            file.write("'\U0001F680': is the start point, '\U0001F3AF': is the target item, '\U0001F7E9' is the path, "
                       "'\U0001F6AA' is the shelf location, '\U0001F518' is the empty space ")

            file.write("\n")
            for instruction in self.total_path_description:
                for sentence in instruction:
                    file.write("\n")
                    file.write(sentence)
                file.write("\n")


def set_path_description(path):
    """A function to print the text path description.
    The function will first check whether the path is found.
    If the path is found, then the function will print the path length and the number of iterations.
    Then the function will record each direction of the current node to the bext node.
    The text path description will be reconstructed by the recorded directions.
    Use two pointers to implement the reconstruction, one pointer points to the current direction,
    if the next direction is the same as the current direction, then the pointer will move to the next direction.
    If the next direction is different from the current direction, then the pointer will stop and record how many
    times the current direction appears and add the text description to the path description list.
    Then the two pointer will move to the next direction.
    """

    pre_x = path[0].x
    pre_y = path[0].y

    path_words = []
    # Record the direction of the current node to the next node
    for i in range(1, len(path)):
        curr_x = path[i].x
        curr_y = path[i].y
        if curr_x == pre_x:  # Vertical
            if curr_y > pre_y:
                path_words.append("UP")
            else:
                path_words.append("DOWN")
        else:
            if curr_x > pre_x:  # Horizontal
                path_words.append("RIGHT")
            else:
                path_words.append("LEFT")
        pre_x = curr_x
        pre_y = curr_y
    sentence = "From " + str(path[0].pos) + " to " + str(path[-1].pos) + ": " + "length: " + str(len(path) - 1)
    path_description = [sentence]

    # Reconstruct the text description
    step = 1
    i = 0

    while i < len(path_words):
        freq = 0
        j = i

        if path_words[i] == path_words[j]:
            # If the next direction is the same as the current direction, j pointer move to the next direction.
            while j < len(path_words) and path_words[i] == path_words[j]:
                freq += 1
                j += 1
            # Stop and record how many times the current direction appears.
            sentence = "   - " + "Step " + str(step) + ": Go " + path_words[i] + " " + str(freq) + " units."
            # Move i pointer to the j pointer position.
            i = j
        else:
            # If the next direction is different from the current direction, record the current direction.
            sentence = "   - " + "Step " + str(step) + ": Go " + path_words[i] + " " + str(freq) + " units."
            # Move i and j pointer to the next direction.
            i += 1

        # Add the text description to the path description list
        step += 1
        path_description.append(sentence)

    return path_description


def print_path_descriptions(total_path_descriptions, total_path):
    """A function to print the text path description.
    The function will print the text path description for each path.
    """
    print("The path length is: ", total_path)
    for description in total_path_descriptions:
        for sentence in description:
            print(sentence)
        print()