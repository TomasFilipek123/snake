import pygame, random, time
from pygame.locals import *
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255,165,0)
COL_WIDTH, COL_HEIGHT, SIZE = 20, 20, 20
SCREEN_WIDTH, SCREEN_HEIGHT = COL_WIDTH * SIZE, COL_HEIGHT * SIZE
THICK = 1
# Returns list of possible locations
def locations():
    #return [0.5*COL_WIDTH*num for num in range(SIZE)]
    locations = []
    for x in range(2 * SIZE):
        for y in range(2 * SIZE):
            if (x * COL_WIDTH/2) % COL_WIDTH == 0 or (y * COL_HEIGHT/2) % COL_HEIGHT == 0:
                continue
            locations.append((x * COL_WIDTH/2, y * COL_HEIGHT/2))
    return locations

def draw_snake(body, screen):
    for i, snake_part in enumerate(body):
        if i == 0:
            color = YELLOW
        elif i % 2 == 1:
            color = GREEN
        else:
            color = ORANGE
        surface = pygame.Surface((COL_WIDTH - 1, COL_HEIGHT - 1))
        surface.fill(color)
        rect = surface.get_rect(center=snake_part)
        screen.blit(surface, rect)


def draw_apple(apple_position, screen):
    apple_surf = pygame.image.load('apple.png')
    apple_surf = pygame.transform.scale(apple_surf, (COL_WIDTH, COL_HEIGHT))
    apple_rect = apple_surf.get_rect(center=apple_position)
    screen.blit(apple_surf, apple_rect)
# Returns Rect object
def grid_maker(surface, thick):
    for x in range(SIZE):
        for y in range(SIZE):
            pygame.draw.rect(surface, GRAY, (x * COL_WIDTH, y * COL_HEIGHT, COL_WIDTH, COL_HEIGHT), thick)
# Function returnig True if snake get apple:
def snake_get_apple(snake_pos, apple_pos):
    return snake_pos[0] == apple_pos[0] and snake_pos[1] == apple_pos[1]

def snake_die(snake_pos, snake_body):
    for snake_part in snake_body[1:]:
        if snake_pos[0] == snake_part[0] and snake_pos[1] == snake_part[1]:
            return True


def main():
    pygame.init()
    pygame.display.set_caption('Snake')

    icon = pygame.image.load('snakehead.png')
    icon = pygame.transform.scale(icon, (40, 40))
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    fps = 10
    snake_body = [(210, 210), (190, 210), (170, 210)]
    snake_position = (210, 210)
    apple_position = random.choice(locations())
    running = True
    dir = 'right'
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_UP and dir != 'down':
                    dir = 'up'
                elif event.key == K_RIGHT and dir != 'left':
                    dir = 'right'
                elif event.key == K_DOWN and dir != 'up':
                    dir = 'down'
                elif event.key == K_LEFT and dir != 'right':
                    dir = 'left'
        screen.fill(WHITE)
        grid_maker(screen, THICK)
        # Updating Snake position
        if dir == 'right':
            snake_position = ((snake_position[0] + SIZE) % SCREEN_WIDTH, snake_position[1])
        elif dir == 'down':
            snake_position = (snake_position[0], (snake_position[1] + SIZE) % SCREEN_HEIGHT)
        elif dir == 'left':
            snake_position = ((snake_position[0] - SIZE) % SCREEN_WIDTH, snake_position[1])
        elif dir == 'up':
            snake_position = (snake_position[0], (snake_position[1] - SIZE) % SCREEN_HEIGHT)

        if snake_get_apple(snake_position, apple_position):
            del apple_position
            while True:
                apple_position = random.choice(locations())
                if apple_position in snake_body:
                    continue
                break

            snake_body.insert(0, (snake_position[0], snake_position[1]))
        elif snake_die(snake_position, snake_body):
            time.sleep(2)
            running = False
        else:
            snake_body.insert(0, (snake_position[0], snake_position[1]))
            del snake_body[-1]
        draw_snake(snake_body, screen)
        draw_apple(apple_position, screen)
        pygame.display.flip()
if __name__ == '__main__':
    main()


