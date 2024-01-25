import sys
import time

from maze_env import MazeEnv
from maze_state import MazeState
from search import Search

"""
maze_solver.py

Solves the maze based on the input arguments given.
"""

VISUALISE_TIME_PER_STEP = 1.0
VISUALISE_TIME_END = 5.0

def print_usage():
    print("Usage: python tester.py [search_type] [testcase_file] \
          [-v (optional)]")
    print("    search_type = 'bfs' or 'dfs' or 'iddfs' or 'ucs' or 'greedy' \
          or 'a_star'")
    print("    testcase_file = filename of a valid testcase file \
          (e.g. L1.txt)")
    print("    if -v is specified, the solver's trajectory will be visualised")


def main(arglist):
    # Check if there is the correct number of arguments
    if len(arglist) != 2 and len(arglist) != 3:
        print_usage()
        return
    
    # Check search type
    search_type = arglist[0]
    if search_type not in ['bfs', 'dfs', 'iddfs', 'ucs', 'greedy', 'a_star']:
        print("/!\\ ERROR: Invalid search_type given")
        print_usage()
        return

    # Load the maze environment from the input level
    testcase_file = arglist[1]
    maze_env = MazeEnv(testcase_file)

    # Check if visualisation mode is activated
    if len(arglist) == 3:
        if arglist[2] == '-v':
            visualise = True
        else:
            print(f"/!\\ ERROR: Invalid option given: {arglist[2]}")
            print_usage()
            return
    else:
        visualise = False

    # Run the search chosen on the selected maze
    actions = None
    t0 = time.time()
    solver = Search(maze_env)
    if search_type == 'bfs':
        actions = solver.search_bfs()
    elif search_type == 'dfs':
        actions = solver.search_dfs()
    elif search_type == 'iddfs':
        actions = solver.search_iddfs()
    elif search_type == 'ucs':
        actions = solver.search_ucs()
    elif search_type == 'greedy ':
        actions = solver.search_greedy()
    else:
        actions = solver.search_a_star()
    run_time = (time.time() - t0)

    # Evaluate the solution
    control_env = MazeEnv(testcase_file)
    persistent_state = control_env.get_init_state()
    total_cost = 0.0
    error_occurred = False

    if visualise:
        try:
            from gui import GUI
            gui = GUI(maze_env)
        except ModuleNotFoundError:
            gui = None
            control_env.render(persistent_state)
            time.sleep(VISUALISE_TIME_PER_STEP)
    else:
        gui = None
    
    path = [(persistent_state.row, persistent_state.col)]
    time.sleep(VISUALISE_TIME_PER_STEP)
    cost = 0

    for i in range(len(actions)): # For each action in the solution
        a = actions[i]
        cost += 1
        try:
            total_cost += maze_env.ACTION_COST[a]
            success, persistent_state = maze_env.perform_action(
                persistent_state, a)

            if not success:
                print("/!\\ ERROR: Action resulting in Collision performed at \
                      step " + str(i))
                error_occurred = True

            if visualise:
                if gui is not None:
                    gui.update_state(persistent_state)
                else:
                    print(f"Optimal Path Cost: {control_env.optimal_cost} || \
                          Current Path Cost: {cost}")
                    control_env.render(persistent_state, path)
                    path.append((persistent_state.row, persistent_state.col))
                    time.sleep(VISUALISE_TIME_PER_STEP)
        
        except KeyError:
            print("/!\\ ERROR: Unrecognised action performed at step " 
                  + str(i))
            error_occurred = True

    if error_occurred:
        print("/!\\ ERROR: Collision or Unrecognised Action Occurred")

    if maze_env.is_solved(persistent_state):
        persistent_state = MazeState(-1, -1)
        if visualise:
            if gui is not None:
                gui.remove_player()
            else:
                if cost == control_env.optimal_cost:
                    print(f"Maze Completed - Path Cost: {cost} || Optimal \
                          Path Taken")
                else:
                    print(f"Maze Completed - Path Cost: {cost} || Optimal \
                          Path Not Taken - Optimal Path Cost: \
                          {control_env.optimal_cost}")
                control_env.render(persistent_state, path)
                        
            time.sleep(VISUALISE_TIME_END)
        print(f"Maze completed! \nSolution cost: {total_cost}\nTime to find" +
              f" solution: {round(run_time, 10)} seconds")
    else:
        print("/!\\ ERROR: Level not completed after all actions performed.")
        return


if __name__ == '__main__':
    main(sys.argv[1:])