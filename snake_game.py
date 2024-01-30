import pygame
import os
import random
import snake
from snake_rotation import *
pygame.font.init()

WIDTH, HEIGHT = 780, 780
TILE_SIZE = 30
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Snake")
BG_COLOR = (204, 120, 50)
MOVE_DELAY = 150
score = 0
SCORE_FONT = pygame.font.SysFont("comicsans", 40)
last_move_time = pygame.time.get_ticks()

snake = snake.Snake(WIDTH, HEIGHT, TILE_SIZE)

# constructs the image paths
base_directory = os.path.dirname(__file__)

snake_head_path = os.path.join(base_directory, "snake skin", "snake_head.png")
snake_body_path = os.path.join(base_directory, "snake skin", "snake_body.png")
snake_turn_path = os.path.join(base_directory, "snake skin", "snake_turn.png")
snake_tail_path = os.path.join(base_directory, "snake skin", "snake_tail.png")

# loads the images
SNAKE_HEAD = pygame.image.load(snake_head_path)
SNAKE_BODY = pygame.image.load(snake_body_path)
SNAKE_TURN = pygame.image.load(snake_turn_path)
SNAKE_TAIL = pygame.image.load(snake_tail_path)


def get_fruit_rect(my_snake, width, height, tile_size):
    while True:
        fruit_x = random.randrange(0, width - tile_size, tile_size)
        fruit_y = random.randrange(0, height - tile_size, tile_size)
        fruit_rect = pygame.Rect(fruit_x, fruit_y, tile_size, tile_size)
        if not any(segment.colliderect(fruit_rect) for segment in my_snake.body):
            return fruit_rect


fruit = get_fruit_rect(snake, WIDTH, HEIGHT, TILE_SIZE)


def restart_game(my_snake, width, height, tile_size):
    if my_snake.collide_detect(width, height, tile_size):
        pygame.time.delay(1000)
        # Reset the snake's position and direction
        my_snake.head = pygame.Rect(width//2, height//2, tile_size, tile_size)
        my_snake.direction = "up"
        my_snake.body = [my_snake.head]
        my_snake.grow = False

        # Reset the move delay and last move time
        global MOVE_DELAY
        MOVE_DELAY = 150
        global last_move_time
        last_move_time = pygame.time.get_ticks()
        global score
        score = 0


def draw_window(my_snake, my_fruit, win, bg_color, game_score):
    win.fill(bg_color)
    pygame.draw.rect(win, "red", my_fruit)
    draw_score = SCORE_FONT.render(str(game_score), True, "white")
    win.blit(draw_score, (10, 10))

# snake head
    head_rotation = head_orientation(my_snake)
    win.blit(pygame.transform.rotate(SNAKE_HEAD, head_rotation), (my_snake.head.x, my_snake.head.y))

# snake body and tail
    for i in range(len(my_snake.body) - 1, 0, -1):
        segment = my_snake.body[i]
        prev_segment = my_snake.body[i - 1]
        coming_segment = my_snake.body[i + 1] if i + 1 < len(my_snake.body) else None
        body_rotation = body_orientation(segment, prev_segment)
        snake_skin = SNAKE_BODY
        straight_piece = False

        if segment == my_snake.body[-1]:
            snake_skin = SNAKE_TAIL
            straight_piece = True

        if coming_segment is not None and (prev_segment.x == coming_segment.x or prev_segment.y == coming_segment.y):
            straight_piece = True

        if straight_piece is True and body_rotation is not None:
            win.blit(pygame.transform.rotate(snake_skin, body_rotation), (segment.x, segment.y))

# snake turn
    for i in range(len(my_snake.body) - 1, 0, -1):
        segment = my_snake.body[i]
        prev_segment = my_snake.body[i - 1]
        previouser_segment = my_snake.body[i - 2]
        coming_segment = my_snake.body[i + 1] if i + 1 < len(my_snake.body) else None
        turn_rotation = turn_orientation(segment, prev_segment, previouser_segment, coming_segment, TILE_SIZE)

        # checks if it's a turn piece
        if all([previouser_segment.x != segment.x, previouser_segment.y != segment.y, prev_segment != my_snake.body[0]]):
            win.blit(pygame.transform.rotate(SNAKE_TURN, turn_rotation), (prev_segment.x, prev_segment.y))

        if turn_on_fruit_overlap(segment, prev_segment, previouser_segment, coming_segment, my_snake):
            pygame.draw.rect(win, bg_color, [segment.x, segment.y, TILE_SIZE, TILE_SIZE])
            win.blit(pygame.transform.rotate(SNAKE_TURN, turn_rotation), (prev_segment.x, prev_segment.y))

    pygame.display.update()


def main():
    global last_move_time
    global fruit
    global score
    clock = pygame.time.Clock()
    run = True
    while run:

        current_time = pygame.time.get_ticks()
        if current_time - last_move_time >= MOVE_DELAY:
            # update the snake's position
            if fruit.colliderect(snake.head):
                snake.update_position(TILE_SIZE, fruit)
                fruit = get_fruit_rect(snake, WIDTH, HEIGHT, TILE_SIZE)
                score += 1
            else:
                snake.update_position(TILE_SIZE, fruit)

            last_move_time = current_time

            if snake.collide_detect(WIDTH, HEIGHT, TILE_SIZE):
                restart_game(snake, WIDTH, HEIGHT, TILE_SIZE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                snake_direction(event, snake, TILE_SIZE)

        draw_window(snake, fruit, WIN, BG_COLOR, score)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
