from utils import *


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."  # noqa
    # First, reduce the puzzle using the previous function

    # Choose one of the unfilled squares with the fewest possibilities

    # Now use recursion to solve each one of the resulting sudokus, and if one
    # returns a value (not False), return that answer!

    # If you're stuck, see the solution.py tab!

    solution = reduce_puzzle(values)

    if not solution:
        return False
    else:
        unsolved = [box for box in solution.keys() if len(solution[box]) > 1]
        print(len(unsolved))

        if len(unsolved) == 0:
            return solution
        else:
            shortest_box = None
            shortest_value = '9999999999'

            for box in unsolved:
                if len(solution[box]) < len(shortest_value):
                    shortest_box = box
                    shortest_value = solution[box]

            for value in shortest_value:
                solution[shortest_box] = value
                result = search(solution.copy())

                if result:
                    return result

            return False


if __name__ == '__main__':
    # display(search(grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')))  # noqa
    display(search(grid_values('4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')))  # noqa
