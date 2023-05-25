from time import sleep

from data import MapData
from entities import Worker
from lazy_picker import read_map_data
from service import Map, Block
from visualize import RenderScreen, waiting

"""--------------------------------------------------------
    This contains all the scripts for testing
    --------------------------------------------------------"""""
"""--------------------------------------------------------
    Test for configuration should be written below
    --------------------------------------------------------"""""
items, shelves = read_map_data('qvBox-warehouse-data-s23-v01.txt')

"""--------------------------------------------------------
    Worker position should be written below
    --------------------------------------------------------"""""

worker = Worker(0, 0)
"""-------------------------------------------------------- 
   Test cases:
--------------------------------------------------------"""
# (4, 0)2176620,2176619,2176621  (4,4)2620261, 2620841, (2,4)2625240, 2629382, 2625159, (1,4)1258916
target_list_0 = [2176620,  1258916]
target_list_1 = [108335]
target_list_2 = [108335, 391825, 340367, 286457, 661741]
target_list_3 = [281610, 342706, 111873, 198029, 366109, 287261, 76283, 254489, 258540, 286457]
target_list_4 = [427230, 372539, 396879, 391680, 208660, 105912, 332555, 227534, 68048, 188856, 736830, 736831, 479020, 103313, 1]
target_list_5 = [633, 1321, 3401, 5329, 10438, 372539, 396879, 16880, 208660, 105912, 332555, 227534, 68048, 188856,
                 736830, 736831, 479020, 103313, 1, 20373]

test_case = target_list_3 # change this to test different cases

"""-------------------------------------------------------- 
   Data initialization should be written below
--------------------------------------------------------"""

items_map = {items[i].item_id: items[i] for i in range(len(items))}
targets = []
for item_id in test_case:
    if item_id in items_map:
        targets.append(items_map[item_id])


map_data = MapData(worker, shelves, items, targets)
grid = Map(map_data)
"""--------------------------------------------------------
    All the test for algorithm should be written below
    --------------------------------------------------------"""

""" Test single search algorithm """
# start_block = Block(0, 0)
# end_block = Block(6, 4)
# path = grid.bfs(start_block, end_block)
# path = grid.find_single_target()


# grid.dijkstra()
# grid.a_star()
# grid.bfs()

""" Test TSP algorithm """
# grid.print_map()
grid.init_for_tsp()
# path, path_description = grid.tsp("dummy_greedy")

path, path_description = grid.tsp()

""" Visualize the result """

# for sentence in path_description:
#     print(sentence)

# grid.dump_instruction_into_file()
""" Test the render screen """
# waiting = waiting()
# render = RenderScreen(waiting)
# render.start()
# sleep(10)
# render.stop()
# render = RenderScreen(grid.print_map_single_search)
# render = RenderScreen(grid.print_map_tsp)
# render.start()

# render.stop()
# while True:
#     print("NEXT ITERATION")
#     input()
#     grid.iterate(algorithm='Dijkstra')

# for testing
