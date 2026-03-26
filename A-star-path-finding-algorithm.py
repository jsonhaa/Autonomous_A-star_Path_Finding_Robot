import random
import time
import socket

class Astar:
    def __init__(self):
        # These are used for randomizing maps
        # self.map = None
        # self.build_map()

        # Self-built maps
        # self.build_physical_map_1()
        # self.build_physical_map_2()
        self.build_physical_map_3()

        self.map_width = 5
        self.map_height = 5
        self.robot_height = 0
        self.robot_width = 0
        self.start = (self.robot_height, self.robot_width)
        self.goal = (self.map_height - 1, self.map_width - 1)
        self.path = []
        self.direction = []
        self.orientation = 1

    def build_physical_map_1(self):
        self.map = [
            ['S', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', 'G']
        ]


    def build_physical_map_2(self):
        self.map = [
            ['S', '#', '.', '.', '.'],
            ['.', '#', '#', '#', '.'],
            ['.', '#', '.', '#', '.'],
            ['.', '#', '#', '#', '.'],
            ['.', '.', '.', '.', 'G']
        ]

    def build_physical_map_3(self):
        self.map = [
            ['S', '#', '.', '#', '.'],
            ['.', '.', '.', '#', '.'],
            ['#', '#', '.', '#', '.'],
            ['.', '#', '.', '#', '.'],
            ['.', '.', '.', '.', 'G'],
        ]

    def build_map(self):
        self.map = []
        for i in range(self.map_height):
            inner_grid = []
            for j in range(self.map_width):
                r = random.random()
                if r < 0.5:
                    inner_grid.append('#')
                else:
                    inner_grid.append(".")
            self.map.append(inner_grid)

        self.map[self.start[0]][self.start[1]] = 'S'
        self.map[self.goal[0]][self.goal[1]] = 'G'


        if not self.is_solvable(self.start, self.goal):
            # self.build_map()
            self.build_physical_map_1()

    def print_map(self):
        print()
        for index, row in enumerate(self.map):
            display_row = list(row)
            if index == self.robot_height:
                display_row[self.robot_width] = 'R'
            print(index, display_row)

    def robot_traversal(self):
        self.print_map() # Initial draw

        for points in self.path:
            # print(points)
            self.robot_height = points[0]
            self.robot_width = points[1]
            self.print_map()
            time.sleep(0.4)

        print("Traversal Complete!")

    def is_solvable(self, start, end):
        visited = []
        to_visit = [start]
        while to_visit:
            current = to_visit.pop(0)
            visited.append(current)

            if current == end:
                return True

            UP = (current[0] - 1, current[1])
            RIGHT = (current[0], current[1] + 1)
            DOWN = (current[0] + 1, current[1])
            LEFT = (current[0], current[1] - 1)

            DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

            for direction in DIRECTIONS:
                if 0 <= direction[0] <= self.map_height - 1 and 0 <= direction[1] <= self.map_width - 1 and self.map[direction[0]][direction[1]] != '#':
                    if direction not in visited:
                        to_visit.append(direction)
        return False

    def heuristic(self, current, goal):
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def astar(self):
        # g_score tracks actual cost from start to each cell
        g_score = {}
        g_score[self.start] = 0

        # open list stores (f_score, node) pairs
        open_list = []
        open_list.append((self.heuristic(self.start, self.goal), self.start))

        came_from = {}

        while open_list:
            open_list.sort()
            f, current = open_list.pop(0)

            if current == self.goal:
                path = []
                while current != self.start:
                    path.append(current)
                    current = came_from[current]
                path.append(self.start)
                path.reverse()
                self.path = path
                print("Path found:", self.path)

                self.robot_traversal()

                facing = 1  # starts facing right (0 = Up, 1 = Right, 2 = Down, 3 = Left)
                start = path[0]

                direction_map = {'U': 0, 'R': 1, 'D': 2, 'L': 3}

                for y, x in path[1:]:
                    next_index = (y, x)
                    sub = (y - start[0], x - start[1])

                    target = ''
                    # figure out which grid direction this step is
                    if sub[0] == 1:
                        target = 'D'
                    elif sub[0] == -1:
                        target = 'U'
                    elif sub[1] == 1:
                        target = 'R'
                    elif sub[1] == -1:
                        target = 'L'

                    target_facing = direction_map[target]

                    # how many right turns needed
                    turns = (target_facing - facing + 4) % 4

                    if turns == 3:
                        self.direction.append('L')  # L = turn right 3 times
                    else:
                        for i in range(turns):
                            self.direction.append('R')  # R = turn right

                    self.direction.append('F')  # F = move forward one cell
                    facing = target_facing
                    start = next_index
                print(self.direction)
                return path

            # Explore neighbors
            UP = (current[0] - 1, current[1])
            RIGHT = (current[0], current[1] + 1)
            DOWN = (current[0] + 1, current[1])
            LEFT = (current[0], current[1] - 1)


            for neighbor in [UP, RIGHT, DOWN, LEFT]:
                # boundary check
                if not (0 <= neighbor[0] <= self.map_height - 1 and 0 <= neighbor[1] <= self.map_width - 1):
                    continue
                # wall check
                if self.map[neighbor[0]][neighbor[1]] == '#':
                    continue

                # g score for this neighbor is current g + 1 step
                new_g = g_score[current] + 1

                # only add if we found a better path to this neighbor
                if neighbor not in g_score or new_g < g_score[neighbor]:
                    g_score[neighbor] = new_g
                    f_score = new_g + self.heuristic(neighbor, self.goal)
                    open_list.append((f_score, neighbor))
                    came_from[neighbor] = current

        return False

    def see_map(self):
        for index, num in enumerate(self.map):
            print(index, num)

    def send_to_esp32(self, max_retries=10):
        for attempt in range(1, max_retries + 1):
            try:
                s = socket.socket()  # ← create NEW socket each attempt!
                s.settimeout(5)
                s.connect(("10.188.130.236", 8080))
                print("Connected to ESP32!")
                break
            except (ConnectionRefusedError, OSError, TimeoutError) as e:
                print(f"Attempt {attempt}/{max_retries} failed: {e}")
                s.close()  # ← close failed socket before retrying!
                if attempt == max_retries:
                    print("Could not reach ESP32. Aborting.")
                    return
                time.sleep(2)

        time.sleep(1)
        s.settimeout(15)
        sf = s.makefile('r', buffering=1)

        for cmd in self.direction:
            try:
                s.send((cmd + '\n').encode())
                response = sf.readline().strip()
                print(f"Sent: {cmd} | Response: {response}")

                if response == "BLOCKED":
                    print("Obstacle detected! Stopping...")
                    break

            except ConnectionResetError:
                print("Connection lost!")
                break
            except TimeoutError:
                print("Timed out!")
                break

        s.close()

if __name__ == "__main__":
    A = Astar()
    A.astar()
    A.send_to_esp32()
