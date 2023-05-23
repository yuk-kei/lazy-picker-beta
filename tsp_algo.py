import copy
import random
from queue import PriorityQueue


class Edge:
    def __init__(self, node1, node2, path, path_description):
        self.node1 = node1
        self.node2 = node2
        self.path = path
        self.length = len(path)
        self.path_description = path_description
        self.weight = len(path)

    def __lt__(self, other):
        return self.weight < other.cost

    def __str__(self):
        return f"Edge({self.node1}, {self.node2}, {self.path}, {self.weight})"


class Vertex:
    def __init__(self, node, is_entrance_of=None):
        self.block = node
        self.level = 0
        self.is_entrance_of = is_entrance_of
        self.index = None

    def __str__(self):
        return f"Vertex({self.block}, {self.is_entrance_of})"

    def __eq__(self, other):
        return self.block == other.block

    # def __hash__(self):
    #     return hash(self.block)
    #
    # def __lt__(self, other):
    #     return self.cost < other.cost


class PathTreeNode:

    def __init__(self, vertex, cost=0, parent=None):
        self.vertex = vertex
        self.parent = parent
        self.path = parent.path + vertex.block if parent else vertex.block
        self.cost = cost
        self.matrix = None
        self.len = len(self.path)

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        return f"PathNode({self.vertex}, {self.parent}, {self.path}, {self.cost})"

    def __eq__(self, other):
        return self.vertex == other.vertex


def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print(matrix[i][j], end=" ")
        print()


class Branch_n_Bound:

    def __init__(self, adjacent_map, vertexes, size):

        self.adjacent_map = adjacent_map
        self.vertexes = vertexes
        self.nums_of_vertexes = len(vertexes)
        self.matrix = None
        self.size = size
        self.pq = PriorityQueue()
        self.same_target = {}
        self.result = []
        for i in range(self.nums_of_vertexes):
            curr_vertex = set()
            vertexes[i].index = i
            for j in range(self.nums_of_vertexes):
                if i != j and vertexes[i].is_entrance_of == vertexes[j].is_entrance_of:
                    curr_vertex.add(j)
            self.same_target[i] = curr_vertex
            # print(i, " ", curr_vertex)

    def set_matrix(self):
        self.matrix = [[0 for i in range(self.nums_of_vertexes)] for j in range(self.nums_of_vertexes)]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.adjacent_map[i][j] is None:
                    self.matrix[i][j] = float("inf")
                else:
                    self.matrix[i][j] = self.adjacent_map[i][j].cost

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                print(self.matrix[i][j], end=" ")
            print()

    def get_path(self):

        random_index = random.randint(0, self.nums_of_vertexes - 1)
        random_vertex = self.vertexes[random_index]
        self.reduce_matrix(self.matrix, random_vertex)
        root = PathTreeNode(random_vertex)
        self.pq.put(root)

        iterate = 0
        # self.pq.put(random_vertex)
        while not self.pq.empty():
            iterate += 1
            print("pq size: ", self.pq.qsize())
            curr_node = self.pq.get()

            print_matrix(current_vertex.matrix)

            if len(close_list) == self.nums_of_vertexes:
                self.result.append(current_vertex.index)
                print("success")
                break

            for index in range(self.nums_of_vertexes):
                if index not in close_list:
                    next_vertex = self.vertexes[index]
                    new_matrix = copy.deepcopy(current_vertex.matrix)
                    self.reduce_matrix(new_matrix, next_vertex, current_vertex)

                    self.pq.put(next_vertex)
                    # print("put: ", new_vertex.index)

    def reduce_matrix(self, matrix, curr_tree_node, pre_tree_node=None):
        curr_index = curr_tree_node.index
        # if it is reduced by pre to curr
        if pre_tree_node is not None:

            curr_tree_node.cost = pre_tree_node.cost
            pre_index = pre_tree_node.index
            # delete the row of the pre_vertex
            for j in range(len(matrix)):
                matrix[pre_index][j] = float("inf")
            # delete the column of the curr_vertex
            for i in range(len(matrix)):
                matrix[i][curr_index] = float("inf")
        else:
            curr_tree_node.cost = 0

        # ignore the same target
        for index in self.same_target[curr_index]:
            # set the row and column of the same target to inf
            for i in range(len(matrix)):
                matrix[i][index] = float("inf")
            for j in range(len(matrix)):
                matrix[index][j] = float("inf")

        cost = 0
        # reduce row
        for i in range(len(matrix)):

            row = matrix[i]
            # get the min value of the row
            min_value = min(row)
            if min_value == float("inf") or min_value == 0:
                continue

            else:
                # reduce each element of the row by the min value
                for j in range(len(row)):
                    if row[j] != float("inf") and row[j] != 0:
                        row[j] -= min_value
                matrix[i] = row
                # get the total cost of each row
                cost += min_value

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
                cost += min_value

        print("curr_index: ", curr_index)
        print("cost: ", cost)
        # for i in range(len(self.matrix)):
        #     for j in range(len(self.matrix[0])):
        #         print(self.matrix[i][j], end=" ")
        #     print()
        curr_tree_node.cost += cost
        curr_tree_node.matrix = matrix
