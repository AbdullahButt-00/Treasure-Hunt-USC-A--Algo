pip install pygame
import pygame
import random
from queue import PriorityQueue
import time
from pygame.locals import *

#Global variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

GRID_SIZE = 8
TILE_SIZE = SCREEN_WIDTH // GRID_SIZE
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.radius = 10

    def draw(self,screen):
        pygame.draw.circle(screen, RED, (self.x*TILE_SIZE + TILE_SIZE//2, (GRID_SIZE-1-self.y)*TILE_SIZE + TILE_SIZE//2), self.radius)

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = {}
        self.isAnimal = False
        self.obstacleDirection = None
        self.heuristic_value = None

    def connect(self, node, weight):
        self.edges[node] = weight

    def draw(self, screen, color, border_color):
        if self.isAnimal:
            animal_image = pygame.image.load('animal.png')
            animal_image = pygame.transform.scale(animal_image, (TILE_SIZE, TILE_SIZE))
            screen.blit(animal_image, (self.x*TILE_SIZE, (GRID_SIZE-1-self.y)*TILE_SIZE))
        elif self.obstacleDirection is not None:
            obstacle_image = pygame.image.load('obstacle.jpg')
            obstacle_image = pygame.transform.scale(obstacle_image, (TILE_SIZE, TILE_SIZE))
            if self.obstacleDirection == 'up':
                obstacle_image = pygame.transform.rotate(obstacle_image, 90)
            elif self.obstacleDirection == 'down':
                obstacle_image = pygame.transform.rotate(obstacle_image, 270)
            elif self.obstacleDirection == 'left':
                obstacle_image = pygame.transform.rotate(obstacle_image, 180)
            screen.blit(obstacle_image, (self.x*TILE_SIZE, (GRID_SIZE-1-self.y)*TILE_SIZE))
        else:
            rect = pygame.Rect(self.x*TILE_SIZE, (GRID_SIZE-1-self.y)*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, border_color, pygame.Rect(self.x*TILE_SIZE, (GRID_SIZE-1-self.y)*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def draw_coordinates(self, screen):
        font = pygame.font.Font(None, 24)
        text = font.render(f'({self.x},{self.y})', True, (255, 255, 255))
        screen.blit(text, (self.x*TILE_SIZE, (GRID_SIZE-1-self.y)*TILE_SIZE))
    def __lt__(self, other):
        return self.x < other.x if self.y == other.y else self.y < other.y
class Graph:
    def __init__(self, width, height, animals, obstacles):
        self.nodes = [[Node(x, y) for y in range(height)] for x in range(width)]
        self.width = width
        self.height = height
        for x in range(width):
            for y in range(height):
                weight = 1
                if x > 0:
                    self.nodes[x][y].connect(self.nodes[x - 1][y], weight)
                if x < width - 1:
                    self.nodes[x][y].connect(self.nodes[x + 1][y], weight)
                if y > 0:
                    self.nodes[x][y].connect(self.nodes[x][y - 1], weight)
                if y < height - 1:
                    self.nodes[x][y].connect(self.nodes[x][y + 1], weight)

        for animal in animals:
            self.nodes[animal[0]][animal[1]].isAnimal = True

        for obstacle in obstacles:
            cost = random.randint(2, 4)
            self.nodes[obstacle[0][0]][obstacle[0][1]].edges[self.nodes[obstacle[1][0]][obstacle[1][1]]] = cost
            self.nodes[obstacle[1][0]][obstacle[1][1]].edges[self.nodes[obstacle[0][0]][obstacle[0][1]]] = cost
            self.nodes[obstacle[0][0]][obstacle[0][1]].obstacleDirection = obstacle[2]
        for x in range(width):
            for y in range(height):
                self.nodes[x][y].heuristic_value = abs(x - (width-1)) + abs(y - (height-1))
        

    def draw(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                if self.nodes[x][y].isAnimal:
                    self.nodes[x][y].draw(screen, BLACK, BLACK)
                elif (x, y) == (0, 0):
                    self.nodes[x][y].draw(screen, PURPLE, BLACK)
                elif (x, y) == (self.width-1, self.height-1):
                    self.nodes[x][y].draw(screen, RED, BLACK)
                else:
                    self.nodes[x][y].draw(screen, WHITE, BLACK)
                self.nodes[x][y].draw_coordinates(screen)
    def UCS(self, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        while not frontier.empty():
            current = frontier.get()
            if current == goal:
                break
            for next_node, weight in current.edges.items():
                new_cost = cost_so_far[current] + weight
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost
                    frontier.put(next_node, priority)
                    came_from[next_node] = current
        current = goal
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        total_cost = 0
        return path, total_cost
    def Astar(self, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        total_cost = 0
        while not frontier.empty():
            current = frontier.get()
            if current == goal:
                break
            for next_node, weight in current.edges.items():
                if next_node.isAnimal:
                    random_dice = random.randint(0, 10)
                    if random_dice in [1,2]:
                        random_weight = random.randint(1, 3)
                        weight = random_weight
                    elif random_dice in [3,4,5,6,7,8,9,10]:
                        random_weight = random.randint(2,4)
                        weight = random_weight
                new_cost = cost_so_far[current] + weight + next_node.heuristic_value
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost
                    frontier.put(next_node, priority)
                    came_from[next_node] = current
        current = goal
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path, total_cost
def showAstar(graph, start_node, goal_node, screen, player):
    path,total_cost = graph.Astar(start_node, goal_node)
    for i in range(len(path)-1):
        if path[i].isAnimal:
            random_dice = random.randint(0, 10)
            if random_dice in [1,2]:
                random_weight = random.randint(1, 3)
                total_cost += random_weight
            elif random_dice in [3,4,5,6,7,8,9,10]:
                random_weight = random.randint(2,4)
                total_cost += random_weight
        total_cost += path[i].edges[path[i+1]]
    visualize_path(path, screen, player,graph,total_cost)

def showUCS(graph, start_node, goal_node, screen, player):
    path,total_cost = graph.UCS(start_node, goal_node)
    total_cost = 0
    for i in range(len(path)-1):
        if path[i].isAnimal:
            random_dice = random.randint(0, 10)
            if random_dice in [1,2]:
                random_weight = random.randint(1, 3)
                total_cost += random_weight
            elif random_dice in [3,4,5,6,7,8,9,10]:
                random_weight = random.randint(2,4)
                total_cost += random_weight
        total_cost += path[i].edges[path[i+1]]
    visualize_path(path, screen, player,graph,total_cost)

def visualize_path(path, screen, player,graph,total_cost):
    running = True
    path_index = 0
    font = pygame.font.Font(None, 36)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        graph.draw(screen)
        #Calculate the total cost for the path
        if path_index < len(path):
            player.x = path[path_index].x
            player.y = path[path_index].y
            path_index += 1
            time.sleep(0.2)
        elif path_index == len(path):
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(0, SCREEN_HEIGHT // 2 - 20, SCREEN_WIDTH, 40))
            cost_text = font.render('Total cost: ' + str(total_cost), True, (0, 0, 0))
            screen.blit(cost_text, (SCREEN_WIDTH // 2 - cost_text.get_width() // 2, SCREEN_HEIGHT // 2 - cost_text.get_height() // 2))
        player.draw(screen)
        pygame.display.flip()

    pygame.quit()
    
    


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    background = pygame.image.load('background.jpg')
    button_width, button_height = 200, 50
    astar_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2, button_width, button_height)
    ucs_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 60, button_width, button_height)
    button_color = (0, 255, 0)
    hover_color = (255, 0, 0)

    animals = []
    obstacles = []
    for i in range(random.randint(10, 15)):
        random_x = random.randint(0, GRID_SIZE-1)
        random_y = random.randint(0, GRID_SIZE-1)
        if (random_x,random_y) == (0,0) or (random_x,random_y) == (GRID_SIZE-1,GRID_SIZE-1):
            continue
        animals.append((random_x, random_y))
    for i in range(random.randint(3, 5)):
        x = random.randint(0, GRID_SIZE-1)
        y = random.randint(0, GRID_SIZE-1)
        if (x,y) == (0,0) or (x,y) == (GRID_SIZE-1,GRID_SIZE-1):
            continue
        direction = random.choice(["up", "down", "left", "right"])
        if x == 0 and direction == "left":
            direction = "right"
        if x == GRID_SIZE-1 and direction == "right":
            direction = "left"
        if y == 0 and direction == "up":
            direction = "down"
        if y == GRID_SIZE-1 and direction == "down":
            direction = "up"
        if direction == "up":
            obstacles.append(((x, y), (x, y - 1),'up'))
        elif direction == "down":
            obstacles.append(((x, y), (x, y + 1),'down'))
        elif direction == "left":
            obstacles.append(((x, y), (x - 1, y),'left'))
        elif direction == "right":
            obstacles.append(((x, y), (x + 1, y),'right'))


    graph = Graph(GRID_SIZE, GRID_SIZE, animals, obstacles)

    player = Player(0, 0)


    start_node = graph.nodes[0][0]
    goal_node = graph.nodes[GRID_SIZE-1][GRID_SIZE-1]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos() 
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if astar_button.collidepoint(event.pos):
                    showAstar(graph, start_node, goal_node, screen, player)
                elif ucs_button.collidepoint(event.pos):
                    showUCS(graph, start_node, goal_node, screen, player)

        if astar_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, astar_button) 
        else:
            pygame.draw.rect(screen, button_color, astar_button) 

        if ucs_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, ucs_button)  
        else:
            pygame.draw.rect(screen, button_color, ucs_button) 

        astar_text = font.render('A*', True, (0, 0, 0))
        ucs_text = font.render('UCS', True, (0, 0, 0))
        screen.blit(astar_text, (astar_button.x + 50, astar_button.y + 10))
        screen.blit(ucs_text, (ucs_button.x + 50, ucs_button.y + 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()