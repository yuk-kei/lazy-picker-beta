import copy
import random
import time
from queue import PriorityQueue

from data import NodeState


class Edge:
    def __init__(self, node1, node2, path, path_description):
        self.node1 = node1
        self.node2 = node2
        self.path = path
        self.path_description = path_description
        self.weight = 0 if len(path) == 0 else len(path) - 1
        # self.weight = len(path)

    def __lt__(self, other):
        return self.weight < other.weight

    def __str__(self):
        return f"Edge({self.node1}, {self.node2}, {self.path}, {self.weight})"


class Vertex:
    def __init__(self, node, index, is_entrance_of=None):
        self.block = node
        self.level = 0
        self.is_entrance_of = is_entrance_of
        self.index = index

    def __str__(self):
        return f"Vertex({self.block}, {self.is_entrance_of})"

    def __eq__(self, other):
        return self.block == other.block


class PathTreeNode:
    """
    This class represents a Treed node to store
    """

    def __init__(self, vertex, num_of_vertexes, cost=0, parent=None):
        self.vertex = vertex
        self.parent = parent
        self.first_index = vertex.index if parent is None else parent.first_index
        self.num_of_vertexes = num_of_vertexes
        self.path = parent.path + [vertex] if parent else [vertex]
        self.cost = cost
        self.matrix = None
        self.len = len(self.path)
        self.visited = parent.visited.copy() if parent else [False for _ in range(num_of_vertexes)]

    def __lt__(self, other):
        if self.cost == other.cost:
            return self.len > other.len
        return self.cost < other.cost

    def __str__(self):
        return f"PathNode({self.vertex}, {self.parent}, {self.path}, {self.cost})"

    def __eq__(self, other):
        return self.vertex == other.vertex


def print_matrix(matrix):
    """
    Print matrix , used for debugging
    Iterate through the matrix and print each element
    :param matrix: The matrix to be printed
    """
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] < 10:
                print(matrix[i][j], end="   ")
            elif matrix[i][j] == float("inf"):
                print("inf", end=" ")
            else:
                print(matrix[i][j], end="  ")
        print()





class Branch_n_Bound:
    """
    Branch and bound algorithm to find the shortest path
    """

    def __init__(self, adjacent_map, vertexes, size, limit_time=60, is_limit_time=True,destination=None):

        self.adjacent_map = adjacent_map
        self.vertexes = vertexes
        self.nums_of_vertexes = len(vertexes)
        self.matrix = None
        self.limit_time = limit_time
        self.is_limit_time = is_limit_time
        self.size = size
        self.has_destination = destination is not None
        self.destination = destination
        self.pq = PriorityQueue()
        self.same_target = {}
        self.result = []
        # Set up the index mapping to the same target vertexes
        for i in range(self.nums_of_vertexes):
            curr_vertex = set()

            for j in range(self.nums_of_vertexes):
                if i != j and vertexes[i].is_entrance_of == vertexes[j].is_entrance_of:
                    curr_vertex.add(j)
            self.same_target[i] = curr_vertex
            # print(i, " ", curr_vertex)

    def set_matrix(self):
        """
        Iterate through the adjacent map and set the matrix
        f the adjacent map is None, set the matrix to infinity
        Else set the matrix to the weight of the edge
        """

        self.matrix = [[0 for i in range(self.nums_of_vertexes)] for j in range(self.nums_of_vertexes)]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.adjacent_map[i][j] is None:

                    self.matrix[i][j] = float("inf")
                else:
                    self.matrix[i][j] = self.adjacent_map[i][j].weight
        print("Original matrix: ")
        print_matrix(self.matrix)

    def solve(self):
        """
        Solve the problem with branch and bound algorithm
        1. Select a random vertex as the root
        2. set the other entrance with the same target to infinity
        2. Reduce the matrix
        3. Put the root into the priority queue
        4. While the priority queue is not empty:
            4.1 Get the node with the smallest cost
            4.2 If the node is a leaf node:
                return the result
            4.3 Else:
                Keep reducing the matrix and put the node into the priority queue
        """
        start_time = time.time()
        if self.nums_of_vertexes > 1 and not self.has_destination:
            random_index = random.randint(0, self.nums_of_vertexes - 1)
        else:
            # print((len(self.vertexes)))
            random_index = 0
        # random_vertexes = []
        # random_index = 0
        random_vertex = self.vertexes[random_index]
        root = PathTreeNode(random_vertex, self.nums_of_vertexes)
        start_matrix = copy.deepcopy(self.matrix)

        self.reduce_matrix(start_matrix, root)
        self.pq.put(root)

        for other_index in self.same_target[random_index]:
            root = PathTreeNode(self.vertexes[other_index], self.nums_of_vertexes)
            start_matrix = copy.deepcopy(self.matrix)

            self.reduce_matrix(start_matrix, root)
            self.pq.put(root)

        print("Initial end")
        iterate = 0
        while not self.pq.empty():
            iterate += 1
            # print("pq size: ", self.pq.qsize())

            curr_node = self.pq.get()

            # print_matrix(curr_node.matrix)
            curr_time = time.time()

            # if all(curr_node.visited):
            if curr_node.len == self.size:
                # print("Success!")
                # print("Path: ")
                # for vertex in curr_node.path:
                #     print(vertex.block, end=" ")
                print("start_index: ", self.vertexes[random_index].block)

                return self.generate_result(curr_node)

            elif self.has_destination and curr_node.len == self.size - 1:

                return self.generate_result_with_destination(curr_node, self.destination)


            # set the limit time, which default is 60 seconds, stop the algorithm and return a result
            if self.is_limit_time and self.limit_time and curr_time - start_time > self.limit_time:
                print("Time is up! Returning what we current got")
                max_node = curr_node
                while not self.pq.empty():
                    temp_node = self.pq.get()
                    if max_node.len < temp_node.len:
                        max_node = temp_node

                for index in range(self.nums_of_vertexes):
                    if not max_node.visited[index]:
                        next_vertex = self.vertexes[index]
                        new_matrix = copy.deepcopy(max_node.matrix)
                        next_node = PathTreeNode(next_vertex, self.nums_of_vertexes, max_node.cost, max_node)
                        self.reduce_matrix(new_matrix, next_node)
                        max_node = next_node

                return self.generate_result(max_node)

            for index in range(self.nums_of_vertexes):
                if not curr_node.visited[index]:
                    next_vertex = self.vertexes[index]
                    new_matrix = copy.deepcopy(curr_node.matrix)

                    next_node = PathTreeNode(next_vertex, self.nums_of_vertexes, curr_node.cost, curr_node)
                    self.reduce_matrix(new_matrix, next_node)

                    self.pq.put(next_node)




    def reduce_matrix(self, matrix, curr_tree_node):
        """
        Reduce Matrix (rows & columns to at least one 0) = reduced cost
        1. If it is not the root node, reduce the matrix by pre to curr
        2. Set the same target row and column to infinity
        2. Reduce the matrix by finding the minimum value in each row and subtracting it from each element of that row
        3. Set the visited vertex to True
        4. Set the same target vertex to True
        """

        # input("Press Enter to continue...")
        curr_vertex = curr_tree_node.vertex
        curr_index = curr_vertex.index
        curr_tree_node.visited[curr_index] = True
        self.ignore_same_target_entrance(curr_index, curr_tree_node, matrix)
        # if curr_tree_node.parent is None: it is a root node
        if curr_tree_node.parent is None:

            print()
            print("root matrix: ", curr_index)
            reduce_cost, matrix = self.reduce_row_n_col(matrix)
            curr_tree_node.cost = reduce_cost
            print_matrix(matrix)
            # ignore the entrance with same target as current vertex

        else:
            # if it is not the root node
            # input("Press Enter to continue...")
            parent = curr_tree_node.parent
            pre_vertex = parent.vertex
            pre_index = pre_vertex.index
            first_index = curr_tree_node.first_index

            print("parent matrix: ", )
            print("pre_index: ", pre_index, "-> curr_index: ", curr_index)
            print_matrix(parent.matrix)

            # reduce_cost, matrix = self.reduce_row_n_col(matrix)

            main_reduce_cost = parent.cost
            reduction = matrix[pre_index][curr_index]

            for vertex in curr_tree_node.path:
                print(vertex.block, end=" -> ")

            print("main reduce cost: ", main_reduce_cost)
            print("reduction: ", reduction)

            # delete the row of the pre_vertex
            for j in range(len(matrix)):
                matrix[pre_index][j] = float("inf")
            # delete the column of the curr_vertex
            for i in range(len(matrix)):
                matrix[i][curr_index] = float("inf")

            matrix[curr_index][first_index] = float("inf")

            reduce_cost, matrix = self.reduce_row_n_col(matrix)

            curr_tree_node.cost += reduction
            curr_tree_node.cost += reduce_cost

            print()
            print("curr_matrix: ")
            print_matrix(matrix)
            print("current length: ", curr_tree_node.len, "total size: ", self.size)
            print()
            print("curr_vertex: ", curr_vertex.block)

            print("parent_cost: ", parent.cost)
            print("deduction: (parent, curr)", "(", pre_index, ",", curr_index, ")", " = ", reduction)
            print("reduce_cost: ", reduce_cost)
            # print("reduced_cost: ", reduced_cost)
            print("curr_cost: ", curr_tree_node.cost)

        curr_tree_node.matrix = matrix
        print("------------------------------------------")

    def ignore_same_target_entrance(self, curr_index, curr_tree_node, matrix):
        for index in self.same_target[curr_index]:
            curr_tree_node.visited[index] = True
            # set the row and column of the same target to inf
            for i in range(len(matrix)):
                matrix[i][index] = float("inf")
            for j in range(len(matrix)):
                matrix[index][j] = float("inf")

    def reduce_row_n_col(self, matrix):

        print("before reduce row and col: ")
        print_matrix(matrix)
        print()
        print("each row min value: ")

        reduced_cost = 0
        for i in range(len(matrix)):

            row = matrix[i]
            # get the min value of the row
            min_value = min(row)
            print(min_value, end=" ")
            if min_value == float("inf") or min_value == 0:
                continue

            else:
                # reduce each element of the row by the min value
                for j in range(len(row)):
                    if row[j] != float("inf") and row[j] != 0:
                        row[j] -= min_value
                matrix[i] = row
                # get the total cost of each row
                reduced_cost += min_value

        print()
        print("row_reduced_cost: ", reduced_cost)
        print()
        print("each column min value:")

        # reduce column
        for j in range(len(matrix[0])):
            column = [row[j] for row in matrix]
            min_value = min(column)
            print(min_value, end=" ")
            if min_value == float("inf") or min_value == 0:
                continue
            else:
                # reduce each element of the column by the min value
                for i in range(len(column)):
                    if column[i] != float("inf") and column[i] != 0:
                        column[i] -= min_value
                for i in range(len(matrix)):
                    matrix[i][j] = column[i]
                reduced_cost += min_value

        print()
        print("total_reduced_cost: ", reduced_cost)
        print()
        print("after reduce row and col: ")
        print_matrix(matrix)
        print()

        return reduced_cost, matrix

    def generate_result(self, curr_node):
        """
        Generate the result
        """

        print("curr_node: ", curr_node.vertex.block)
        print("curr_node matrix: ")
        print_matrix(curr_node.matrix)
        print("curr_node cost: ", curr_node.cost)
        print("curr_node path: ")
        for vertex in curr_node.path:
            print(vertex.block, end=" -> ")
        print()
        path_vertexes = curr_node.path
        print("start_index: ", path_vertexes[0].index)
        print("start block: ", path_vertexes[0].block)
        final_path = []
        final_path_description = []
        total_cost = 0
        start_index = 0
        for i in range(len(path_vertexes)):
            if path_vertexes[i].index == 0:
                start_index = i
                # print(path_vertexes[i].block)
                break
        curr_index = start_index

        for i in range(start_index, len(path_vertexes) - 1):
            curr_index = i + 1
            self.result.append(self.adjacent_map[path_vertexes[i].index][path_vertexes[curr_index].index])

        self.result.append(self.adjacent_map[path_vertexes[curr_index].index][path_vertexes[0].index])
        for i in range(start_index):
            self.result.append(self.adjacent_map[path_vertexes[i].index][path_vertexes[i + 1].index])

        for edge in self.result:
            if len(edge.path) == 0:
                continue
            edge.path[0].state = NodeState.STOP
            total_cost += edge.weight
            for i in range(1, len(edge.path)):
                if edge.path[i].state == NodeState.STOP:
                    continue

                edge.path[i].state = NodeState.PATH

            final_path += edge.path
            final_path_description.append(edge.path_description)
        final_path[-1].state = NodeState.START
        return final_path, final_path_description, total_cost

    def generate_result_with_destination(self, curr_node, destination):
        """
        Generate the result with destination
        :param curr_node: The current node
        :param destination: The destination
        :return: The result
        """

        final_path = []
        final_path_description = []
        total_cost = 0
        curr_vertex = curr_node.vertex
        path_vertexes = curr_node.path
        for i in range(0, len(path_vertexes) - 1):
            curr_index = i + 1
            self.result.append(self.adjacent_map[path_vertexes[i].index][path_vertexes[curr_index].index])

        self.result.append(self.adjacent_map[curr_vertex.index][destination.index])

        for edge in self.result:
            if len(edge.path) == 0:
                continue
            edge.path[0].state = NodeState.STOP
            total_cost += edge.weight
            for i in range(1, len(edge.path)):
                if edge.path[i].state == NodeState.STOP:
                    continue

                edge.path[i].state = NodeState.PATH

            final_path += edge.path
            final_path_description.append(edge.path_description)
        final_path[-1].state = NodeState.START
        return final_path, final_path_description, total_cost


def color_edge(edge):
    edge.path[0].state = NodeState.STOP
    for j in range(1, len(edge.path)):
        if edge.path[j].state == NodeState.STOP:
            continue

        edge.path[j].state = NodeState.PATH


class NearestNeighbor:
    """
    A dummy greedy algorithm to find the nearest vertex to the current vertex for every step
    """

    def __init__(self, adjacent_map, vertexes, size):

        self.adjacent_map = adjacent_map
        self.vertexes = vertexes
        self.nums_of_vertexes = len(vertexes)
        self.size = size
        self.start_index = 0
        self.same_target = {}
        self.visited = [False] * self.nums_of_vertexes
        self.result = []
        # print("Failed to find the optimal solution, using greedy algorithm instead")
        for i in range(self.nums_of_vertexes):
            curr_vertex = set()

            for j in range(self.nums_of_vertexes):
                if i != j and vertexes[i].is_entrance_of == vertexes[j].is_entrance_of:
                    curr_vertex.add(j)
            self.same_target[i] = curr_vertex

    def choose_first_vertex(self):

        if self.nums_of_vertexes > 1:
            self.start_index = random.randint(0, self.nums_of_vertexes - 1)
        else:
            # print((len(self.vertexes)))
            self.start_index = 0
        curr_vertex = self.vertexes[self.start_index]
        return curr_vertex

    def solver(self):

        # start from a random vertex
        curr_vertex = self.choose_first_vertex()

        self.backtrack(curr_vertex)
        return self.generate_result()

    def iterate(self, curr_vertex):

        curr_index = curr_vertex.index
        # find an edge with the minimum weight
        next_min = float("inf")
        min_edge = None
        min_index = 0
        for (i, edge) in enumerate(self.adjacent_map[curr_index]):
            if edge is not None and edge.weight < next_min and not self.visited[i]:
                next_min = edge.weight
                min_edge = edge
                min_index = i
        # set the min edge to the next vertex
        color_edge(min_edge)
        self.result.append(min_edge)

        # set the current vertex as visited
        self.visited[curr_index] = True
        for index in self.same_target[curr_index]:
            self.visited[index] = True

        return self.vertexes[min_index], min_edge

    def backtrack(self, curr_vertex):

        if len(self.result) == self.size - 1:
            self.result.append(self.adjacent_map[curr_vertex.index][self.start_index])
            return

        curr_index = curr_vertex.index
        self.visited[curr_index] = True
        for index in self.same_target[curr_index]:
            self.visited[index] = True

        next_min = float("inf")
        min_edge = None
        min_index = 0
        for (i, edge) in enumerate(self.adjacent_map[curr_index]):
            if edge is not None and edge.weight < next_min and not self.visited[i]:
                next_min = edge.weight
                min_edge = edge
                min_index = i
        self.result.append(min_edge)
        self.backtrack(self.vertexes[min_index])

    def generate_path(self):
        final_path = []
        final_path_description = []
        total_cost = 0
        final_path, total_cost, final_path_description = self.construct_path(final_path, final_path_description,
                                                                             total_cost, len(self.result))

        final_path[-1].state = NodeState.START
        return final_path, final_path_description, total_cost

    def generate_result(self):
        """
        Generate the result
        """
        final_path = []
        final_path_description = []
        total_cost = 0

        start_index = 0
        for i in range(len(self.result)):
            if self.result[i].node1.index == 0:
                start_index = i
                # print(path_vertexes[i].block)
                break

        final_path, total_cost, final_path_description = self.construct_path(final_path, final_path_description,
                                                                             total_cost, len(self.result), start_index)
        final_path, total_cost, final_path_description = self.construct_path(final_path, final_path_description,
                                                                             total_cost, start_index)

        return final_path, final_path_description, total_cost

    def construct_path(self, final_path, final_path_description, total_cost, end_index, start_index=0):
        for i in range(start_index, end_index):
            edge = self.result[i]
            edge.path[-1].state = NodeState.STOP
            total_cost += edge.weight
            color_edge(edge)

            final_path += edge.path
            final_path_description.append(edge.path_description)
        return final_path, total_cost, final_path_description

    # def debug(self):