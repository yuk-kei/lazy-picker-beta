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
        self.weight = len(path) - 1

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
        self.num_of_vertexes = num_of_vertexes
        self.path = parent.path + [vertex] if parent else [vertex]
        self.cost = cost
        self.matrix = None
        self.len = len(self.path)
        self.visited = parent.visited.copy() if parent else [False for _ in range(num_of_vertexes)]

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        return f"PathNode({self.vertex}, {self.parent}, {self.path}, {self.cost})"

    def __eq__(self, other):
        return self.vertex == other.vertex


def print_matrix(matrix):
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
    Branch and bound algorithm
    """

    def __init__(self, adjacent_map, vertexes, size, limit_time=True):

        self.adjacent_map = adjacent_map
        self.vertexes = vertexes
        self.nums_of_vertexes = len(vertexes)
        self.matrix = None
        self.limit_time = limit_time
        self.size = size
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
        """ Set matrix from adjacent map """

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
        if self.nums_of_vertexes > 1:
            random_index = random.randint(0, self.nums_of_vertexes - 1)
        else:
            # print((len(self.vertexes)))
            random_index = 0
        random_vertexes = []
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
                print("what the fuck")
                return self.generate_result(curr_node)

            # set the limit time, which is 14 seconds, stop the algorithm and return a result
            if self.limit_time and curr_time - start_time > 14:
                print("Time is up! Returning what we current got")
                max_node = curr_node
                while not self.pq.empty():
                    temp_node = self.pq.get()
                    if max_node.len < temp_node.len:
                        max_node = temp_node

                # print_matrix(max_node.matrix)
                # print(max_node.visited)
                for index in range(self.nums_of_vertexes):
                    if not max_node.visited[index]:
                        next_vertex = self.vertexes[index]
                        new_matrix = copy.deepcopy(max_node.matrix)

                        next_node = PathTreeNode(next_vertex, self.nums_of_vertexes, max_node.cost, max_node)

                        self.reduce_matrix(new_matrix, next_node)

                        # print_matrix(max_node.matrix)
                        # print("pre_max_node: ", max_node.len, " size: ", self.size)
                        max_node = next_node
                        # print("max_node: ", max_node.len, " size: ", self.size)
                        # print_matrix(max_node.matrix)

                # print("Success!")
                # print("Path: ")
                # for vertex in max_node.path:
                #     print(vertex.block, end=" ")
                return self.generate_result(max_node)

            for index in range(self.nums_of_vertexes):
                if not curr_node.visited[index]:
                    next_vertex = self.vertexes[index]
                    new_matrix = copy.deepcopy(curr_node.matrix)

                    next_node = PathTreeNode(next_vertex, self.nums_of_vertexes, curr_node.cost, curr_node)
                    self.reduce_matrix(new_matrix, next_node)
                    if next_node.len == self.size:
                        return self.generate_result(next_node)
                    self.pq.put(next_node)

    # def iterate_child_node(self, curr_node):
    #
    #             # print("put: ", next_node.vertex.block)
    #             # print("cost", next_node.cost, "next_node: ", next_node.len, " size: ", self.size)
    #             # print()

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
        # if it is reduced by pre to curr

        # ignore the same target
        for index in self.same_target[curr_index]:
            curr_tree_node.visited[index] = True
            # set the row and column of the same target to inf
            for i in range(len(matrix)):
                matrix[i][index] = float("inf")
            for j in range(len(matrix)):
                matrix[index][j] = float("inf")

        if curr_tree_node.parent is not None:

            parent = curr_tree_node.parent
            pre_vertex = parent.vertex
            pre_index = pre_vertex.index

            reduced_cost = 0

            # print_matrix(matrix)
            # reduce row
            for i in range(len(matrix)):

                row = matrix[i]
                # get the min value of the row
                min_value = min(row)
                print("min_value: ", min_value)
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

            # reduce column
            for j in range(len(matrix[0])):
                column = [row[j] for row in matrix]
                min_value = min(column)
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

            reduction = matrix[pre_index][curr_index]
            # delete the row of the pre_vertex
            for j in range(len(matrix)):
                matrix[pre_index][j] = float("inf")
            # delete the column of the curr_vertex
            for i in range(len(matrix)):
                matrix[i][curr_index] = float("inf")
            #
            # print("parent_index: ", curr_tree_node.parent.vertex.index)
            # print("parent: ", curr_tree_node.parent.vertex.block)
            # print("parent_cost: ", curr_tree_node.parent.cost)
            #
            # print("curr_index: ", curr_index)
            # print("curr_vertex: ", curr_vertex.block)
            # print("reduced_cost: ", reduced_cost)
            # print("reduction: ", reduction)
            # print("curr_cost: ", curr_tree_node.cost)
            #
            # print("After reduce:")

            # for vertex in curr_tree_node.path:
            #     print(vertex.block, end=" -> ")
            #
            # print()
            # print(curr_tree_node.len)
            # print(self.size)
            print_matrix(matrix)

            print("End reduce matrix")
            # input("Press Enter to continue...")
            curr_tree_node.cost += reduction
            curr_tree_node.cost += reduced_cost
        curr_tree_node.matrix = matrix

    def generate_result(self, curr_node):
        """
        Generate the result
        """
        print("curr_node: ", curr_node.vertex.block)

        path_vertexes = curr_node.path
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


class DummyGreedy:
    """
    A dummy greedy algorithm to find the nearest vertex to the current vertex for every step
    """
    def __init__(self, adjacent_map, vertexes, size):

        self.adjacent_map = adjacent_map
        self.vertexes = vertexes
        self.nums_of_vertexes = len(vertexes)
        self.size = size
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

    def solver(self):
        curr_vertex = self.vertexes[0]

        self.backtrack(curr_vertex)
        return self.generate_path()

    def backtrack(self, curr_vertex):

        if len(self.result) == self.size - 1:
            self.result.append(self.adjacent_map[curr_vertex.index][0])
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
        for i in range(len(self.result)):
            edge = self.result[i]
            edge.path[-1].state = NodeState.STOP
            total_cost += edge.weight
            for i in range(1, len(edge.path)):
                if edge.path[i].state == NodeState.STOP:
                    continue

                edge.path[i].state = NodeState.PATH

            final_path += edge.path
            final_path_description.append(edge.path_description)

        final_path[-1].state = NodeState.START
        return final_path, final_path_description, total_cost
