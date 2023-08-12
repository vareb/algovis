import pygame
import random
pygame.init()

class DrawInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0 

    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (0, 250, 250),
        (0, 200, 200),
        (0, 150, 150)
    ]

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
        self.block_height = round((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info):
    list = draw_info.list
    
    for i, val in enumerate(list):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height # subtract from height because y coordinate 0 is at the top

        color = draw_info.GRADIENTS[i % 3] # rotate between gradients to distinguish different elements

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

def generate_starting_list(n, min_val, max_val):
    list = []
    for _ in range(0,n):
        i = random.randint(min_val, max_val)
        list.append(i)
    return list

def main():
    run = True
    clock = pygame.time.Clock()
    
    n = 100
    min_val = 0
    max_val = 100

    list = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInfo(800, 600, list)

    while run:
        clock.tick(60)
        draw(draw_info)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                list = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(list)


    pygame.quit()

if __name__ == "__main__":
    main()




