import sys
from time import sleep

from data import Algorithm, MapData
from entities import Item, Shelf, Worker
from service import Map
from visualize import refresh, print_banner, RenderScreen, waiting
from tkinter.filedialog import askopenfilename


def read_map_data(filename):
    """Reads the map data from the given file.
    It first generates a list of items by reading the file line by line.
    Then it generates a list of shelves by calling the gen_shelves function.

    :param filename: A string representing the name of the file to read from.
    :return: items and shelves generated from the data in the file.
    """

    items = []
    try:
        with open(filename, 'r') as file:
            # Skip the first line of the file

            next(file)
            # Read the file line by line
            for line in file:
                data = line.strip().split()
                item = Item(int(data[0]), float(data[1]), float(data[2]))

                items.append(item)
    except FileNotFoundError:
        print('File not found, please make sure the file is in the same directory as the program.')
        choice = input('Press 1 to try again when the file is in the same directory, press 2 to choose file manually: ')
        if choice == '1':
            return read_map_data(filename)
        elif choice == '2':
            print("File Browser will open, please choose the file.")
            filename = askopenfilename()
            return read_map_data(filename)

    shelves = gen_shelves(items)
    return items, shelves


def gen_shelves(items):
    """
    The gen_shelves function takes in a list of items and returns a list of shelves.
    The function first sorts the items by their position (x-coordinate, y-coordinate).
    It then iterates through the sorted list, if the current item has the same position as the previous item,
    it adds the item to the existing shelf. Otherwise, it creates a new shelf and adds the item to the shelf.

    :param items: A list of items read from the database file(from read_map_data function)
    :return: A list of shelves generated from the list of items
    """

    temp = list(items)
    # Sort the items by their position
    temp.sort(key=lambda item: item.pos)
    index = 0

    pre = temp[0]
    shelf = Shelf(index, pre.pos[0], pre.pos[1])
    shelf.add_item(pre)
    shelves = [shelf]
    # Iterate through the sorted list of items
    for i in range(1, len(temp)):

        curr = temp[i]
        # If the current item has the same position as the previous item, add the item to the existing shelf
        if curr.pos == pre.pos:
            i += 1
            shelf.add_item(curr)
        # Otherwise, create a new shelf and add the item to the shelf
        else:
            pre = curr
            index += 1

            shelf = Shelf(index, pre.pos[0], pre.pos[1])
            shelf.add_item(pre)
            shelves.append(shelf)

    return shelves


def get_worker_pos():
    """
    The get_worker_pos function base on the user's input to create a worker.
    If the user wants to use the default position, the function returns a worker with the default position.
    If the user wants to enter a custom position, the function prompts the user to enter the position
    The function then returns a worker with the custom position.


    :return: A worker object, which is used to create a worker
    :author:
    """
    print("-----------------------------------------------------------------------------")
    while True:
        print()
        print("please enter the worker's starting position")
        is_default = input("Do you want to use the default position(0,0)? (y/n)")
        # If the user wants to use the default position, return a worker with the default position
        if is_default == "y":
            return Worker(0, 0)
        # If the user wants to enter a custom position, prompt the user to enter the x-coordinate and y-coordinate
        elif is_default == "n":
            print("worker's x-coordinate is:")
            worker_x = input()
            # Check if the input is numeric
            if worker_x.isnumeric():
                # Convert the input to an integer
                converted_x = int(worker_x)
                print("worker's y-coordinate is:")
                worker_y = input()
                # Check if the input is numeric
                if worker_y.isnumeric():
                    # Convert the input to an integer
                    converted_y = int(worker_y)
                    # Create a worker with the given position
                    worker_pos = (converted_x, converted_y)
                    # Display the worker's position(Let the user confirm the position)
                    print("worker's position is:", worker_pos)
                    print("Press any key to continue")
                    input()
                    return Worker(worker_pos[0], worker_pos[1])  # return the worker's position
                else:
                    print("must be number")
            else:
                print("must be number")
        else:
            print("invalid input")


def peek_items(items):
    """ Prints the items in the list.
        :param items: The list of all items
    """
    for item in items:
        print(item)

    input("Press any key to continue:")
    print()


def set_target_id_once(items_map):
    """
    The set_target_item function takes in a list of items and prompts the user to enter an item id.
    If the input is not numeric, it will prompt again until a valid number is entered.
    It then checks if that number matches any of the item ids in the list, and returns that item if so.

    :param items_map: Pass the list of items to the function
    :return: The target item
    """

    print()
    print("Please enter all the target item's id by once: ")
    print("separate each id by a comma, for example: 1,2,3")
    print("(If you forgot the id, you can press 'p' to see all the items' information)")
    user_input = input()
    if user_input == "p":
        peek_items(items_map)
        return set_target_id_once(items_map)
    target_items = []
    count = 0
    target_list = user_input.split(",")
    print(target_list)
    for target_id in target_list:
        target_id = target_id.strip()
        if target_id.isnumeric():
            converted_id = int(target_id)
            if converted_id in items_map:
                target_items.append(items_map[converted_id])
                count += 1
            else:
                print("Cannot find item with id:", converted_id)
                return set_target_id_once(items_map)
        else:
            print("Invalid input: ", target_id, "is not a number")
            return set_target_id_once(items_map)

    print("You have entered", count, "target items")
    print("Press any key to continue")
    input()
    return target_items


def get_time_limit():
    print("-----------------------------------------------------------------------------")
    choice = input("Do you want to change the time limit ? (y/n) Default is 60 seconds")
    while True:
        if choice == "y":
            print("Please enter the time limit in seconds: ")
            time_limit = input()
            if time_limit.isnumeric():
                return int(time_limit)
            elif is_float(time_limit):
                return float(time_limit)
            else:
                print("Invalid input: ", time_limit, "is not a number")
        else:
            return 60


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def initialize_data():
    """
    The initialize_data function reads the data from the database file to get the items and shelves,
    It first calls the read_map_data function to read the data from the file,
    then calls the get_worker_pos function to get the worker's starting position,
    then calls the set_target_item function to get the target item.
    finally, it generates a MapData object with the data it got from the previous functions.

    :return: A MapData object, which contains all the data needed to create a map
    """

    items, shelves = read_map_data('qvBox-warehouse-data-s23-v01.txt')

    targets = set_targets(items)
    worker = get_worker_pos()
    time_limit = get_time_limit()
    access_mode = set_access_mode()
    map_data = MapData(worker, shelves, items, targets, time_limit=time_limit, access_mode=access_mode)

    return map_data


def set_targets_one_by_one(items_map):
    count = 0
    target_items = []
    while True:
        print()
        print("Please enter each target items' ID, then press 'enter', if you are done, press 'q' to quit")
        print("(If you forgot the id, you can press 'p' to see all the items' information)")
        curr = input()
        if curr == "q":
            return target_items
        elif curr == "p":
            peek_items(list(items_map.values()))
        elif curr.isnumeric():
            converted_id = int(curr)
            if converted_id in items_map:
                target_items.append(items_map[converted_id])
                count += 1
                print("Target items' IDs are: ", list(map(lambda x: x.item_id, target_items)))
            else:
                print("Cannot find item with that id, please try again!")
        else:
            print("Invalid input")


def set_target_from_file(items_map):
    file_path = "qvBox-warehouse-orders-list-part01.txt"
    while True:
        try:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                lines = file_contents.split('\n')
                break

        except FileNotFoundError:
            print("Error: File not found. Please make sure your file is in the same directory as this program.")
            choice = input("Would you like to upload your file manually? (y/n)")
            if choice == "y":
                print("A file explorer will open. Please select your file.")
                file_path = askopenfilename()
            else:
                print("Make sure your file is in the same directory as this program and try again.")
                pass
        except PermissionError:
            print("Error: Permission denied. Make sure you have the necessary permissions to access the file.")
        except Exception as e:
            print("An error occurred:", e)

    order_list = [line.split(', ') for line in lines if line]
    order_list_row = input('Please enter which order row you want to proceed. (Start at 1)')
    curr_order = order_list[int(order_list_row) - 1]
    target_items = []
    for target_id in curr_order:
        target_id = target_id.strip()
        if target_id.isnumeric():
            converted_id = int(target_id)
            if converted_id in items_map:
                target_items.append(items_map[converted_id])
            else:
                print("Cannot find item with id:", converted_id)
                return set_target_from_file(items_map)

    return target_items


def set_targets(items):
    print("-----------------------------------------------------------------------------")
    print("Press 1 to set target items one by one")
    print("Press 2 to enter all target items by once")
    print("Press 3 to enter target items through input files")
    print()
    items_map = {items[i].item_id: items[i] for i in range(len(items))}
    while True:
        choice = input()
        if choice == "1":

            return set_targets_one_by_one(items_map)
        elif choice == "2":
            return set_target_id_once(items_map)
        elif choice == "3":
            return set_target_from_file(items_map)
        else:
            print("Invalid input")


def set_access_mode():
    print("-----------------------------------------------------------------------------")
    print("Press 1 to set access mode to 'single access point'")
    print("Press 2 to set access mode to multiple access point'")
    print("Warning: Current version of the program will not be able to find the optimal path for multiple access point")
    print("-----------------------------------------------------------------------------")
    while True:
        choice = input()
        if choice == "1":
            return "single"
        elif choice == "2":
            return "multiple"
        else:
            print("Invalid input")


def display_welcome():
    """ Displays the welcome screen for the program.

    :return: None
    """

    refresh()
    print_banner()
    print('------------------------------------------------------------------------------------')
    print()
    print('Welcome to Lazy Warehouse Picker!')
    print("Before we start, please make sure you file is in the same directory as this program.")
    print()
    print('------------------------------------------------------------------------------------')
    print("Press 'space' then enter to continue...")
    while True:
        # wait for space key to be pressed
        key = input()
        if key == ' ':
            break
        elif key == 'q':
            sys.exit(0)
        else:
            print("Invalid input")


def find_path(map_data):
    """
    The find_path function takes in a MapData object and prompts the user to select an algorithm.
    It then calls the corresponding function in the Map class.
    If the user input 1, it calls the a_star function in the Map class.
    If the user input 2, it calls the bfs function in the Map class.
    If the user input 3, it calls the dijkstra function in the Map class.
    If the user input 4, it calls the dfs function in the Map class.

    :param map_data: Pass the MapData object to the function
    """

    refresh()
    map_service = Map(map_data)
    render = RenderScreen(waiting)
    render.start()
    map_service.init_for_tsp()
    render.stop()
    sleep(1)
    refresh()
    map_service.print_map()

    while True:

        print('-------------------------------------------------------------------------------------------------------')
        print()
        print("Welcome to the lazy picker for warehouse!")
        print("Press '1' to find a short path(using Branch and Bound), '2' to find the path faster (using Dummy "
              "Greedy),")
        print("Press 'r' to return to the main menu")
        print()
        print('-------------------------------------------------------------------------------------------------------')

        choice = input('Press the corresponding number and enter to continue: ')

        if choice == '1':
            # render = RenderScreen(map_service.print_map_single_search)
            # render.start()
            map_service.tsp("branch_and_bound")
            to_be_continue(map_data, map_service)

        elif choice == '2':
            map_service.tsp("nearest_neighbor")
            to_be_continue(map_data, map_service)

        elif choice == 'r':
            display_menu(map_data)

        else:
            print('Invalid input...')


def to_be_continue(map_data, map_service):
    while True:
        key = input('Press c to continue... if you want to quit, press q')
        if key == 'c':
            render = RenderScreen(map_service.print_map_single_search)
            render.start()
            map_service = Map(map_data)
            map_service.init_for_tsp()
            render.stop()
        elif key == 'q':
            display_menu(map_data)
        else:
            print('Invalid input...')


def setting(map_data):
    """
    The setting function prompts the user to enter a new target item or algorithm.
    It then returns the new map data.

    :param map_data: Pass the map data to the function
    :return: The new map data
    """

    print()

    while True:
        print("Welcome to the setting menu!")
        print("Please enter '1' to set a new target item, '2' to set a new start point, ")
        print("'3' to set a new algorithm, 'r' to return to the main menu")
        choice = input()
        if choice == "1":
            new_targets = set_targets(map_data.items)
            map_data.update("targets", new_targets)

        elif choice == "2":
            new_worker = get_worker_pos()
            map_data.update("worker", new_worker)

        elif choice == "3":
            algo = input("Please enter the algorithm you want to use: 1. A* 2. BFS 3. Dijkstra 4. DFS")
            if algo == "1":
                map_data.update("algorithm", Algorithm.A_STAR)
            elif algo == "2":
                map_data.update("algorithm", Algorithm.BFS)
            elif algo == "3":
                map_data.update("algorithm", Algorithm.DIJKSTRA)
            elif algo == "4":
                map_data.update("algorithm", Algorithm.DFS)

        elif choice == "r":
            return display_menu(map_data)

        else:
            print("Invalid input")
            return setting(map_data)


def display_menu(map_data):
    """
    Displays the menu for the user to choose from.
    The function will display a list of options and then prompt the user to enter their choice.

    :return: The chosen screen
    """

    print('------------------------------------')
    print()
    print('Menu:')
    print('1. Find your target item')
    print('2. Settings')
    print('3. Exit')
    print()
    print('------------------------------------')
    while True:
        choice = input('Press the corresponding number and enter to continue: ')

        if choice == '1':
            return find_path(map_data)

        elif choice == '2':
            return setting(map_data)

        elif choice == '3':
            print('Exiting program...')
            sys.exit(0)

        else:
            print('Invalid choice. Please try again.')


def main():
    """
    The main function is the entry point of the program.
    """

    display_welcome()
    map_data = initialize_data()
    display_menu(map_data)


if __name__ == '__main__':
    main()

"""
----------------------------------------------
NOT USED, save for future development
----------------------------------------------
"""
