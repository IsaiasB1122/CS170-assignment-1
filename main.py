def user_prompt():
    print (f"Please choose the algorithm you would like to solve the puzzle:")
    print (f"[1] Uniform Cost Search")
    print (f"[2] A* with misplace tile heuristic")
    print (f"[3] A* with Manhattan Distance heuristic")

mega_easy =((1, 2, 3),
            (4, 5, 6),
            (7, 8, 0))
very_easy = ((1, 2, 3), 
            (4, 5, 6),
            (0, 7, 8))
easy =      ((1, 2, 3),
            (4, 5, 6),
            (7, 8, 0))
goal_state = ((1, 2, 3), 
            (4, 5, 6),
            (7, 8, 0))

user_prompt()
choice = input()
if choice == 1:
    print("gaming")