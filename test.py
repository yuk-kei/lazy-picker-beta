from data import MapData
from entities import Worker
from lazy_picker import read_map_data
from service import Map
from visualize import RenderScreen

"""--------------------------------------------------------
    This contains all the scripts for testing
    --------------------------------------------------------"""""
"""--------------------------------------------------------
    Test for configuration should be written below
    --------------------------------------------------------"""""
items, shelves = read_map_data('qvBox-warehouse-data-s23-v01.txt')

worker = Worker(0, 0)


target_list_1 = [108335]
target_list_2 = [108335, 391825, 340367, 286457, 661741]
target_list_3 = [281610, 342706, 111873, 198029, 366109, 287261, 76283, 254489, 258540, 286457]
target_list_4 = [427230, 372539, 396879, 391680, 208660, 105912, 332555, 227534, 68048, 188856, 736830, 736831, 479020, 103313, 1]
target_list_5 = [633, 1321, 3401, 5329, 10438, 372539, 396879, 16880, 208660, 105912, 332555, 227534, 68048, 188856, 736830, 736831, 479020, 103313, 1, 20373]
"""-------------------------------------------------------- 
   Data initialization should be written below
--------------------------------------------------------"""

items_map = {items[i].item_id: items[i] for i in range(len(items))}
targets = []
for item_id in target_list_2:
    if item_id in items_map:
        targets.append(items_map[item_id])

map_data = MapData(worker, shelves, items, targets)

"""--------------------------------------------------------
    All the test for algorithm should be written below
    --------------------------------------------------------"""
grid = Map(map_data)
# path = grid.find_single_target()
# path_description = grid.set_path_description(path)
grid.print_map_tsp()
grid.tsp()
# for sentence in path_description:
#     print(sentence)
# grid.dijkstra()
# grid.a_star()
# grid.bfs()

# render = RenderScreen(grid.print_map_single_search)
# render = RenderScreen(grid.print_map_tsp)
# render.start()

# render.stop()
# while True:
#     print("NEXT ITERATION")
#     input()
#     grid.iterate(algorithm='Dijkstra')

# for testing
