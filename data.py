import json
from enum import unique, Enum


@unique
class Algorithm(Enum):
    """An enumeration of the different algorithms that can be used to solve the problem.
        0: A*, 1: BFS, 2: DFS, 3: Dijkstra
    """
    A_STAR = 0
    BFS = 1
    DFS = 2
    DIJKSTRA = 3


class MapData:
    """A class to store the data for the map."""

    def __init__(self, worker, shelves, items, targets, algorithm=Algorithm.A_STAR, map_row=40, map_col=21):
        self.worker_org = worker.pos
        self.map_row = map_row
        self.map_col = map_col
        self.worker = worker
        self.shelves = shelves
        self.items = items
        self.targets = targets
        self.algorithm = algorithm

    def get_map_row(self):
        return self.map_row

    def get_map_col(self):
        return self.map_col

    def get_worker(self):
        return self.worker

    def get_shelves(self):
        return self.shelves

    def get_items(self):
        return self.items

    def get_worker_org(self):
        return self.worker_org

    def update(self, attribute, value):
        """
        The update function takes in an attribute and a value.
        It then checks to see if the attribute is valid, and if it is,
        it updates the value of that attribute.

        :param self: Represent the instance of the class
        :param attribute: Specify which attribute of the object is being updated
        :param value: Update the attribute of the object

        """
        if attribute == "worker":
            self.worker = value
        elif attribute == "shelves":
            self.shelves = value
        elif attribute == "items":
            self.items = value
        elif attribute == "targets":
            self.targets = value
        elif attribute == "algorithm":
            self.algorithm = value
        else:
            print("Invalid attribute")

    def __str__(self):
        return "Map Row: " + str(self.map_row) + "\n" + "Map Col: " + str(self.map_col) + "\n" + "Worker: " + str(
            self.worker) + "\n" + "Shelves: " + str(self.shelves) + "\n" + "Items: " + str(self.items)

    def toJSON(self):
        """
        The toJSON function is used to convert the object into a JSON string.

        :param self: Refer to the object itself
        :return: A Json String with the map_row, map_col, worker, shelves and items

        """
        return {
            "map_row": self.map_row,
            "map_col": self.map_col,
            "worker": self.worker.toJSON(),
            "shelves": json.dumps(self.shelves, default=lambda o: o.toJSON(), indent=4),
            "items": json.dumps(self.items, default=lambda o: o.toJSON(), indent=4)
        }


class NodeState(Enum):
    """
    An enumeration of the different states that a node can be in;
    0: GOAL, represents the target node(the target item); 1: NEW, represents a node that has not been visited;
    2: OPEN, represents a node in the open list(will be visited in the future);
    3: BLOCK, represents a node that is a shelf; 4: PATH, represents a node that is in the path to the target node;
    5: CLOSE, represents a node that has been visited; 6: START, represents the starting node(worker start position)
    """

    TARGET = 0
    NEW = 1
    OPEN = 2
    BLOCK = 3
    PATH = 4
    CLOSE = 5
    START = 6
    STOP = 7
