import pygame
import random
import math
pygame.init()

class DrawInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0 
    DARKGREEN = 0, 100, 0

    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (0, 250, 250),
        (0, 200, 200),
        (0, 150, 150)
    ]

    FONT = pygame.font.SysFont('cambriacambriamath', 28)
    LARGE_FONT = pygame.font.SysFont('cambriacambriamath', 40)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__ (self, width, height, list):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Algorithm Visualizer")
        self.set_list(list)

    def set_list(self, list):
        self.list = list
        self.max_val = max(list)
        self.min_val = min(list)

        self.block_width = round((self.width - self.SIDE_PAD) / len(list))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.DARKGREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

    controls = draw_info.FONT.render("(R) - Reset | (Space) - Start | (A) - Ascending | (D) - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 35))
 
    sorting = draw_info.FONT.render("(I) - Insertion Sort | (B) - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 65))
 


    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    list = draw_info.list
    

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, 
                                                                draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(list):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height # subtract from height because y coordinate 0 is at the top

        color = draw_info.GRADIENTS[i % 3] # rotate between gradients to distinguish different elements

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()
        
def generate_starting_list(n, min_val, max_val):
    list = []
    for _ in range(0,n):
        i = random.randint(min_val, max_val)
        list.append(i)
    return list


def bubblesort(draw_info, ascending=True):
    list = draw_info.list 
    for i in range(len(list) - 1):
        for j in range(len(list) - 1 - i):
            n1 = list[j]
            n2= list[j + 1]

            if (n1 > n2 and ascending) or (n1 < n2 and not ascending): # for asc and desc order
                list[j], list[j+1] = list[j+1], list[j]
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.BLACK}, True)
                yield True
    return list

def insertionsort(draw_info, ascending=True):
    list = draw_info.list
    for i in range(1, len(list)):
        current = list[i]
        
        while True:
            ascending_sort = i > 0 and list[i - 1] > current and ascending
            descending_sort = i > 0 and list[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            list[i] = list[i - 1]
            i -= 1
            list[i] = current
            draw_list(draw_info, {i: draw_info.GREEN, i - 1: draw_info.BLACK}, True)
            yield True
    
    return list


def main():
    run = True
    clock = pygame.time.Clock()
    
    n = 100
    min_val = 0
    max_val = 100

    list = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInfo(800, 600, list)
    sorting = False
    ascending = True

    sorting_algorithm = bubblesort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(120)

        if sorting:
            try: 
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                list = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(list)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and sorting == False:
                ascending = True
            elif event.key == pygame.K_d and sorting == False:
                ascending = False
            elif event.key == pygame.K_i and sorting == False:
                sorting_algorithm = insertionsort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and sorting == False:
                sorting_algorithm = bubblesort
                sorting_algo_name = "Bubble Sort"



    pygame.quit()

if __name__ == "__main__":
    main()




