import random
import turtle
import heapq

# ==========================================
# 1 : Maze Generation
# ==========================================

def generate_maze(width, height):
    """
    สร้างเขาวงกตโดยใช้วิธี Randomized Depth-First Search (DFS)
    คืนค่ากลับมาเป็นอาเรย์ 3 มิติที่เก็บข้อมูลกำแพง
    """
    # สร้าง Grid เก็บข้อมูลกำแพง [ซ้าย, บน, ขวา, ล่าง] (1=มีกำแพง, 0=ไม่มี)
    maze_grid = [[[1, 1, 1, 1] for _ in range(width)] for _ in range(height)]
    
    x, y = 0, 0
    visited_count = 1  # ตัวนับจำนวนช่องที่ไปมาแล้ว
    total_cells = width * height
    
    # Stack สำหรับเก็บประวัติการเดิน (ใช้ย้อนกลับเมื่อเจอทางตัน)
    path_history = [[x, y]] 
    
    # ตารางเช็คว่าช่องไหนเคยไปมาแล้วบ้าง
    visited = [[0 for _ in range(width)] for _ in range(height)]
    visited[0][0] = 1

    while visited_count < total_cells:
        # ตรวจสอบ 4 ทิศทางว่าไปทางไหนได้บ้างที่ยังไม่เคยไป
        # options เก็บค่า [ซ้าย, บน, ขวา, ล่าง]
        options = [0, 0, 0, 0]

        # เช็คซ้าย
        if x != 0 and visited[y][x-1] == 0:
            options[0] = 1
        # เช็คบน
        if y != height-1 and visited[y+1][x] == 0:
            options[1] = 1
        # เช็คขวา
        if x != width-1 and visited[y][x+1] == 0:
            options[2] = 1
        # เช็คล่าง
        if y != 0 and visited[y-1][x] == 0:
            options[3] = 1
        
        # ถ้าไปต่อไม่ได้เลย (ทางตัน) -> ย้อนกลับ (Backtrack)
        if options == [0, 0, 0, 0]:
            current_node = path_history.pop() # ดึงค่าล่าสุดออก
            x, y = current_node[0], current_node[1]
        
        # ถ้ามีทางไปต่อ -> สุ่มเลือก 1 ทาง
        else:
            node_found = False
            while not node_found:
                rand_direction = random.randint(0, 3)
                
                if options[rand_direction] == 1:
                    # 0=ซ้าย, 1=บน, 2=ขวา, 3=ล่าง
                    if rand_direction == 0:
                        next_node = [x-1, y]
                        maze_grid[y][x][0] = 0       # ทุบกำแพงซ้ายเรา
                        maze_grid[y][x-1][2] = 0     # ทุบกำแพงขวาเขา
                    elif rand_direction == 1:
                        next_node = [x, y+1]
                        maze_grid[y][x][1] = 0       # ทุบกำแพงบนเรา
                        maze_grid[y+1][x][3] = 0     # ทุบกำแพงล่างเขา
                    elif rand_direction == 2:
                        next_node = [x+1, y]
                        maze_grid[y][x][2] = 0       # ทุบกำแพงขวาเรา
                        maze_grid[y][x+1][0] = 0     # ทุบกำแพงซ้ายเขา
                    else:
                        next_node = [x, y-1]
                        maze_grid[y][x][3] = 0       # ทุบกำแพงล่างเรา
                        maze_grid[y-1][x][1] = 0     # ทุบกำแพงบนเขา
                    
                    # อัปเดตสถานะ
                    path_history.append([x, y]) # เก็บจุดเดิมไว้ก่อนย้าย
                    x, y = next_node[0], next_node[1]
                    visited[y][x] = 1
                    visited_count += 1
                    node_found = True
    return maze_grid

def draw_maze(width, height, maze_grid):
    """ วาดเขาวงกตด้วย Turtle Graphics """
    start_x = -380
    start_y = -start_x
    grid_size = (2 * (-start_x)) / width
    
    # ตั้งค่า Turtle ให้วาดเร็วที่สุด (ปิด Animation)
    turtle.tracer(0)
    turtle.hideturtle()
    turtle.clear()
    turtle.speed(0)
    
    # วาดกรอบและเส้น
    turtle.penup()
    turtle.goto(start_x, start_y)
    turtle.pendown()
    turtle.goto(-start_x, start_y)
    turtle.goto(-start_x, -start_y)
    turtle.setheading(0)
    
    # วาดเส้นแนวนอน
    for y in range(width):
        turtle.penup()
        turtle.goto(start_x, -start_y + grid_size * y)
        for x in range(height):
            if maze_grid[y][x][3] == 1: # เช็คกำแพงล่าง
                turtle.pendown()
            else:
                turtle.penup()
            turtle.forward(grid_size)
            
    turtle.left(90)
    
    # วาดเส้นแนวตั้ง
    for x in range(width):
        turtle.penup()
        turtle.goto(start_x + grid_size * x, -start_y)
        for y in range(height):
            if maze_grid[y][x][0] == 1: # เช็คกำแพงซ้าย
                turtle.pendown()
            else:
                turtle.penup()
            turtle.forward(grid_size)
            
    turtle.update() # อัปเดตหน้าจอทีเดียวเมื่อวาดเสร็จ

def add_open_zones(maze_grid, width, height, remove_percentage=10):
    # สุ่มทุบกำแพงเพิ่มเพื่อให้เกิด Loop และพื้นที่เปิด (Open Zone)
    total_walls_removed = 0
    target_remove = (width * height) * (remove_percentage / 100)
    
    while total_walls_removed < target_remove:
        # สุ่มเลือกจุด
        x = random.randint(1, width - 2)
        y = random.randint(1, height - 2)
        # สุ่มทิศทางที่จะทุบ (0=ซ้าย, 1=บน, 2=ขวา, 3=ล่าง)
        direction = random.randint(0, 3)
        
        # ถ้าตรงนั้นมีกำแพงอยู่ -> ทุบเลย!
        if maze_grid[y][x][direction] == 1:
            if direction == 0: # ซ้าย
                maze_grid[y][x][0] = 0
                maze_grid[y][x-1][2] = 0
            elif direction == 1: # บน
                maze_grid[y][x][1] = 0
                maze_grid[y+1][x][3] = 0
            elif direction == 2: # ขวา
                maze_grid[y][x][2] = 0
                maze_grid[y][x+1][0] = 0
            elif direction == 3: # ล่าง
                maze_grid[y][x][3] = 0
                maze_grid[y-1][x][1] = 0
            
            total_walls_removed += 1

# ==========================================
# 2 : Helper Functions
# ==========================================

def get_heuristic(x1, y1, x2, y2):
    """ 
    คำนวณ Manhattan Distance 
    ใช้ประเมินระยะห่างจากจุดปัจจุบันไปถึงเป้าหมาย
    """
    return abs(x1 - x2) + abs(y1 - y2)

def get_next_node_coords(direction, current_node):
    """ คำนวณพิกัดถัดไปตามทิศทาง (0=ซ้าย, 1=บน, 2=ขวา, 3=ล่าง) """
    x, y = current_node[0], current_node[1]
    if direction == 0:   return [x-1, y]
    elif direction == 1: return [x, y+1]
    elif direction == 2: return [x+1, y]
    else:                return [x, y-1]

def reconstruct_path(visited_map, width, height, maze_grid):
    """ 
    สร้างเส้นทางย้อนกลับจากจุดสิ้นสุดมาจุดเริ่มต้น 
    โดยดูจากค่า Distance ที่บันทึกไว้ใน visited_map
    """
    distance = visited_map[width-1][height-1]
    route = [[width-1, height-1]] # เริ่มที่จุดสิ้นสุด
    
    # วนลูปย้อนกลับจนกว่าจะถึงจุดเริ่มต้น [0,0]
    while route[0] != [0, 0]:
        cx, cy = route[0][0], route[0][1]
        
        # เช็ค 4 ทิศ ถ้าไม่มีกำแพง และค่าระยะทางลดลง 1 -> คือทางที่เดินมา
        # เช็คซ้าย
        if maze_grid[cy][cx][0] == 0 and visited_map[cy][cx-1] == distance - 1:
            route.insert(0, [cx-1, cy])
            distance -= 1
        # เช็คบน
        elif maze_grid[cy][cx][1] == 0 and visited_map[cy+1][cx] == distance - 1:
            route.insert(0, [cx, cy+1])
            distance -= 1
        # เช็คขวา
        elif maze_grid[cy][cx][2] == 0 and visited_map[cy][cx+1] == distance - 1:
            route.insert(0, [cx+1, cy])
            distance -= 1
        # เช็คล่าง
        elif maze_grid[cy][cx][3] == 0 and visited_map[cy-1][cx] == distance - 1:
            route.insert(0, [cx, cy-1])
            distance -= 1
            
    return route

def draw_route(route, start_x, start_y, grid_size):
    """ วาดเส้นทางคำตอบสีแดง """
    turtle.speed(0)
    turtle.penup()
    
    first_node = route[0] # จุดเริ่มต้น (ปกติคือ [0,0])
    current_x = start_x + (first_node[0] * grid_size) + (grid_size / 2)
    current_y = -start_y + (first_node[1] * grid_size) + (grid_size / 2)
    turtle.goto(current_x, current_y)
    turtle.pendown()
    turtle.pensize(grid_size/2)
    turtle.color("red")
    
    for i in range(len(route)-1):
        # คำนวณพิกัดใหม่
        next_node = route[i+1]
        
        next_x = start_x + (next_node[0] * grid_size) + (grid_size / 2)
        next_y = -start_y + (next_node[1] * grid_size) + (grid_size / 2)
        
        turtle.goto(next_x, next_y)

    turtle.update()

# ==========================================
# 3 : Algorithm Breadth First Search & A*
# ==========================================

def bfs_search(maze_grid, height, width):
    # Breadth-First Search (BFS)
    visited = [[0 for _ in range(width)] for _ in range(height)]
    visited[0][0] = 1
    
    queue = [[0, 0]] # ใช้ Queue เก็บจุดที่ต้องสำรวจ
    explored_count = 0
    
    while len(queue) > 0:
        current = queue.pop(0) # FIFO: ดึงตัวแรกสุดออก
        explored_count += 1
        
        cx, cy = current[0], current[1]

        # ถ้าถึงเป้าหมาย หยุดทันที
        if cx == width-1 and cy == height-1:
            break

        # ตรวจสอบ 4 ทิศ
        for direction in range(4):
            if maze_grid[cy][cx][direction] == 0: # ถ้าไม่มีกำแพง
                neighbor = get_next_node_coords(direction, current)
                nx, ny = neighbor[0], neighbor[1]
                
                # ถ้ายังไม่เคยไป
                if visited[ny][nx] == 0:
                    visited[ny][nx] = visited[cy][cx] + 1 # บันทึกระยะทาง
                    queue.append(neighbor)
                    
    return visited, explored_count

def a_star_search(maze_grid, height, width):
    # A* Search Algorithm
    end_x, end_y = width - 1, height - 1
    
    # g_score: ต้นทุนจริงจากจุดเริ่มต้น
    g_score = [[float('inf') for _ in range(width)] for _ in range(height)]
    g_score[0][0] = 0
    
    # Priority Queue เก็บ (f_score, g_score, x, y)
    # f_score = g_score + h_score
    open_set = []
    
    # เริ่มต้นใส่จุดแรกลงไป
    h_start = get_heuristic(0, 0, end_x, end_y)
    heapq.heappush(open_set, (0 + h_start, 0, 0, 0))
    
    explored_count = 0
    
    while open_set:
        # ดึงโหนดที่มี f_score ต่ำที่สุดออกมาสำรวจ
        current_f, current_g, cx, cy = heapq.heappop(open_set)
        explored_count += 1
        
        # เจอเป้าหมายแล้ว
        if cx == end_x and cy == end_y:
            print(">>> A* พบเส้นทางแล้ว!")
            return g_score, explored_count
        
        current_node = [cx, cy]
        for direction in range(4):
            if maze_grid[cy][cx][direction] == 0: # ถ้าไม่มีกำแพง
                neighbor = get_next_node_coords(direction, current_node)
                nx, ny = neighbor[0], neighbor[1]
                
                new_g = current_g + 1 # ระยะทางเพิ่มขึ้น 1 ช่อง
                
                # ถ้าเส้นทางใหม่นี้ดีกว่าเส้นทางเดิมที่เคยเจอ
                if new_g < g_score[ny][nx]:
                    g_score[ny][nx] = new_g
                    h_score = get_heuristic(nx, ny, end_x, end_y)
                    f_score = new_g + h_score
                    
                    heapq.heappush(open_set, (f_score, new_g, nx, ny))
                    
    return None, explored_count

# ==========================================
# 4 : Main Program
# ==========================================

if __name__ == "__main__":
    # 1. ตั้งค่าเริ่มต้น
    MAP_WIDTH = 60
    MAP_HEIGHT = 60
    START_X = -380
    START_Y = -START_X
    GRID_SIZE = (2 * (-START_X)) / MAP_WIDTH

    print(f"กำลังสร้างเขาวงกตขนาด {MAP_WIDTH}x{MAP_HEIGHT} ...")
    maze = generate_maze(MAP_WIDTH, MAP_HEIGHT)

    # =========================================
    # สถานการณ์ที่ 1 : เขาวงกตปกติทางออกเดียว
    # =========================================
    print("\n" + "="*40)
    print("สถานการณ์ที่ 1 : ก่อนทุบกำแพง (Normal)")
    print("="*40)
    
    # รัน BFS
    _, bfs_count_1 = bfs_search(maze, MAP_HEIGHT, MAP_WIDTH)
    print(f"1. BFS สำรวจ : {bfs_count_1} nodes")
    
    # รัน A*
    _, astar_count_1 = a_star_search(maze, MAP_HEIGHT, MAP_WIDTH)
    print(f"2. A* สำรวจ : {astar_count_1} nodes")
    
    diff_1 = bfs_count_1 - astar_count_1
    percent_1 = (diff_1 / bfs_count_1) * 100
    print(f">>> ผลลัพธ์ : A* สำรวจ Node น้อยกว่า {percent_1:.2f}%")

    # =========================================
    # สถานการณ์ที่ 2: เขาวงกตแบบเปิด (Open Zone)
    # =========================================
    print("\n" + "="*40)
    print("สถานการณ์ที่ 2: หลังทุบกำแพง 20% (Open Zone)")
    print("="*40)
    
    # สุ่มทุบกำแพงเพิ่ม 20%
    add_open_zones(maze, MAP_WIDTH, MAP_HEIGHT, remove_percentage=20)
    
    # รัน BFS รอบ 2
    _, bfs_count_2 = bfs_search(maze, MAP_HEIGHT, MAP_WIDTH)
    print(f"1. BFS สำรวจ: {bfs_count_2} nodes")
    
    # รัน A* รอบ 2 (ต้องรันใหม่เพราะทางเปลี่ยน)
    astar_result_2, astar_count_2 = a_star_search(maze, MAP_HEIGHT, MAP_WIDTH)
    print(f"2. A* สำรวจ: {astar_count_2} nodes")
    
    diff_2 = bfs_count_2 - astar_count_2
    percent_2 = (diff_2 / bfs_count_2) * 100
    print(f">>> ผลลัพธ์: A* สำรวจ Node น้อยกว่า {percent_2:.2f}%")

    # =========================================
    # สรุปผลการทดลอง
    # =========================================
    print("\n" + "#"*40)
    print("\tสรุปผลการเปรียบเทียบ")
    print("#"*40)
    print(f"ก่อนทุบ : A* สำรวจ Node น้อยกว่า BFS ประมาณ {percent_1:.2f}%")
    print(f"หลังทุบ : A* สำรวจ Node น้อยกว่า BFS ประมาณ {percent_2:.2f}%")

    # วาดเขาวงกต (แบบหลังทุบแล้ว) และเส้นทางคำตอบ
    draw_maze(MAP_WIDTH, MAP_HEIGHT, maze)
    
    if astar_result_2:
        path = reconstruct_path(astar_result_2, MAP_WIDTH, MAP_HEIGHT, maze)
        draw_route(path, START_X, START_Y, GRID_SIZE)
    
    input("\nกด Enter เพื่อจบโปรแกรม...")