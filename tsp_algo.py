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

    def __init__(self, adjacent_map, vertexes, size, limit_time=60, is_limit_time=True, destination=None,
                 is_debug=False):

        self.adjacent_map = adjacent_map
        self.vertexes = vertexes
        self.nums_of_vertexes = len(vertexes)
        self.matrix = None
        self.limit_time = limit_time
        self.is_limit_time = is_limit_time
        self.size = size
        self.destination = destination
        self.destination_index = None if destination is None else self.nums_of_vertexes - 1
        self.is_debug = is_debug
        self.pq = PriorityQueue()
        self.same_target = {}
        self.is_entrance_of_index = {}
        self.result = []
        # Set up the index mapping to the same target vertexes
        for i in range(self.nums_of_vertexes):
            curr_vertex = set()

            for j in range(self.nums_of_vertexes):
                if i != j and vertexes[i].is_entrance_of is not None \
                        and vertexes[i].is_entrance_of == vertexes[j].is_entrance_of:
                    curr_vertex.add(j)
            self.same_target[i] = curr_vertex
            # print(i, " ", curr_vertex)

        # Set up the index mapping to the same target vertexes
        node_index = 0
        self.is_entrance_of_index[0] = node_index
        pre_target_block = vertexes[0].is_entrance_of
        for i in range(1, len(vertexes)):
            curr_target_block = vertexes[i].is_entrance_of
            if curr_target_block is None:
                self.is_entrance_of_index[i] = node_index
            elif curr_target_block != pre_target_block:
                node_index += 1
                self.is_entrance_of_index[i] = node_index
            else:
                self.is_entrance_of_index[i] = node_index
            pre_target_block = curr_target_block

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

        if self.is_debug:
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
            random_index = 0

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

            parent_node = self.pq.get()

            # print_matrix(curr_node.matrix)
            curr_time = time.time()

            # if all(curr_node.visited):
            if parent_node.len == self.size:
                # print("Success!")
                if self.is_debug:
                    print("size of the path:", self.size)
                    print("Actual size of the path:", parent_node.len)
                    print("Actual number of vertexes:", len(parent_node.path))
                    print("Path: ")
                    for vertex in parent_node.path:
                        print(vertex.block, end=" ")

                    print("start_index: ", self.vertexes[random_index].block)
                total_path, total_path_description, total_length = self.generate_result(parent_node)
                return False, total_path, total_path_description, total_length

            # elif self.has_destination and curr_node.len == self.size - 1:
            #
            #     return self.generate_result_with_destination(curr_node, self.destination)

            # set the limit time, which default is 60 seconds, stop the algorithm and return a result

            if self.is_limit_time and self.limit_time and curr_time - start_time > self.limit_time:
                # If we want to return a more decent result, we can use the following code """
                # --------------------------------------------------------------------------------"""
                # # If it needs a destination, return the nearest neighbor result
                # if self.destination is not None:
                #     total_path, total_path_description, total_length = \
                #         NearestNeighbor(self.adjacent_map, self.vertexes, self.size, self.destination).solver()
                #     return True, total_path, total_path_description, total_length
                #
                # # Else, return the current best result
                # max_node = parent_node
                # while not self.pq.empty():
                #     temp_node = self.pq.get()
                #     if max_node.len < temp_node.len:
                #         max_node = temp_node
                #
                # for index in range(self.nums_of_vertexes):
                #     if not max_node.visited[index]:
                #         next_vertex = self.vertexes[index]
                #         new_matrix = copy.deepcopy(max_node.matrix)
                #         next_node = PathTreeNode(next_vertex, self.nums_of_vertexes, max_node.cost, max_node)
                #         self.reduce_matrix(new_matrix, next_node)
                #         max_node = next_node

                # total_path, total_path_description, total_length = self.generate_result(max_node)
                # --------------------------------------------------------------------------------
                org_path = []
                visited = [False for i in range(self.nums_of_vertexes)]
                for index in range(self.nums_of_vertexes):
                    if not visited[index]:
                        org_path.append(self.vertexes[index])
                        for other_index in self.same_target[index]:
                            visited[other_index] = True
                final_vertex = None
                if self.nums_of_vertexes != 0:
                    final_vertex = self.vertexes[self.nums_of_vertexes - 1]
                org_node = PathTreeNode(final_vertex, self.nums_of_vertexes)
                org_node.path = org_path
                total_path, total_path_description, total_length = self.generate_result(org_node)
                return True, total_path, total_path_description, total_length

            pre_node = None
            for index in range(self.nums_of_vertexes):

                # optimization: if the entrance vertex has other same target entrance's vertex has been visited,
                # then use the same matrix as the previous node, but recalculated the cost
                if not parent_node.visited[index]:
                    next_vertex = self.vertexes[index]
                    if pre_node is not None and next_vertex.is_entrance_of is not None \
                            and pre_node.vertex.is_entrance_of == next_vertex.is_entrance_of:
                        # the matrix is the same as the previous node
                        new_matrix = copy.deepcopy(pre_node.matrix)
                        next_node = PathTreeNode(next_vertex, self.nums_of_vertexes, pre_node.cost, pre_node)
                        # need to recalculate the cost, delete the pre reduction
                        cost = pre_node.cost - parent_node.matrix[parent_node.vertex.index][pre_node.vertex.index]
                        # add the current reduction
                        next_node.cost = cost + parent_node.matrix[parent_node.vertex.index][index]
                        # set the path
                        next_node.path = parent_node.path + [next_vertex]
                        next_node.len = parent_node.len + 1
                        next_node.matrix = new_matrix

                    else:
                        new_matrix = copy.deepcopy(parent_node.matrix)
                        next_node = PathTreeNode(next_vertex, self.nums_of_vertexes, parent_node.cost, parent_node)
                        self.reduce_matrix(new_matrix, next_node)

                    # Add the route back to the start node
                    if next_node.len == self.size:
                        final_value = next_node.matrix[index][next_node.first_index]
                        if final_value != float("inf"):
                            next_node.cost += final_value

                    pre_node = next_node
                    self.pq.put(next_node)

    def reduce_matrix(self, matrix, curr_tree_node):
        """
        Reduce Matrix (rows & columns to at least one 0) = reduced cost
        1. Mark the current entrance node and the same target entrance node as visited
        2. If it is a root node,
            2.1 Set the vertex of same target nodes' row and column to infinity
            2.2 Reduce the matrix to get the main reduced cost
        3. Else, the main reduced cost is the parent's main reduced cost
            3.1 get the matrix[pre_index][curr_index] the value as reduction
            3.2 reduce the matrix to get the reduced cost
            3.3 set the current node's cost to the parent's cost + reduction + reduced cost
        """

        curr_vertex = curr_tree_node.vertex
        curr_index = curr_vertex.index

        # Mark the current entrance node and the same target entrance node as visited
        curr_tree_node.visited[curr_index] = True
        for index in self.same_target[curr_index]:
            curr_tree_node.visited[index] = True

        # if curr_tree_node.parent is None: it is a root node
        if curr_tree_node.parent is None:

            if self.is_debug:
                print()
                print("root matrix of index: ", curr_index)
                print("curr_node: ", curr_vertex.block)

            # Set the vertex of same target nodes' row and column to infinity
            for index in self.same_target[curr_index]:

                for i in range(len(matrix)):
                    matrix[i][index] = float("inf")

                for j in range(len(matrix)):
                    matrix[index][j] = float("inf")

            #  Reduce the matrix to get the main reduced cost
            reduce_cost, matrix = self.reduce_each_row_n_col(matrix)

            curr_tree_node.cost = reduce_cost

        else:
            # if it is not the root node

            parent = curr_tree_node.parent
            pre_vertex = parent.vertex
            pre_index = pre_vertex.index

            if self.is_debug:
                print("parent matrix: ", )
                print("pre_index: ", pre_index, "-> curr_index: ", curr_index)
                print_matrix(parent.matrix)

            # reduce_cost, matrix = self.reduce_row_n_col(matrix)

            main_reduce_cost = parent.cost
            reduction = matrix[pre_index][curr_index]

            if self.is_debug:
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

            self.ignore_same_target_entrance(pre_index, curr_index, matrix)

            # reduce_cost, matrix = self.reduce_row_n_col(matrix)
            reduce_cost, matrix = self.reduce_each_row_n_col(matrix)
            curr_tree_node.cost += reduction
            curr_tree_node.cost += reduce_cost

            if self.is_debug:
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
        if self.is_debug:
            print("------------------------------------------")

    def ignore_same_target_entrance(self, pre_index, curr_index, matrix):
        for index in self.same_target[pre_index]:
            for j in range(len(matrix)):
                matrix[index][j] = float("inf")

        for index in self.same_target[curr_index]:
            for i in range(len(matrix)):
                matrix[i][index] = float("inf")

    def reduce_each_row_n_col(self, matrix):

        if self.is_debug:
            print("before reduce row and col: ")
            print_matrix(matrix)
            print()
            print("each row min value: ")

        reduced_row_cost = 0
        node_start_row_index = 0
        node_end_row_index = node_start_row_index + 1

        while node_end_row_index < len(matrix):
            while node_end_row_index < len(matrix) and self.is_entrance_of_index[node_start_row_index] \
                    == self.is_entrance_of_index[node_end_row_index]:
                node_end_row_index += 1

            curr_row_min = float("inf")

            break_outer_loop = False
            for i in range(node_start_row_index, node_end_row_index):

                for j in range(len(matrix)):
                    # search the min value of each row belongs to the current node
                    if matrix[i][j] < curr_row_min:
                        curr_row_min = matrix[i][j]
                        # if the min value is 0, then break the loop
                        if curr_row_min == 0:
                            break_outer_loop = True
                            break

                if break_outer_loop:
                    break
            '''--------------------------------------------'''
            if self.is_debug:
                print(curr_row_min, end=" ")
            '''--------------------------------------------'''
            # get the min value of the row
            if curr_row_min != 0 and curr_row_min != float("inf"):
                # reduce each element of the row by the min value
                for i in range(node_start_row_index, node_end_row_index):
                    for j in range(len(matrix)):
                        if matrix[i][j] != float("inf") and matrix[i][j] != 0:
                            matrix[i][j] -= curr_row_min

                reduced_row_cost += curr_row_min

            node_start_row_index = node_end_row_index

        if self.is_debug:
            print()
            print("row_reduced_cost: ", reduced_row_cost)
            print()
            print("each column min value:")

        # reduced_col_cost = 0
        node_start_col_index = 0
        reduced_col_cost = 0
        node_end_col_index = node_start_col_index + 1
        while node_end_col_index < len(matrix):
            while node_end_col_index < len(matrix) and self.is_entrance_of_index[node_start_col_index] == \
                    self.is_entrance_of_index[node_end_col_index]:
                node_end_col_index += 1

            curr_col_min = float("inf")

            break_outer_loop = False
            for j in range(node_start_col_index, node_end_col_index):
                for i in range(len(matrix)):
                    # search the min value of each column belongs to the current node
                    if matrix[i][j] < curr_col_min:
                        curr_col_min = matrix[i][j]
                        # if the min value is 0, then break the loop
                        if curr_col_min == 0:
                            break_outer_loop = True
                            break

                if break_outer_loop:
                    break

            """--------------------------------------------"""
            if self.is_debug:
                print(curr_col_min, end=" ")
            """--------------------------------------------"""

            # get the min value of the column
            if curr_col_min != 0 and curr_col_min != float("inf"):
                # reduce each element of the column by the min value
                for j in range(node_start_col_index, node_end_col_index):
                    for i in range(len(matrix)):
                        if matrix[i][j] != float("inf") and matrix[i][j] != 0:
                            matrix[i][j] -= curr_col_min

                reduced_col_cost += curr_col_min
            node_start_col_index = node_end_col_index

        total_reduced_cost = reduced_row_cost + reduced_col_cost
        if self.is_debug:
            print()
            print("col_reduced_cost: ", reduced_col_cost)
            print("total_reduced_cost: ", total_reduced_cost)
            print()
            print("after reduce row and col: ")
            print_matrix(matrix)
            print()

        return total_reduced_cost, matrix

    def generate_result(self, curr_node):
        """
        Generate the result of the TSP problem by the final node of the tree

        :param curr_node: the current node
        :return: the final path
        """
        path_vertexes = curr_node.path

        if self.is_debug:
            print("curr_node: ", curr_node.vertex.block)
            print("curr_node matrix: ")
            print_matrix(curr_node.matrix)
            print("curr_node cost: ", curr_node.cost)
            print("curr_node path: ")
            for vertex in curr_node.path:
                print(vertex.block, end=" -> ")
            print()

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
            if edge is None or len(edge.path) == 0:
                continue
            edge.path[0].state = NodeState.STOP
            total_cost += edge.weight
            for i in range(1, len(edge.path)):
                if edge.path[i].state == NodeState.STOP:
                    continue

                edge.path[i].state = NodeState.PATH

            final_path += edge.path
            final_path_description.append(edge.path_description)
        if len(final_path) > 0:
            final_path[-1].state = NodeState.START
        return final_path, final_path_description, total_cost


def color_edge(edge):
    """
    Color the edges
    :param edge: The edge
    """
    edge.path[0].state = NodeState.STOP
    for j in range(1, len(edge.path)):
        if edge.path[j].state == NodeState.STOP:
            continue

        edge.path[j].state = NodeState.PATH


class NearestNeighbor:
    """
    A dummy greedy algorithm to find the nearest vertex to the current vertex for every step
    """

    def __init__(self, adjacent_map, vertexes, size, destination=None, is_debug=False):

        self.adjacent_map = adjacent_map
        self.vertexes = vertexes
        self.nums_of_vertexes = len(vertexes)
        self.size = size
        self.start_index = 0
        self.same_target = {}
        self.visited = [False] * self.nums_of_vertexes
        self.result = []
        self.destination = destination
        self.is_debug = is_debug
        self.destination_index = self.nums_of_vertexes - 1

        for i in range(self.nums_of_vertexes):
            curr_vertex = set()

            for j in range(self.nums_of_vertexes):
                if i != j and vertexes[i].is_entrance_of is not None \
                        and vertexes[i].is_entrance_of == vertexes[j].is_entrance_of:
                    curr_vertex.add(j)
            self.same_target[i] = curr_vertex

    def choose_first_vertex(self):
        """
        Choose the first vertex randomly
        :return: The first vertex
        """

        if self.nums_of_vertexes > 1:
            self.start_index = random.randint(0, self.nums_of_vertexes - 1)
        else:
            self.start_index = 0
        curr_vertex = self.vertexes[self.start_index]
        return curr_vertex

    def solver(self):
        """
        Solve the problem using the nearest neighbor algorithm
        :return: the result path, path description and total cost
        """
        # start from a random vertex
        curr_vertex = self.choose_first_vertex()

        self.backtrack(curr_vertex)
        return self.generate_result()

    def backtrack(self, curr_vertex):
        """
        Backtrack the algorithm

        :param curr_vertex: The current vertex
        """
        # End condition, if the result is the size of the vertexes, then we have found the path
        if len(self.result) == self.size - 1:
            final_edge = self.adjacent_map[curr_vertex.index][self.start_index]
            self.result.append(final_edge)
            return

        curr_index = curr_vertex.index
        self.visited[curr_index] = True
        for index in self.same_target[curr_index]:
            self.visited[index] = True

        # Find the nearest vertex
        next_min = float("inf")
        min_edge = None
        min_index = 0
        # If there is a destination, then we need to ensure that the start and the destination are connected
        if self.destination is not None:
            if curr_index == self.destination_index:
                min_edge = self.adjacent_map[curr_index][0]
                min_index = 0
            else:
                for i in range(self.nums_of_vertexes):
                    if self.visited[i]:
                        continue
                    edge = self.adjacent_map[curr_index][i]
                    if i != 0 and edge is not None and edge.weight < next_min:
                        next_min = edge.weight
                        min_edge = edge
                        min_index = i
        # If there is no destination, then we can choose the nearest vertex
        else:
            for i in range(self.nums_of_vertexes):
                if self.visited[i]:
                    continue
                edge = self.adjacent_map[curr_index][i]
                if edge is not None and edge.weight < next_min:
                    next_min = edge.weight
                    min_edge = edge
                    min_index = i

        if self.is_debug and min_edge is None:
            print("Error: ", curr_index, min_index, len(self.result), self.size)
            print(self.visited)
            for i in range(len(self.result)):
                print("(", self.result[i].node1.block, self.result[i].node2.block, ")" + "->", end="")
            print()
            self.print_adjacent_map()
            input()

        self.result.append(min_edge)
        self.backtrack(self.vertexes[min_index])

    def generate_result(self):
        """
        Generate the result path
        :return: the result path, path description and total cost
        """
        final_path = []
        final_path_description = []
        total_cost = 0

        start_index = 0
        for i in range(len(self.result)):
            if self.result[i] is None:
                print(i, len(self.result), self.size)
            if self.result[i].node1.index == 0:
                start_index = i
                # print(path_vertexes[i].block)
                break

        final_path, total_cost, final_path_description = self.construct_path(final_path, final_path_description,
                                                                             total_cost, len(self.result), start_index)
        final_path, total_cost, final_path_description = self.construct_path(final_path, final_path_description,
                                                                             total_cost, start_index)

        if len(final_path) > 0 and final_path[-1] is not None:
            final_path[-1].state = NodeState.START
        return final_path, final_path_description, total_cost

    def construct_path(self, final_path, final_path_description, total_cost, end_index, start_index=0):
        """
        Construct the path from the result edges, description and total cost
        Extract blocks of a path from each edge and add them to the final path
        Set the start and stop state of the path

        :param final_path: The final path
        :param final_path_description: The final path description
        :param total_cost: The total cost
        :param end_index: The end index of the result path
        :param start_index: The start index of the result path
        :return: the final path, path description and total cost
        """
        for i in range(start_index, end_index):
            edge = self.result[i]
            if edge is not None and edge.path is not None and len(edge.path) > 0:
                edge.path[-1].state = NodeState.STOP
                total_cost += edge.weight
                color_edge(edge)

                final_path += edge.path
                final_path_description.append(edge.path_description)

        return final_path, total_cost, final_path_description

    def print_adjacent_map(self):
        """
        Print the adjacent map
        For debug purpose
        """
        for i in range(self.nums_of_vertexes):
            for j in range(self.nums_of_vertexes):
                if self.adjacent_map[i][j] is not None:
                    if self.adjacent_map[i][j].weight < 10:
                        print(self.adjacent_map[i][j].weight, end="   ")

                    else:
                        print(self.adjacent_map[i][j].weight, end="  ")
                else:
                    print("inf", end=" ")
            print()

        print()
